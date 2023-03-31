# Ejercicio N°5:
Modificar la lógica de negocio tanto de los clientes como del servidor para nuestro nuevo caso de uso.

## Cliente
Emulará a una _agencia de quiniela_ que participa del proyecto. Existen 5 agencias. Deberán recibir como variables de entorno los campos que representan la apuesta de una persona: nombre, apellido, DNI, nacimiento, numero apostado (en adelante 'número'). Ej.: `NOMBRE=Santiago Lionel`, `APELLIDO=Lorca`, `DOCUMENTO=30904465`, `NACIMIENTO=1999-03-17` y `NUMERO=7574` respectivamente.

Los campos deben enviarse al servidor para dejar registro de la apuesta. Al recibir la confirmación del servidor se debe imprimir por log: `action: apuesta_enviada | result: success | dni: ${DNI} | numero: ${NUMERO}`.

## Servidor
Emulará a la _central de Lotería Nacional_. Deberá recibir los campos de la cada apuesta desde los clientes y almacenar la información mediante la función `store_bet(...)` para control futuro de ganadores. La función `store_bet(...)` es provista por la cátedra y no podrá ser modificada por el alumno.
Al persistir se debe imprimir por log: `action: apuesta_almacenada | result: success | dni: ${DNI} | numero: ${NUMERO}`.

## Comunicación:
Se deberá implementar un módulo de comunicación entre el cliente y el servidor donde se maneje el envío y la recepción de los paquetes, el cual se espera que contemple:
* Definición de un protocolo para el envío de los mensajes.
* Serialización de los datos.
* Correcta separación de responsabilidades entre modelo de dominio y capa de comunicación.
* Correcto empleo de sockets, incluyendo manejo de errores y evitando los fenómenos conocidos como [_short read y short write_](https://cs61.seas.harvard.edu/site/2018/FileDescriptors/).
* Límite máximo de paquete de 8kB.


# Solucion

## Cliente

Se implemento una clase de agencia que recive los datos del servidor y de todos los clientes adheridos. Una vez creado el objeto crea las apuestas a partir de todos casa cliente y luego procede a enviarlas mediante un protocolo compartido con el servidor.

El protocolo consiste simplemente en enviar primero el tamaño del contenido a enviar y luego el conteido a enviar cada elemento de la apuesta en formato TLV. 

Para el servidor el cambio fue menor ya que no se debia incorporar ninguna nueva estructura como cliente o agencia. Simplemente se debia cambiar como se maneja el mensaje recivido que es seguir el protocolo ya establecido. Y una vez leidas las apuestas llamar a la funcion store_bet() para poder almacenarlas.

El protocolo es explicado en desarrolo en el ejercicio 7 donde se explica con desarrollo cada parte.
