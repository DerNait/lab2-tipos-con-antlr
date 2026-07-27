# Laboratorio 2: Sistema de Tipos con ANTLR

## Video

[Ver demostración del laboratorio en YouTube](https://youtu.be/W7eN0Ss0vDM)

## Cambios implementados

Se extendió la gramática `SimpleLang.g4` con dos operaciones:

- `%`: operación de módulo válida únicamente entre dos valores `int`. Su resultado es `int`.
- `==`: comparación de igualdad válida entre dos valores numéricos o dos valores del mismo tipo. Su resultado es `bool`.

Las reglas se implementaron utilizando los dos recorridos solicitados:

- `TypeCheckVisitor`, mediante el patrón Visitor.
- `TypeCheckListener`, mediante el patrón Listener y propagación de tipos.

Ambas implementaciones acumulan los conflictos encontrados y producen los mismos mensajes de validación.

## Pruebas

Se conservaron los archivos de prueba originales y se agregaron:

- `program_test_extended_pass.txt`: casos válidos de módulo e igualdad.
- `program_test_extended_no_pass.txt`: conflictos con módulo, igualdad y operaciones aritméticas entre tipos incompatibles.

El entorno Docker utiliza ANTLR 4.13.1 tanto para generar el Lexer y Parser como para ejecutar el runtime de Python.
