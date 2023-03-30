# Ejercicio N°6:
Modificar los clientes para que envíen varias apuestas a la vez (modalidad conocida como procesamiento por _chunks_ o _batchs_). La información de cada agencia será simulada por la ingesta de su archivo numerado correspondiente, provisto por la cátedra dentro de `.data/datasets.zip`.
Los _batchs_ permiten que el cliente registre varias apuestas en una misma consulta, acortando tiempos de transmisión y procesamiento. La cantidad de apuestas dentro de cada _batch_ debe ser configurable.
El servidor, por otro lado, deberá responder con éxito solamente si todas las apuestas del _batch_ fueron procesadas correctamente.

# Solucion:
Para implementar esto al protocolo se le incorporo un nuevo termino al inicio que informa la cantidad de apuestas a leer y se envia todas las apuestas concatenadas. Para leerlas simplemente se lee cuantas apuestas hay y se utiliza el protocolo creado en el Ejercicio 5 para cada una.

Otra parte de la implementacion requirio poder leer los archivos del dataset, para lo cual se recurrió a la biblioteca de csv y simplemente se derivaron los valores a su posicion correspondiente
