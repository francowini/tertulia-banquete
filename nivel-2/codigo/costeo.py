"""Costeo de la carta de El Término Medio (nivel 2).

Uso: python3 -I costeo.py <dir_material> <fecha YYYY-MM-DD> <salida.csv> [precios_usados.csv] [desglose.csv]
Entradas en <dir_material>: recetas.json, catalogo.csv, rendimientos.csv,
facturas/*.pdf|*.txt y notas/*.pdf|*.txt (PDF se lee con `pdftotext -layout`).
"""
import csv, json, re, sys, glob, os, subprocess
from decimal import Decimal as D, ROUND_HALF_UP

def num(s):
    """Número en formato argentino ('1.234,56' o '1234,56') -> Decimal exacto."""
    s = s.strip().replace('$', '').replace('%', '').strip()
    return D(s.replace('.', '').replace(',', '.'))

def texto(path):
    if path.endswith('.pdf'):
        return subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True, check=True).stdout
    return open(path, encoding='utf-8').read()

COLUMNAS = {'Cant.': 'cantidad', 'Cantidad': 'cantidad', 'Unidad': 'presentacion', 'Presentación': 'presentacion',
            'P. unitario': 'precio', 'Precio': 'precio', 'Bonif.%': 'bonif', 'Bonif.': 'bonif', 'Neto': 'neto'}

def orden_columnas(t):
    """Cada proveedor ordena distinto las columnas: se lee el orden desde el encabezado de la tabla."""
    for line in t.splitlines():
        if ('descripción' in line) or ('Producto' in line and 'Neto' in line):
            cab = line.split('|') if '|' in line else re.split(r'\s{2,}', line.strip())
            cols = [COLUMNAS[c.strip()] for c in cab if c.strip() in COLUMNAS]
            if len(cols) == 5: return cols
    raise ValueError('sin encabezado de tabla')

def leer_facturas(base):
    renglones = []
    for f in sorted(glob.glob(f'{base}/facturas/*')):
        t = texto(f)
        doc = re.search(r'Factura\s+(F-\w+)', t).group(1)
        fecha = re.search(r'Fecha:\s*(\d{4}-\d{2}-\d{2})', t).group(1)
        cols = orden_columnas(t)
        total = re.search(r'TOTAL:?\s*\$?\s*([\d.,]+)', t)
        suma = D(0)
        for line in t.splitlines():
            tok = [x for x in re.split(r'\s*\|\s*|\s+', line.strip()) if x]
            if len(tok) >= 7 and tok[0].isdigit() and re.fullmatch(r'[A-Z]\d{2}', tok[1]):
                v = dict(zip(cols, tok[-5:]))
                r = dict(doc=doc, fecha=fecha, renglon=int(tok[0]), producto=tok[1], presentacion=v['presentacion'],
                         cantidad=num(v['cantidad']), precio=num(v['precio']), bonif=num(v['bonif']), neto=num(v['neto']),
                         archivo=os.path.basename(f))
                renglones.append(r); suma += r['neto']
        if total and abs(num(total.group(1)) - suma) > D('0.05'):
            print(f'AVISO {doc}: TOTAL {total.group(1)} != suma de netos {suma}', file=sys.stderr)
    return renglones

def leer_notas(base):
    notas = []
    for f in sorted(glob.glob(f'{base}/notas/*')):
        t = texto(f)
        g = lambda k: re.search(k + r'\s*:\s*(.+)', t).group(1).strip()
        cant = g('Cantidad devuelta').split()
        notas.append(dict(nota=re.search(r'Nota de crédito\s+(\S+)', t).group(1), fecha=g('Fecha'),
                          doc=g('Factura asociada'), renglon=int(g('Renglón')), producto=g('Producto').split()[0],
                          concepto=g('Concepto').lower(), cantidad=num(cant[0]), unidad=cant[1],
                          importe=num(g('Importe acreditado')), archivo=os.path.basename(f)))
    return notas

def cargar(base):
    cat = {(r['producto'], r['presentacion']): D(r['cantidad_base']) for r in csv.DictReader(open(f'{base}/catalogo.csv', encoding='utf-8'))}
    rend = {r['producto']: (D(r['limpio_sobre_bruto']), D(r['cocido_sobre_limpio'])) for r in csv.DictReader(open(f'{base}/rendimientos.csv', encoding='utf-8'))}
    recetas = {r['codigo']: r for r in json.load(open(f'{base}/recetas.json', encoding='utf-8'))}
    return cat, rend, recetas, leer_facturas(base), leer_notas(base)

def precios(cat, renglones, notas, fecha):
    """Precio por unidad base de cada producto: última factura <= fecha (empate: id mayor),
    ajustada por las notas emitidas <= fecha que apuntan a ese documento y renglón."""
    elegido = {}
    for r in renglones:
        if r['fecha'] > fecha: continue
        k = (r['fecha'], r['doc'])
        if r['producto'] not in elegido or k > (elegido[r['producto']]['fecha'], elegido[r['producto']]['doc']):
            elegido[r['producto']] = r
    precio, traza = {}, {}
    for p, r in elegido.items():
        neto = r['neto']; eq = r['cantidad'] * cat[(p, r['presentacion'])]; aplicadas = []
        for n in notas:
            if n['doc'] == r['doc'] and n['renglon'] == r['renglon'] and n['fecha'] <= fecha:
                assert n['producto'] == p, (n, r)
                neto -= n['importe']                      # bonificación y devolución restan importe
                if n['concepto'].startswith('devoluci'):  # devolución además resta unidades
                    eq -= n['cantidad'] * cat[(p, n['unidad'])]
                aplicadas.append(n['nota'])
        precio[p] = neto / eq
        traza[p] = dict(producto=p, factura=r['doc'], fecha=r['fecha'], renglon=r['renglon'], neto=neto,
                        cantidad_base=eq, notas='+'.join(aplicadas), precio_base=precio[p])
    return precio, traza

def desglose(cod, recetas, rend, precio):
    """Filas de trazabilidad de un plato: cada ingrediente o subreceta con su cantidad bruta, precio y subtotal."""
    filas = []
    for ing in recetas[cod]['ingredientes']:
        p, q, est = ing['producto'], D(str(ing['cantidad'])), ing['estado']
        if p in recetas:
            unit = costo(p, recetas, rend, precio) / D(str(recetas[p]['rendimiento']))
            filas.append(dict(plato=cod, componente=p, tipo='subreceta', estado=est, cantidad_receta=q,
                              cantidad_bruta=q, precio_unitario=unit, subtotal=unit * q))
        else:
            lb, cl = rend[p]
            bruto = {'bruto': q, 'limpio': q / lb, 'cocido': q / (lb * cl)}[est]
            filas.append(dict(plato=cod, componente=p, tipo='producto', estado=est, cantidad_receta=q,
                              cantidad_bruta=bruto, precio_unitario=precio[p], subtotal=bruto * precio[p]))
    return filas

def costo(cod, recetas, rend, precio, memo=None):
    """Costo total de una receta (su rendimiento declarado). Subrecetas: costo de tanda / rendimiento * cantidad."""
    memo = {} if memo is None else memo
    if cod in memo: return memo[cod]
    total = D(0)
    for ing in recetas[cod]['ingredientes']:
        p, q, est = ing['producto'], D(str(ing['cantidad'])), ing['estado']
        if p in recetas:
            total += costo(p, recetas, rend, precio, memo) / D(str(recetas[p]['rendimiento'])) * q
            continue
        lb, cl = rend[p]
        bruto = {'bruto': q, 'limpio': q / lb, 'cocido': q / (lb * cl)}[est]
        total += bruto * precio[p]
    memo[cod] = total
    return total

if __name__ == '__main__':
    base, fecha, salida = sys.argv[1:4]
    cat, rend, recetas, renglones, notas = cargar(base)
    precio, traza = precios(cat, renglones, notas, fecha)
    os.makedirs(os.path.dirname(salida) or '.', exist_ok=True)
    with open(salida, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n'); w.writerow(['plato', 'costo_por_porcion'])
        for cod, r in recetas.items():
            if r['unidad_rendimiento'] != 'porción': continue   # las subrecetas no son platos
            c = costo(cod, recetas, rend, precio) / D(str(r['rendimiento']))
            w.writerow([cod, str(c.quantize(D('0.01'), rounding=ROUND_HALF_UP))])
    if len(sys.argv) > 5:  # desglose por plato: de dónde sale cada costo
        with open(sys.argv[5], 'w', encoding='utf-8', newline='') as fh:
            campos = ['plato', 'componente', 'tipo', 'estado', 'cantidad_receta', 'cantidad_bruta', 'precio_unitario', 'subtotal']
            w = csv.DictWriter(fh, fieldnames=campos, lineterminator='\n'); w.writeheader()
            for cod, r in recetas.items():
                for f in desglose(cod, recetas, rend, precio):
                    w.writerow({k: (f'{v:.6f}' if isinstance(v, D) else v) for k, v in f.items()})
    if len(sys.argv) > 4:
        with open(sys.argv[4], 'w', encoding='utf-8', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(next(iter(traza.values())).keys()), lineterminator='\n'); w.writeheader()
            for p in sorted(traza): w.writerow(traza[p])
