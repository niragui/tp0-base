# Enunciado

Modificar el cliente y el servidor para lograr que realizar cambios en el archivo de configuración no requiera un nuevo build de las imágenes de Docker para que los mismos sean efectivos. La configuración a través del archivo correspondiente (`config.ini` y `config.yaml`, dependiendo de la aplicación) debe ser inyectada en el container y persistida afuera de la imagen (hint: `docker volumes`).

# Solucion

Se agrega en el archivo DockerCompose (y en sus derivados necesarios para la composicion mediante el archivo pyton creado en el ejercicio 1) para que se incluyan los archivos de configuracion como volumenes.
