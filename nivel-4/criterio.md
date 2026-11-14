# Nivel 4 · Criterio para la carta de 40 platos

Margen mínimo: 0.500000

## 1. Situación y método de costo

- **Aviso del Frigorífico del Muelle (31/10/2026):** sus productos cuestan 18 % más para reponer. Se aplica sobre el precio efectivo de la última compra, después de bonificaciones.
- **Productos alcanzados:** C01 pollo, C02 carne para brasear, C03 bondiola, C04 merluza, C05 panceta, C06 chorizo, C07 atún y C08 jamón. En los ocho, la compra de cierre (≤ 31/10) es del Frigorífico: facturas F-038 y M-010 y ticket T-014.
- **Costo de reposición:** precio efectivo de cierre × 1,18 para esos ocho productos. Los demás conservan su precio efectivo de cierre, con notas de crédito, como en los niveles 2 y 3. Las recetas, subrecetas, rendimientos y estados son los del nivel 2. Las compras manuscritas son las del nivel 3, leídas con OCR local.
- **Control:** sin el 18 % el cálculo reproduce exacto `nivel-3/costos.csv`. La valoración histórica de ventas (`nivel-3/margenes.csv`) no se modifica: solo la usamos como dato de lo que ya se vendió.
- **Impacto:** 49 de 50 platos usan algún producto del Frigorífico. Su costo por porción sube entre 4 % y 17 %. El único que no cambia es P48 (Bowl de la huerta).
- **Margen a precio de carta actual:** va de 0,4668 (P33) a 0,6892 (P34).
- **Código:** `nivel-4/codigo/reposicion.py` calcula los costos y escribe `nivel-4/analisis.csv`. `nivel-4/codigo/decidir.py` aplica esta regla a los 50 platos y escribe `decisiones.json`.

## 2. Por qué el mínimo es 0,50

El margen es de ingredientes: `(precio_nuevo − costo_actualizado) / precio_nuevo`. Exigimos que como mínimo la mitad del precio quede después de pagar ingredientes a costo de reposición.

Por qué 0,50:
- **Es alcanzable sin cambios bruscos.** Con el costo nuevo, 40 de los 50 platos ya llegan a 0,50 al precio actual. Los que quedan y no llegan se corrigen con aumentos de 3,6 % a 7,0 %.
- **Las alternativas exigían mucho más.** Con 0,55, los aumentos llegarían al 16 %. Con 0,60, habría que subir 30 platos. Como no tenemos datos de elasticidad ni de aceptación de precios, preferimos aumentos chicos.
- **Deja lugar para lo que el margen no mide:** personal, energía, alquiler y mermas no previstas. Ninguno entra en este margen, que es solo de ingredientes.
- **Mantiene una referencia conocida.** Antes del aviso, con los costos de cierre, ningún plato quedaba por debajo de 0,54. El mínimo de 0,50 absorbe el golpe del proveedor sin trasladarlo completo al cliente.

## 3. Regla de decisión, aplicada igual a los 50 platos

1. **Platos protegidos (no se retiran).** Son los que cumplen una función que ningún otro plato cubre:
   - de la casa, por identidad: P01, P11 y P25;
   - única opción vegetariana: P48;
   - única opción sin TACC, con circuito dedicado: P50.
2. **Retiros.** Entre los 45 no protegidos salen los 10 con menor contribución del trimestre a costo de reposición. Contribución = unidades vendidas netas ago–oct (de caja, nivel 3) × (precio de carta − costo de reposición). Es el aporte en pesos que el plato habría dejado con el costo nuevo y el volumen ya vendido. Las unidades son ventas reales. La contribución es un recálculo de esas ventas con costo de reposición: es un indicador para comparar platos, no una ganancia realizada. La valoración histórica real está en `nivel-3/margenes.csv`.
3. **Platos que continúan.**
   - Si su margen al precio de carta es ≥ 0,50: se **mantiene** el precio.
   - Si no: se **sube** al menor múltiplo de $100 que deja margen ≥ 0,50 con un colchón del 1 % sobre el costo, es decir precio ≥ costo × 1,01 / 0,50.

### Resultado

**Retiros (10):**

| Plato | Unidades ago–oct | Margen de reposición |
|---|---|---|
| P23 Pescado del muelle | 351 | 0,474 |
| P47 Arroz costero | 362 | 0,476 |
| P37 Arroz de la galería | 331 | 0,555 |
| P12 Pollo del aljibe | 343 | 0,554 |
| P45 Ñoquis con pollo | 336 | 0,599 |
| P31 Arroz del domingo | 497 | 0,630 |
| P34 Panqueque del salón | 366 | 0,689 |
| P33 Merluza al limón | 832 | 0,467 |
| P38 Pollo con salsa blanca | 1.057 | 0,480 |
| P36 Timbal de atún | 649 | 0,633 |

Entre los diez suman 5.124 unidades, el 8,4 % de las 61.139 del trimestre, y $22,9 M de contribución a costo de reposición, el 6,3 % de $364,0 M.

**Aumentos (6):**

| Plato | Precio actual | Precio nuevo | Aumento |
|---|---|---|---|
| P08 Merluza con crema | 9.400 | 9.900 | +5,3 % |
| P13 Pastel de carne | 11.100 | 11.800 | +6,3 % |
| P18 Lentejas de invierno | 5.200 | 5.500 | +5,8 % |
| P28 Lentejas con bondiola | 6.200 | 6.600 | +6,5 % |
| P42 Cazuela de septiembre | 5.300 | 5.500 | +3,8 % |
| P43 Arroz cremoso con jamón | 5.600 | 5.800 | +3,6 % |

**Se mantienen (34):** los demás, todos con margen ≥ 0,5167 al precio actual. El menor margen de toda la carta nueva es 0,5077 (P08).

## 4. Condiciones de operación: qué más se mueve con cada retiro

- **Subrecetas.** Las 15 subrecetas (S01–S15) siguen en uso en la carta de 40, así que no se desarma ninguna preparación de cocina:
  - S12 queda solo en P46, porque sale P33;
  - S07 queda en P04, P14 y P30;
  - S03 queda en P10 y P27;
  - S09 queda en P05 y P15.
  
  Hay dos insumos que quedan en un solo plato, y lo aceptamos como consecuencia:
  - el atún (C07) queda solo en P15, porque sale P36;
  - el aliño de limón (S12) queda solo en P46, porque sale P33.
  
  Como la carta mantiene el mismo set de bases, el trabajo de mise en place no crece. Baja la cantidad de variantes finales para el pase. Las 50 fichas son de cocina caliente, así que no hay una estación que quede vacía o sobrecargada.
- **Insumos compartidos.** Los ocho productos del Frigorífico siguen en uso en varios platos, así que no queda stock sin destino. La compra de merluza, atún, pollo y jamón baja en volumen, pero no se discontinúa.
- **Alérgenos (conteo de platos, carta actual → carta de 40).**
  - Sin gluten: 2 → 2 (P48 y P50).
  - Sin leche: 8 → 7 (sale P45).
  - Sin huevo: 41 → 33.
  - Sin pescado: 41 → 35.
  
  Todas las alternativas para cada alérgeno siguen en la carta.
- **Trabajo de cocina.** Las fichas no traen tiempos ni carga por plato, y no hay costos de personal. Por eso el trabajo de cocina se mide solo por lo que se puede ver en las fichas: estación y subrecetas compartidas. Es una limitación del dato, no una conclusión.
- **Condiciones alimentarias.**
  - Siguen la opción vegetariana (P48) y la sin TACC (P50). P48 no tiene ingredientes con gluten, pero no está declarado sin TACC: el único con circuito dedicado es P50.
  - Con pescado quedan cinco platos: P08, P15, P17, P44 y P50.
  - Con arroz quedan P05, P15, P43 y P21.
  - No se pierde ninguna categoría de la carta.

## 5. Qué ganamos y qué resignamos (consecuencias aceptadas)

**Ganamos:**
- Una carta de 40 donde cada plato deja al menos 0,50 de margen de ingredientes a costo de reposición.
- Solo 6 aumentos, todos de 7 % o menos.
- Se conservan los platos de la casa y las dos opciones para condiciones alimentarias.
- Salen los platos de menor aporte. Siete de los diez vendían menos de 500 unidades en el trimestre.

**Resignamos:**
- El 6,3 % de la contribución recalculada (no realizada) del trimestre y el 8,4 % de las unidades. Parte de esos clientes podría pasarse a otro plato, pero eso es una **hipótesis**, no una venta realizada.
- Retiramos platos con margen alto pero poco volumen, como P34 (0,689) y P31 (0,630), porque aportan poco en pesos.
- Mantenemos P48, que tiene una contribución baja, por ser la única opción vegetariana.
- Los aumentos pueden reducir las ventas de esos 6 platos. No tenemos datos de elasticidad, así que no lo estimamos. Con el colchón del 1 %, cada uno sigue sobre 0,50 aunque su costo suba hasta 1 % más.

**Qué tan firme es el corte:** el 10.º retirado (P36, $3,45 M) y el 11.º (P17, $3,49 M) están separados por apenas 1,3 %. La regla los ordena igual, pero con otro volumen podrían intercambiarse.

**Por qué ordenar por contribución y no por margen:** el margen en porcentaje se corrige con precio, como muestran los 6 aumentos. Lo que un plato aporta en pesos depende de cuánto se vende, y eso no se corrige subiendo el precio. Por eso retiramos lo que menos aporta y ajustamos el precio de lo que aporta pero quedó bajo el mínimo.

**Hipótesis (no verificadas, no son ventas):**
- Usar las ventas de ago–oct como medida del aporte de cada plato supone que la mezcla de demanda se parece en el próximo servicio.
- Los aumentos no cambian el volumen.
- No consideramos costos de personal por plato porque no hay datos.
- El colchón del 1 % es una protección contra pequeñas variaciones de costo. No es una predicción de cuánto va a subir el costo.
