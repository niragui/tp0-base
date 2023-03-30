# Ejercicio N°8:
Modificar el servidor para que permita aceptar conexiones y procesar mensajes en paralelo.
En este ejercicio es importante considerar los mecanismos de sincronización a utilizar para el correcto funcionamiento de la persistencia.

En caso de que el alumno implemente el servidor Python utilizando _multithreading_,  deberán tenerse en cuenta las [limitaciones propias del lenguaje](https://wiki.python.org/moin/GlobalInterpreterLock).

# Solución:

Para manejar el servidor de manera concurrente lo que se implemento son threads que cada uno se encarga de manejar una conexión. De esta manera el hilo principal puede continuar recibiendo nuevos clientes mientras que los otros hilos los leen. De esta forma el unico recurso a compartir que se presenta es el archivo donde se almacenan las apuestas. Es por ello que se utiliza un lock para el acceso a la escritura del archivo.

Cabe destacar que este formato de iniciar un thread cada vez que se recibe una nueva conexion es posible dbido a que sabemos que se trata de una cantidad limitada de agencias, de ser un sistema que escala a cantidades mayores no se podría dado que se trataria de demsiados threads en simultaneo. En caso de querer crear un sistema que soporte esto deberiamos crear un tope de threads e ir almaceenando sockets a leer para que estos threads vayan cargando a medida que se liberen.

