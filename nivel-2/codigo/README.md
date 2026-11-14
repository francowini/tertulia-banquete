# Nivel 2 · Costeo de la carta completa

Programa: `costeo.py` (Python 3, solo librería estándar + `pdftotext` de poppler para leer los PDF).

```
python3 -I costeo.py <material> 2026-10-31 ../costos.csv precios_usados.csv
```

## Entradas (en `<material>`, el zip del nivel 2)
- `recetas.json`: 50 platos (rendimiento 1 porción) y 15 subrecetas S01–S15 (rendimiento = tamaño de tanda en g o ml). Hay subrecetas que usan otras subrecetas (S06→S05→S04, S14→S13→S01/S02, etc.).
- `catalogo.csv`: equivalencia de cada presentación de compra de cada producto en g, ml o unidades.
- `rendimientos.csv`: coeficientes limpio/bruto y cocido/limpio por producto.
- `facturas/F-001…F-040.pdf`: 8 renglones cada una. **Cada proveedor ordena distinto las columnas**, por eso el orden se lee del encabezado de la tabla de cada factura (`orden_columnas`). Además se controla que la suma de netos dé el TOTAL impreso.
- `notas/NC-001…NC-004.pdf`: notas de crédito que ajustan una factura y un renglón.

## Cálculo
1. **Precio por producto** (`precios`): se toma el renglón de la última factura con fecha ≤ 31/10/2026; si hay empate de fecha, el identificador de factura mayor.
2. **Notas** emitidas hasta la fecha de costeo que apuntan a ese documento y renglón:
   - una *bonificación* resta importe y deja igual la cantidad;
   - una *devolución* resta importe y unidades (convertidas con el catálogo).

   No son compras nuevas. Hoy aplican NC-003 (A03, F-039 r3) y NC-004 (L05, F-040 r5). NC-001 y NC-002 ajustan facturas que no son la última de su producto, así que no cambian el precio.
3. **Precio efectivo** = neto ajustado ÷ cantidad equivalente en unidad base.
4. **Cantidad bruta** por estado del ingrediente: bruto = q; limpio = q ÷ (limpio/bruto); cocido = q ÷ (limpio/bruto × cocido/limpio).
5. **Subrecetas** (`estado: preparado`): costo de la tanda ÷ rendimiento de la tanda × cantidad usada. Es recursivo y está memoizado. El agua no tiene costo.
6. **Sin redondeos intermedios** (Decimal exacto). El costo por porción se redondea a 2 decimales, con la mitad hacia arriba. Las subrecetas no se escriben como filas.

## Trazabilidad
`precios_usados.csv` muestra, para cada producto, de dónde sale su número: la factura, la fecha y el renglón, el neto ajustado, la cantidad en unidad base, las notas aplicadas y el precio por unidad base.
