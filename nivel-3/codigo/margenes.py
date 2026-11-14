"""Nivel 3: costos al 31/10/2026 y márgenes del trimestre ago-oct 2026.

Uso: python3 -I margenes.py <material_n2> <material_n3> <compras_ocr.csv> <notas_ocr.csv|-> <dir_salida>

- Compras = facturas y notas del nivel 2 (PDF) + compras nuevas transcriptas por OCR local
  (nivel-3/codigo/ocr.swift -> nivel-3/compras_ocr.csv, revisado con controles aritméticos).
- costos.csv: mismo método que el nivel 2 (última factura <= 31/10 por producto + notas asociadas).
- margenes.csv: cada VTA/COM se costea con los precios vigentes a SU fecha (última compra <= fecha de
  la venta y notas emitidas <= esa fecha). REV anula su movimiento original (mismo reparto y costo).
  EXT (propinas) no son ingreso de platos. COM: cobro neto (bruto - descuento) repartido por peso_ingreso,
  sin redondear; costo y unidades según unidades por combo.
"""
import csv, sys, os
from decimal import Decimal as D, ROUND_HALF_UP
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import costeo

def leer_extra(path_c, path_n, cat):
    reng, notas = [], []
    for r in csv.DictReader(open(path_c, encoding='utf-8')):
        assert (r['producto'], r['presentacion']) in cat, r
        reng.append(dict(doc=r['doc'], fecha=r['fecha'], renglon=int(r['renglon']), producto=r['producto'],
                         presentacion=r['presentacion'], cantidad=D(r['cantidad']), precio=D(r['precio']),
                         bonif=D(r['bonif'] or 0), neto=D(r['neto']), archivo=r['archivo']))
    if path_n and path_n != '-' and os.path.exists(path_n):
        for r in csv.DictReader(open(path_n, encoding='utf-8')):
            notas.append(dict(nota=r['nota'], fecha=r['fecha'], doc=r['doc'], renglon=int(r['renglon']),
                              producto=r['producto'], concepto=r['concepto'].lower(), cantidad=D(r['cantidad'] or 0),
                              unidad=r['unidad'], importe=D(r['importe']), archivo=r['archivo']))
    return reng, notas

def q2(x): return x.quantize(D('0.01'), rounding=ROUND_HALF_UP)

def main(n2, n3, compras, notas_p, out):
    cat, rend, recetas, reng, notas = costeo.cargar(n2)
    r3, n3n = leer_extra(compras, notas_p, cat)
    reng += r3; notas += n3n
    platos = [c for c, r in recetas.items() if r['unidad_rendimiento'] == 'porción']
    memo_fecha = {}
    def costo_porcion(fecha):
        if fecha not in memo_fecha:
            precio, _ = costeo.precios(cat, reng, notas, fecha)
            memo = {}
            memo_fecha[fecha] = {p: costeo.costo(p, recetas, rend, precio, memo) / D(str(recetas[p]['rendimiento'])) for p in platos}
        return memo_fecha[fecha]
    os.makedirs(out, exist_ok=True)
    cierre = costo_porcion('2026-10-31')
    with open(f'{out}/costos.csv', 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n'); w.writerow(['plato', 'costo_por_porcion'])
        for p in platos: w.writerow([p, str(q2(cierre[p]))])
    caja = f'{n3}/caja'
    art = {a['articulo']: a for a in csv.DictReader(open(f'{caja}/articulos.csv', encoding='utf-8'))}
    combos = {}
    for c in csv.DictReader(open(f'{caja}/combos.csv', encoding='utf-8')):
        combos.setdefault(c['combo'], []).append((c['plato'], D(c['unidades']), D(c['peso_ingreso'])))
    movs = []
    for m in ('2026-08', '2026-09', '2026-10'):
        movs += list(csv.DictReader(open(f'{caja}/{m}.csv', encoding='utf-8')))
    byid = {r['id']: r for r in movs}
    agg = {p: dict(u=D(0), ing=D(0), cos=D(0)) for p in platos}
    for r in movs:
        if r['tipo'] not in ('VTA', 'COM', 'REV'): continue      # EXT: propina, no es facturación de platos
        orig = byid[r['referencia']] if r['tipo'] == 'REV' else r
        signo = -1 if r['tipo'] == 'REV' else 1
        fecha = orig['fecha_hora'][:10]                         # REV conserva costo de la venta original
        cant = D(orig['cantidad']); neto = D(orig['importe_bruto']) - D(orig['descuento'])
        cp = costo_porcion(fecha)
        if orig['tipo'] == 'VTA':
            a = art[orig['articulo']]; assert a['desde'] <= fecha <= a['hasta'], orig
            comps = [(a['plato'], D(1), D(1))]
        else:
            comps = combos[orig['articulo']]
        tot_peso = sum(c[2] for c in comps)
        for plato, unid, peso in comps:
            g = agg[plato]
            g['u'] += signo * cant * unid
            g['ing'] += signo * neto * peso / tot_peso
            g['cos'] += signo * cant * unid * cp[plato]
    with open(f'{out}/margenes.csv', 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n'); w.writerow(['plato', 'unidades_vendidas', 'ingreso_neto', 'costo', 'margen'])
        for p in platos:
            g = agg[p]; ing, cos = q2(g['ing']), q2(g['cos'])
            mg = D(0) if g['ing'] == 0 else (g['ing'] - g['cos']) / g['ing']
            w.writerow([p, str(int(g['u'])), f'{ing:.2f}', f'{cos:.2f}', f'{mg.quantize(D("0.000001"), rounding=ROUND_HALF_UP):.6f}'])

if __name__ == '__main__':
    main(*sys.argv[1:6])
