# Informe para Mora · Revisión del retiro de P12 y oferta de soja

Plato revisado: P12
Sustitución propuesta: rechazada
Decisión: se sostiene el retiro de P12, con conversación previa con cocina y fecha de revisión

## 1. Recomendación en una frase

Sostenemos retirar **Pollo del aljibe (P12)**: los registros de caja y de compras no muestran los números de Bruno, y con los números verificados P12 sigue entre los 10 platos no protegidos de menor contribución [nivel-4/criterio.md#L45]. Rechazamos el cambio de pollo por soja en P01 tal como llegó, porque agrega un alérgeno (soja) que la carta no declararía [nivel-5/oferta-almacen.md#L9] [nivel-4/carta.json#L9].

## 2. Tres tipos de números (cómo leer este informe)

| Tipo | Qué es | Ejemplos en este informe |
|---|---|---|
| **Registro** | Dato tal como figura en un documento del restaurante | ventas en caja, facturas, precio de carta, aviso del frigorífico, oferta del almacén |
| **Cálculo** | Resultado aritmético reproducible a partir de registros | costo por porción, unidades netas, margen, contribución |
| **Proyección / hipótesis** | Lo que podría pasar; no está registrado | cuántos clientes de P12 pasan a otro plato, cuánto se vendería de un plato nuevo, ahorro futuro con soja |

## 3. Los argumentos de Bruno, uno por uno

### 3.1 "Cuesta $ 1605 por porción con precios de hoy" [nivel-5/mensaje-chef.md#L5]

- **Registro:** receta de P12 (150 g cocidos de pollo C01 + subrecetas S02, S09, S15 + otros insumos) [nivel-2/recetas.json#L439] [nivel-4/carta.json#L206]; compras hasta el 31/10 (facturas PDF del nivel 2 y fotos manuscritas del nivel 3, leídas con OCR local) [nivel-3/compras_ocr.csv]; aviso del Frigorífico del Muelle: +18 % sobre la última compra [nivel-4/aviso-proveedor.md#L3].
- **Cálculo:** costo de cierre al 31/10 = **$ 3.101,67** [nivel-3/costos.csv#L13]. Con +18 % en los productos del frigorífico (en P12 solo C01) el costo de reposición es **$ 3.566,19** [nivel-4/analisis.csv#L13].
- Cómo se comprueba: para cada insumo, cantidad de receta ÷ rendimientos (limpio/bruto y cocido/limpio) [nivel-2/rendimientos.csv] × precio efectivo de la última compra (neto impreso ÷ cantidad, con notas de crédito que aplican) [nivel-2/procedimientos.md]; las subrecetas se dividen por su tanda. El pollo pesa más que nada: 150 g cocidos de C01 son ≈ 260 g comprados; a precio de cierre $ 2.355,49 y a reposición $ 2.779,48 por porción (150 g ÷ 0,78 ÷ 0,74 × $ 10,6954/g). Solo ese renglón ya supera los $ 1605.
- **De dónde sale 1605 (registro):** es el **código de artículo de caja** de otro plato, Tostón de bondiola (P16): `A1605` [nivel-3/caja/articulos.csv#L25]. El artículo de P12 es `A1577` [nivel-3/caja/articulos.csv#L19]. Ninguna combinación de compras da $ 1605 para P12 con el aumento. No lo usamos como costo.

### 3.2 "Salieron 986 porciones netas en ago–oct" [nivel-5/mensaje-chef.md#L5]

- **Registro:** caja de agosto, septiembre y octubre [nivel-3/caja/2026-08.csv] [nivel-3/caja/2026-09.csv] [nivel-3/caja/2026-10.csv], con las reglas del manual de caja [nivel-3/caja/manual.md]: ventas (VTA) menos reversiones (REV), propinas (EXT) fuera, componentes de combos sí cuentan.
- **Cálculo:** **343 unidades netas** de P12, ingreso neto **$ 2.477.280,00**, margen histórico 0,679097 [nivel-3/margenes.csv#L13]. Este cálculo fue reproducido por un recálculo independiente con otro script (50/50 idéntico).
- **Cálculo de control:** P12 (A1577) tiene 441 unidades vendidas (VTA) − 98 revertidas (REV) = 343; no está en ningún combo [nivel-3/caja/combos.csv]. Ni sumando reversiones se llega a 986 (daría 539).
- **De dónde sale 986 (registro + cálculo):** coincide casi exacto con las ventas netas de **P16 Tostón de bondiola**, 987 unidades (1290 VTA − 303 REV) [nivel-3/margenes.csv#L17]. Los dos números de Bruno parecen leídos de la fila del artículo A1605 / P16, no de P12. Lo revisamos con él mirando la planilla juntos (próximo paso 1).

### 3.3 "Con ese costo y esas ventas no hay razón económica para sacarlo"

- **Cálculo con números verificados:** contribución a costo de reposición = 343 × ($ 8.000 − $ 3.566,19) = **$ 1.520.797** [nivel-4/decisiones.json#L72]. Regla aplicada igual a los 45 platos no protegidos: salen los 10 de menor contribución [nivel-4/criterio.md#L31]. P12 queda en ese grupo.
- **Cálculo con los números de Bruno (solo para mostrar la sensibilidad):** 986 × ($ 8.000 − $ 1.605) = $ 6.305.370. Con esos números P12 no se retiraría. Por eso la discusión es sobre los datos de origen, y no sobre la regla: si la caja o las compras estuvieran mal, la decisión cambia.
- Esta contribución es un **recálculo** de ventas pasadas con costo nuevo: es un indicador para comparar platos, **no una ganancia realizada** ni una venta futura.

### 3.4 "El aumento de un proveedor no vuelve todo un problema; compramos muchas cosas que no son de él"

- Es correcto y así se calculó: el +18 % se aplicó **solo** a C01–C08 del Frigorífico; los demás insumos conservan su precio de cierre [nivel-4/criterio.md]. En P12 el único insumo alcanzado es el pollo C01 [nivel-4/analisis.csv#L13]. Su margen a precio de carta pasa a 0,5542: no queda bajo el mínimo de 0,50; P12 sale por contribución (pocas unidades), no por el aumento.

### 3.5 Preparaciones compartidas, trabajo de cocina y clientes que vuelven

- **Registro:** P12 usa S02, S09 y S15 [nivel-4/carta.json#L206]. Ninguna subreceta queda sin uso al retirar los 10 platos [nivel-4/decisiones.json#L72]; lo preparado se sigue usando en otros platos.
- **No medido:** tiempos de cocina, cuellos de botella en servicio y fidelidad de clientes. No tenemos esos datos y **no los inventamos**. Bruno tampoco tiene encuesta. Proponemos medirlo (próximos pasos) en lugar de suponerlo.
- **Hipótesis (no registro):** no sabemos cuántos de los 343 pedidos de P12 pasan a otro plato o se pierden.

## 4. Oferta del almacén y pedido de cambiar pollo por soja en P01

- **Registro:** A09 bocados de soja cocidos, bolsa 1000 g a $ 2.400, rendimientos 1 y 1, alérgeno **soja** [nivel-5/oferta-almacen.md#L5] [nivel-5/oferta-almacen.md#L7] [nivel-5/oferta-almacen.md#L9]. P01 declara solo **gluten** [nivel-4/carta.json#L9]. El pedido es dejar mismo nombre, descripción y alérgenos y no avisar al salón [nivel-5/mensaje-chef.md#L21].
- **Cálculo:** 160 g × $ 2,40/g = $ 384 por porción, contra $ 2.964,78 del pollo a reposición en P01 ($ 2.512,53 a cierre) [nivel-2/codigo/desglose.csv#L2] [nivel-4/analisis.csv#L2]. Costo P01 con soja = $ 3.697,17 − $ 2.964,78 + $ 384,00 = **$ 1.116,39**; margen a $ 9.900 = 0,887234 (hoy 0,626549).
- **Por qué se rechaza:** (1) la carta seguiría declarando solo gluten con un ingrediente que contiene soja: riesgo directo para un cliente alérgico; (2) "Pollo al limón" sin pollo engaña al cliente; (3) P01 es plato de la casa y ya cumple el mínimo: margen 0,6265 a reposición sin tocar nada [nivel-4/decisiones.json]. No hace falta recuperar margen ahí.
- **Proyección (no registro):** el ahorro de $ 2.580,78 por porción solo existiría si se vende lo mismo, cosa que no sabemos. Si el equipo quiere un plato con soja, debe ser un plato **nuevo**, con nombre propio, soja declarada, salón avisado y prueba previa; se evalúa aparte y no prometemos ventas.

## 5. Efecto del aviso comercial (Frigorífico del Muelle)

- **Registro:** +18 % para reponer desde el 31/10, sobre el precio efectivo de la última compra [nivel-4/aviso-proveedor.md#L3].
- **Cálculo:** 49 de 50 platos usan productos del frigorífico; el costo sube 4 %–17 % [nivel-4/criterio.md]. En P12: de $ 3.101,67 a $ 3.566,19 (+15,0 %).
- La oferta del almacén dice expresamente que no cambia con esa lista y que no modifica compras anteriores [nivel-5/oferta-almacen.md].

## 6. Qué se sostiene y qué se revisa

- **Se sostiene:** la regla y la carta aprobadas en el nivel 4, sin cambios en sus archivos.
- **Se revisa el proceso:** la decisión no se aplica "porque lo dijo el análisis" sino después de una reunión con cocina, con los papeles en la mesa.

## 7. Próximos pasos

1. Reunión Mora + Bruno + cocina antes del próximo servicio: revisar juntos la caja de P12 (343 vs 986) y el costo (factura del pollo usada y aumento del 18 %).
2. Si aparece un error en caja o compras, se recalcula con la misma regla y se publica la corrección.
3. Comunicación: Bruno y el equipo eligen cómo avisar a clientes habituales de P12 y qué plato sugerir en su lugar.
4. Lo preparado (S02, S09, S15) se sigue usando en los platos que continúan.
5. Prueba en servicio de tiempos de cocina durante 2 semanas, medida en comandas.
6. Revisión de la carta a los 30 días con datos de caja del nuevo período.
