# Nivel 3 · Compras, caja y márgenes

Entregables: `nivel-3/costos.csv` (costo por porción al 31/10/2026) y `nivel-3/margenes.csv`
(`plato,unidades_vendidas,ingreso_neto,costo,margen`, trimestre 01/08–31/10/2026).

## Cómo se reproduce
```
swift nivel-3/codigo/ocr.swift <imágenes>          # OCR LOCAL (Apple Vision, offline) -> nivel-3/ocr/*.txt
python3 -I nivel-3/codigo/margenes.py material/nivel-2/archivos/nivel-2 material/nivel-3/archivos/nivel-3 \
        nivel-3/compras_ocr.csv nivel-3/notas_ocr.csv nivel-3
```
(`material/` no se sube: son los archivos de la organización. Tampoco se suben imágenes ni caja.)

## Compras
- Se conservan las facturas y notas de crédito del nivel 2 y se suman las compras nuevas de `facturas/` y `tickets/`.
- Las fotos se transcriben con OCR local (`codigo/ocr.swift`, framework Vision de macOS, sin red).
  El texto crudo queda en `ocr/` y los renglones estructurados en `compras_ocr.csv`, validados con
  cantidad × precio × (1 − bonificación) = neto y suma de netos = total.
- Método igual al nivel 2: por producto, la última compra disponible (fecha ≤ referencia; empate: documento mayor),
  ajustada por sus notas de crédito emitidas hasta esa fecha.

## Caja (convenciones del manual)
- `VTA`: plato según el maestro de artículos (código y vigencia; extremos inclusivos).
- `COM`: el cobro neto (bruto − descuento) se reparte entre los componentes en proporción a `peso_ingreso`,
  sin redondeo previo; unidades y costo = cantidad × unidades por combo.
- `REV`: anula íntegramente su movimiento original (resta las mismas unidades, el mismo reparto y el mismo costo
  histórico de la venta original). No se borra el original además.
- `EXT` (propinas): no es facturación de platos, se excluye.
- Costo de cada venta: precios de la última compra disponible a la fecha de esa venta (con sus notas emitidas
  hasta esa fecha), no el costo de cierre.
- Margen = (ingreso − costo) / ingreso con 6 decimales (0.000000 si el ingreso es 0). Importes con 2 decimales.
