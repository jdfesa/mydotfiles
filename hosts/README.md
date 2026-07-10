# Hosts

Notas especificas por maquina.

Esta capa no debe duplicar configuraciones completas. Sirve para registrar el
estado real de una maquina, diferencias temporales, inventarios, migraciones y
decisiones que no aplican a todos los sistemas.

Las configuraciones reutilizables deben vivir en:

- herramientas compartidas en la raiz del repo;
- `os/<system>/` cuando sean especificas de un sistema operativo;
- `profiles/` cuando describan una combinacion instalable.

Los secretos, credenciales, claves privadas y passwords quedan fuera de Git.
