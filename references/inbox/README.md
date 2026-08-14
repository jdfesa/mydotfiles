# Reference Inbox

Esta carpeta recibe clones o copias temporales de fuentes externas durante una
auditoria. Git ignora su contenido para evitar incorporar repositorios completos,
historiales, archivos grandes o material con licencias incompatibles.

Cada fuente debe tener un dossier versionado en `references/dotfiles/`. El clon
se elimina cuando la evaluacion termina; nunca se usa como fuente de un perfil,
symlink, script de inicio o dependencia de runtime.

