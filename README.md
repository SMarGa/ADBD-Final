# ADBD-Final


### Imágenes de pruebas sobre la base de datos en sql:

Las siguientes pruebas se realizarán sobre la carga inicial de la base de datos como se encuentra en el script.

-Consulta sobre Empleado:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/ef134622-1598-42c1-ba5f-46e788ccabdf)

-Consulta sobre Guia:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/f7c96184-72e7-40e4-a969-f95edfec6589)

-Eliminación de un empleado, borra en cascada en la tabla Guia:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/736a8016-eff0-4070-a09f-94d9d05c7ae2)

-Consulta sobre Transportista y Vehiculo e intento de inserción que viola trigger de compatibilidad de carnet del transportista con tipo del vehiculo:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/63d92e34-6f78-4cff-8db9-dd1a345fcd61)

-Ocurre lo mismo al intentarlo con una operación de actualización:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/6119ea78-9c69-4dba-863a-4a8e70519a4f)

-Inserción en Ruta, vemos que el atributo calculado se introduce automáticamente con un trigger:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/90119caa-426e-4b64-920b-5e80b15d49de)

-Inserción en instalación con tipos repetidos(plástico, papel, papel) trigger lo pone bien (plástico, papel):

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/6d1e632b-9f93-4307-af93-0701f051484b)
