Sustitución propuesta: rechazada

# Respuesta a Bruno

Bruno:

Tenés razón en algo importante: no debiste enterarte por una lista. Te pedimos disculpas por eso. Nadie piensa que el trabajo de la cocina estuvo mal; la carta que tenemos se hizo con ese trabajo. Te explicamos los números con los papeles, sin vueltas, y te proponemos cómo seguir.

**Qué compra usamos.** Para el pollo (C01) usamos la última compra al Frigorífico del Muelle hasta el 31/10, y le sumamos el 18 % que avisaron para reponer [nivel-4/aviso-proveedor.md#L3]. El resto de los insumos quedó con su último precio: el aumento lo aplicamos solo a lo del frigorífico, como decís vos.

**Cómo llegamos al costo por plato.** Tomamos la receta de P12 [nivel-2/recetas.json#L452]: 150 g de pollo cocido, que son unos 260 g comprados, más las preparaciones S02, S09 y S15 y el resto de los ingredientes. Solo el pollo ya cuesta $ 2.779,48 por porción con el aumento: unos 260 g comprados [nivel-2/rendimientos.csv#L10] a $ 10,70 el gramo (última compra, ticket del 30/10, más el 18 %) [nivel-3/tickets/ticket-6270.jpg#imagen]. El plato completo da **$ 3.566,19** con precios de hoy [nivel-4/analisis.csv#L13] (antes del aumento, $ 3.101,67 [nivel-3/costos.csv#L13]). Creemos que el $ 1605 es otra cosa: en la caja, **A1605** es el código del artículo del Tostón de bondiola (P16) [nivel-3/caja/articulos.csv#L25]; el de tu pollo es A1577 [nivel-3/caja/articulos.csv#L19].

**Qué contamos como venta.** En la caja de agosto a octubre contamos las ventas de P12, restamos las anuladas y dejamos afuera propinas; P12 no forma parte de ningún combo [nivel-3/caja/combos.csv]. Son 441 vendidas menos 98 anuladas. Da **343 porciones netas** [nivel-3/margenes.csv#L13], no 986. Y justamente el Tostón de bondiola (P16) vendió 987 netas [nivel-3/margenes.csv#L17]: parece que se miró la fila de otro plato. Nos pasa a todos con planillas largas; lo vemos juntos, planilla en mano.

**Por qué salió de la lista.** La administración pidió retirar 10 platos [nivel-4/nota-administracion.md]. A todos los platos que no son de la casa ni opciones especiales les aplicamos la misma cuenta: porciones vendidas × (precio − costo). P12 deja $ 1.520.797 y queda entre los 10 más bajos [nivel-4/criterio.md#L45]. No es que el plato esté mal: con su precio sigue sobre el margen mínimo. Es que vende menos que otros. Si tus 986 porciones a $ 1605 fueran correctas, P12 no saldría: por eso lo primero es revisar los datos juntos.

**Lo de la soja en el Pollo al limón (P01).** No lo podemos hacer así. Los bocados de soja tienen alérgeno **soja** [nivel-5/oferta-almacen.md#L9] y la carta de P01 solo avisa gluten [nivel-4/carta.json#L10]. Un cliente alérgico podría pasarla mal, y además un "pollo al limón" sin pollo no es lo que el cliente pide. P01 ya cumple el margen con el aumento, así que no hace falta. No proponemos otra versión de este cambio. Cualquier plato con soja sería una idea aparte, que habría que evaluar desde cero y con la soja declarada.

**Lo que no sabemos.** No medimos tiempos de cocina ni cuántos clientes vuelven por P12. No lo vamos a inventar; lo podemos medir.

**Próximos pasos**
1. Nos sentamos vos, Mora y el equipo de cocina antes del próximo servicio y revisamos juntos caja y costo de P12.
2. Si hay un error en los datos, recalculamos con la misma regla y lo corregimos.
3. Si P12 sigue afuera, ustedes deciden cómo avisar a los clientes habituales y qué plato sugerir.
4. Las preparaciones S02, S09 y S15 se siguen usando en los platos que quedan; no se tira nada.
5. Hacemos una prueba de tiempos durante el servicio por 2 semanas.
6. Volvemos a mirar la carta en 30 días con las ventas nuevas.

Podemos discutir fuerte y seguir trabajando juntos. Gracias por escribir.

Mora y el equipo de análisis
