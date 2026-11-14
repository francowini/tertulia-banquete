"""Nivel 4 · costo de reposición al 31/10/2026.
Precio efectivo de cierre (última compra <= 31/10 con notas de crédito, igual que N2/N3, incluye compras OCR locales del N3).
Productos cuya última compra es del Frigorífico del Muelle: precio efectivo x 1,18 (después de bonificaciones). Resto: igual.
Uso: python3 -I nivel-4/codigo/reposicion.py <material n2> <compras_ocr.csv> <notas_ocr.csv> <carta.json> <margenes N3> <salida.csv>"""
import csv, json, sys, os, re, glob
from decimal import Decimal as D
sys.path.insert(0, os.path.dirname(__file__))
import costeo, margenes

def proveedor_doc(n2, compras):
    prov = {}
    for f in glob.glob(f'{n2}/facturas/*'):
        t = costeo.texto(f)
        prov[re.search(r'Factura\s+(F-\w+)', t).group(1)] = t.strip().splitlines()[0].strip()
    ocr = os.path.join(os.path.dirname(compras), 'ocr')
    for r in csv.DictReader(open(compras, encoding='utf-8')):
        t = open(os.path.join(ocr, os.path.splitext(os.path.basename(r['archivo']))[0] + '.txt'), encoding='utf-8').read().lower()
        prov.setdefault(r['doc'], 'Frigorífico del Muelle' if 'muelle' in t else 'otro')
    return prov

def main(n2, compras, notas_p, carta_p, marg_p, out):
    cat, rend, recetas, reng, notas = costeo.cargar(n2)
    r3, n3n = margenes.leer_extra(compras, notas_p, cat)
    reng += r3; notas += n3n
    prov = proveedor_doc(n2, compras)
    precio, traza = costeo.precios(cat, reng, notas, '2026-10-31')
    muelle = {p for p, t in traza.items() if 'Muelle' in prov[t['factura']]}
    repo = {p: (v * D('1.18') if p in muelle else v) for p, v in precio.items()}
    carta = json.load(open(carta_p, encoding='utf-8'))
    marg = {r['plato']: r for r in csv.DictReader(open(marg_p, encoding='utf-8'))}
    def prods(c, acc):
        for i in recetas[c]['ingredientes']:
            (prods(i['producto'], acc) if i['producto'] in recetas else acc.add(i['producto']))
        return acc
    with open(out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['plato','nombre','precio_carta','costo_cierre','costo_reposicion','margen_reposicion','unidades_trim','ingreso_trim','margen_trim','casa','veg','sin_tacc','subrecetas','productos_muelle','productos'])
        for c in carta:
            p = c['plato']; r = D(str(recetas[p]['rendimiento']))
            cc = costeo.costo(p, recetas, rend, precio) / r; cr = costeo.costo(p, recetas, rend, repo) / r
            pc = D(str(c['precio_carta'])); m = marg[p]; ps = sorted(prods(p, set()))
            w.writerow([p, c['nombre'], pc, f'{cc:.2f}', f'{cr:.2f}', f'{(pc-cr)/pc:.6f}', m['unidades_vendidas'], m['ingreso_neto'], m['margen'],
                        int(c['plato_de_la_casa']), int(c['vegetariano']), int(c['sin_tacc']), '+'.join(c['preparaciones']),
                        '+'.join(x for x in ps if x in muelle), '+'.join(ps)])
    print('Muelle:', sorted(muelle), file=sys.stderr)
    print('Muelle docs cierre:', {p: traza[p]['factura'] for p in sorted(muelle)}, file=sys.stderr)

if __name__ == '__main__':
    main(*sys.argv[1:7])
