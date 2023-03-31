# Ejercicio N°7:
Modificar los clientes para que notifiquen al servidor al finalizar con el envío de todas las apuestas y así proceder con el sorteo.
Inmediatamente después de la notificacion, los clientes consultarán la lista de ganadores del sorteo correspondientes a su agencia.
Una vez el cliente obtenga los resultados, deberá imprimir por log: `action: consulta_ganadores | result: success | cant_ganadores: ${CANT}`.

El servidor deberá esperar la notificación de las 5 agencias para considerar que se realizó el sorteo e imprimir por log: `action: sorteo | result: success`.
Luego de este evento, podrá verificar cada apuesta con las funciones `load_bets(...)` y `has_won(...)` y retornar los DNI de los ganadores de la agencia en cuestión. Antes del sorteo, no podrá responder consultas por la lista de ganadores.
Las funciones `load_bets(...)` y `has_won(...)` son provistas por la cátedra y no podrán ser modificadas por el alumno.

# Solucion:

Para implementar el mensaje de finalización se agrego una nueva parte al protocolo en donde se clarifica que se le esta enviando al servidor si apuestas o aviso de finalizado en un solo byte. De esta manera el servidor podrá leer solamente el primer byte y ahi poder saber como actuar en base a este.

Ahora que ya tenemos finalizado el proceso, procederé a explicar con más detalle el protocolo implementado. Primero debemos entender que interacciones se dan entre ambbos miembros para poder comprender porque existe cada parte del protocolo.

Flujo base:

1) Cliente envia apuesta(s) al servidor
2) Servidor confirma recepcion (correcta o incorrecta) de apuesta(s)
3) Cliente informa si continua o no
  a) Si continua vuelve a punto 1
  b) Si termina envia señal de fin
4)El servidor espera la confirmación de todos
5)El servidor envia los ganadores

Aca podemos notar como el cliente tiene un momento en el cual podría enviar 2 opciones, paso 3. Por lo cual el protocolo debe tener una manera de que el servidor reconozca que tipo de mensaje recibe. Para ello se implementa la primer parte del mensaje del cliente que es un Byte que informa si es un infore de fin o una publicacion de más apuestas.

De esta manera el servidor simplemente lee el primer byte y en base a este sabe si debe seguir leyendo o no. En caso de recibir apuestas seguirá leyendo para leer las apuestas mientras que de ser un aviso de fin no hay más información que leer. Para leer las apuestas se debio crear otro protocolo para que el servidor sepa cuantas y hasta adonde leer. El protocolo se basa en asumir que siempre se envian de a chunks (de ser una sola será un chunk de 1 apuesta), por lo que primero se lee un byte de 4 digitos que nos dice la cantidad de apuestas en el chunk y por ultimo tenemos todas las apuestas concatenadas

**Agregar imagen del protocolo**

![Protocolo Cliente](https://github.com/niragui/tp0-base/blob/Ej-7/Protocolo%20Cliente.jpg)

En el caso del servidor notamos como la dualidad se presenta a la hora de informar la recepcion de apuestas por lo que en ese caso tambien se incorpora un byte primero para entender como preseguir y a continuación el formato esperado. En este caso las opciones son informar recepción correcta o informar un error y explicar el error en dicho caso.

Por lo que el cliente leera el primer byte de encontrar el caso ok terminará la lectura y de encontrar un error procederá a leer el error.

![Protocolo Servidor](https://github.com/niragui/tp0-base/blob/Ej-7/Protocolo%20Servidor.jpg)

Por ultimo quedaría explicar como se envian los ganadores y como se manejan los short-reads y short-write y en conjunto con el tope de tamaños. Para enviar a los ganadores nuavemente se ingresa primero la cantidad de ganadores a leer y luego todos los ganadores concatenados en formato TLV, quiza es un poco redundante ya que siempre son tipo document pero esto permite que ante un futuro en el cual se quiera compartir mas informacion como supongamos el premio pueda ser simplemente añadido. En este caso no se incorpora ningun byte de tipo en el inicio del mensaje ya que no hay lugar a confusion al momento de leer los ganadores. 

Para solucionar los short-reads y short-writes se implementaron 2 funciones auxiliares que corroboran cuanto realmente se leyó/escribío y prosiguen el proceso hasta que ese valor sea coherente con el esperado. En la función de escritura también se incorporó un tope para cuanto mander con el cual realizamos el tope de 8kB por paquete, en caso de ser más largo sera partido por el codigo mismo.

