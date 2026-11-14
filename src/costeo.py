"""Costeo de platos de El Término Medio. Uso: python3 -I src/costeo.py <dir_material> <fecha YYYY-MM-DD> <salida.csv>"""
import csv, json, re, sys, glob, os
from decimal import Decimal as D, ROUND_HALF_UP

def num(s):  # formato argentino 1.234,56 -> Decimal
    return D(s.strip().replace('.', '').replace(',', '.').replace('%', '').strip())

def cargar(base):
    cat = {(r['producto'], r['presentacion']): D(r['cantidad_base']) for r in csv.DictReader(open(f'{base}/catalogo.csv', encoding='utf-8'))}
    rend = {r['producto']: (D(r['limpio_sobre_bruto']), D(r['cocido_sobre_limpio'])) for r in csv.DictReader(open(f'{base}/rendimientos.csv', encoding='utf-8'))}
    recetas = {r['codigo']: r for r in json.load(open(f'{base}/recetas.json', encoding='utf-8'))}
    renglones = []
    for f in sorted(glob.glob(f'{base}/facturas/*.txt')):
        txt = open(f, encoding='utf-8').read()
        doc = re.search(r'Factura\s+(\S+)', txt).group(1)
        fecha = re.search(r'Fecha:\s*(\d{4}-\d{2}-\d{2})', txt).group(1)
        for line in txt.splitlines():
            p = [x.strip() for x in line.split('|')]
            if len(p) == 7 and p[0].isdigit():
                prod = p[1].split()[0]
                cant, precio, bonif, neto = num(p[2]), num(p[4]), num(p[5]), num(p[6])
                renglones.append(dict(doc=doc, fecha=fecha, renglon=int(p[0]), producto=prod, cantidad=cant,
                                      presentacion=p[3], precio=precio, bonif=bonif, neto=neto, archivo=os.path.basename(f)))
    return cat, rend, recetas, renglones

def precios(cat, renglones, fecha):
    """Precio por unidad base: última factura <= fecha; a igual fecha, comprobante mayor."""
    out = {}
    for r in renglones:
        if r['fecha'] > fecha: continue
        k = (r['fecha'], r['doc'])
        if r['producto'] not in out or k > out[r['producto']][0]:
            eq = r['cantidad'] * cat[(r['producto'], r['presentacion'])]
            out[r['producto']] = (k, r['neto'] / eq, r)
    return {p: v[1] for p, v in out.items()}, {p: v[2] for p, v in out.items()}

def costo(cod, recetas, rend, precio):
    """Costo de la receta completa (su rendimiento declarado)."""
    total = D(0)
    for ing in recetas[cod]['ingredientes']:
        p, q, est = ing['producto'], D(str(ing['cantidad'])), ing['estado']
        if p in recetas:  # preparación: se mide sobre la tanda terminada
            sub = recetas[p]
            total += costo(p, recetas, rend, precio) / D(str(sub['rendimiento'])) * q
            continue
        lb, cl = rend[p]
        bruto = {'bruto': q, 'limpio': q / lb, 'cocido': q / (lb * cl)}[est]
        total += bruto * precio[p]
    return total

if __name__ == '__main__':
    base, fecha, salida = sys.argv[1:4]
    cat, rend, recetas, renglones = cargar(base)
    precio, _ = precios(cat, renglones, fecha)
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    with open(salida, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n'); w.writerow(['plato', 'costo_por_porcion'])
        for cod, r in recetas.items():
            if r['unidad_rendimiento'] != 'porción': continue
            c = costo(cod, recetas, rend, precio) / D(str(r['rendimiento']))
            w.writerow([cod, str(c.quantize(D('0.01'), rounding=ROUND_HALF_UP))])
            print(cod, c, file=sys.stderr)
