# Enunciado
Crear un script que permita verificar el correcto funcionamiento del servidor utilizando el comando `netcat` para interactuar con el mismo. Dado que el servidor es un EchoServer, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado. Netcat no debe ser instalado en la máquina _host_ y no se puede exponer puertos del servidor para realizar la comunicación (hint: `docker network`).

# Solucion
Primero se crea un archivo bash "test.sh" que simplemente envia un mensaje mediante netcat y luego recibe la respuesta. Una vez obtenida la respuesta se compara con el mensaje enviado y en base a esta comparación se imprime una respuesta.

Para correr este archivo se implemento un nuevo llamado dentro del makefile que invoca tanto al server como al bash file y luego los cierra. Este comando es "docker-compose-test"


```
make docker-compose-test
```
