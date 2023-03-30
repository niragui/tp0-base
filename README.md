
# Enunciado:
Modificar servidor y cliente para que ambos sistemas terminen de forma _graceful_ al recibir la signal SIGTERM. Terminar la aplicación de forma _graceful_ implica que todos los _file descriptors_ (entre los que se encuentran archivos, sockets, threads y procesos) deben cerrarse correctamente antes que el thread de la aplicación principal muera. Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag `-t` utilizado en el comando `docker compose down`).

# Solucion:

Para solucionar esto, utilizo la biblioteca "signal" en python que ante la deteccion de alguna señal (en este caso SIGTERM) invoca alguna función. La función invocada setea un booleano en False que cortara la iteración a la espera de clientes.

Una idea similar se realiza con el cliente pero con bibliotecas de go.
