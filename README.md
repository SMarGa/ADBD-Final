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

-Consulta a Residuo, eliminación de una fila de Celda, comprobamos con otra consulta a residuo que se ponen a nulo:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/1b1ff384-91c8-4647-a103-7fab9aef067a)

-Inserciones en Vehiculo que no cumplen primero el CHECK de la expresion regular para la matrícula y el segundo falla el CHECK que comprueba que dependiendo del tipo de vehiculo si es de residuos capacidad_personas lo tenga a null y capacidad_residuos no sea null y lo mismo para el de personas:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/39d49d37-83be-4678-bd21-75004b11f871)

-Inserción a Empleado que incumple CHECK de la expresión regular para números de teléfono:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/36747850-5b09-4db4-9eca-c3ccb0e64044)

-Inserción a Celda que incumple CHECK de capacidad mayor que 0:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/9c695150-03af-45c1-be27-12e9682233de)

-Inserciones a Ruta que viola CHECK de duracion superior a 0 e inferior a 480, y número de paradas mayor a 0:

![image](https://github.com/SMarGa/ADBD-Final/assets/72406871/a3ff2a0f-6898-4114-a927-518c8461a4a5)

Numerosos ejemplos adicionales de inserciones válidas se encuentran en el script, en la carga inicial de la base de datos.
