"""Nivel 4 · aplica el criterio a toda la carta y escribe nivel-4/decisiones.json.
Uso: python3 -I nivel-4/codigo/decidir.py <analisis.csv> <M> <regla_retiro: margen|contribucion> <salida.json>
- Protegidos (no se retiran): platos de la casa, vegetarianos y sin TACC (única opción de su tipo).
- Retiro: 10 platos no protegidos con menor margen de reposición (regla 'margen') o menor contribución
  del trimestre a costo de reposición = unidades × (precio carta − costo reposición) (regla 'contribucion').
- Continúan: si margen de reposición a precio de carta >= M → mantener; si no → subir al menor múltiplo de $100
  que deja margen >= M con colchón de 1 % sobre el costo (precio >= costo×1,01/(1−M))."""
import csv, json, sys, math
from decimal import Decimal as D

def main(an, M, regla, out):
    M = D(M); R = list(csv.DictReader(open(an, encoding='utf-8')))
    for r in R:
        r['pc'] = D(r['precio_carta']); r['cr'] = D(r['costo_reposicion'])
        r['mg'] = (r['pc'] - r['cr']) / r['pc']; r['u'] = int(r['unidades_trim'])
        r['contrib'] = r['u'] * (r['pc'] - r['cr'])
        r['prot'] = [t for t, k in (('plato de la casa', 'casa'), ('única opción vegetariana', 'veg'), ('única opción sin TACC', 'sin_tacc')) if r[k] == '1']
    clave = (lambda r: (r['mg'], r['plato'])) if regla == 'margen' else (lambda r: (r['contrib'], r['plato']))
    sacar = {r['plato'] for r in sorted([r for r in R if not r['prot']], key=clave)[:10]}
    dec = []
    for r in R:
        base = (f"Costo de reposición ${r['cr']:.2f} (Frigorífico +18%: {r['productos_muelle'] or 'no usa'}); "
                f"margen a precio de carta ${r['pc']:.0f}: {r['mg']:.4f}; ventas ago–oct: {r['u']} u, "
                f"contribución recalculada (no realizada) de esas ventas a costo de reposición ${r['contrib']:,.0f}.")
        if r['plato'] in sacar:
            d, p = 'sacar', None
            pos = sorted([x for x in R if not x['prot']], key=clave).index(r) + 1
            f = (f"Se retira: puesto {pos} de 10 entre los no protegidos por menor {'margen' if regla=='margen' else 'contribución'}. " + base +
                 f" Resignamos sus {r['u']} u del trimestre (no sabemos cuántos clientes pasan a otro plato: hipótesis); ganamos una carta más corta sin bajar del mínimo y sin perder subrecetas ni alternativas por alérgeno.")
        elif r['mg'] >= M:
            d, p = 'mantener', float(r['pc'])
            f = (f"Se mantiene: margen {r['mg']:.4f} ≥ mínimo {M}. " + base + (f" Protegido: {', '.join(r['prot'])}." if r['prot'] else '') +
                 " Ganamos: sigue su aporte sin tocar el precio. Resignamos: absorbe el +18% con menos margen que antes del aviso.")
        else:
            p = D(math.ceil(r['cr'] * D('1.01') / (1 - M) / 100) * 100); d = 'subir'
            f = (f"Sube de ${r['pc']:.0f} a ${p:.0f} (+{(p/r['pc']-1)*100:.1f}%): margen nuevo {(p-r['cr'])/p:.4f} ≥ {M}. " + base +
                 (f" Protegido: {', '.join(r['prot'])}." if r['prot'] else '') + " Ganamos: vuelve al mínimo sin retirarlo. Resignamos: posible baja de ventas por el aumento (hipótesis no verificada, sin datos de elasticidad).")
            p = float(p)
        if p is not None: assert (D(str(p)) - r['cr']) / D(str(p)) >= M
        dec.append(dict(plato=r['plato'], decision=d, precio_nuevo=p, fundamento=f))
    assert len(dec) == 50 and sum(x['decision'] == 'sacar' for x in dec) == 10
    json.dump(dec, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for x in dec:
        if x['decision'] != 'mantener': print(x['plato'], x['decision'], x['precio_nuevo'])

if __name__ == '__main__':
    main(*sys.argv[1:5])
