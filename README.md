# El banquete · Aristóteles (Tertulia · Juegos Olímpicos AI)

Costeo de platos de El Término Medio, reproducible por script.

- `src/costeo.py`: lee recetas, catálogo, rendimientos y facturas; precio efectivo = neto del renglón / cantidad equivalente (última factura ≤ fecha, a igual fecha el comprobante mayor); pasa cocido/limpio a bruto; preparaciones por tanda; sin redondeos intermedios, redondeo final HALF_UP a 2 decimales.
- Nivel 1: `python3 -I src/costeo.py <material> 2026-08-10 nivel-1/costos.csv`
