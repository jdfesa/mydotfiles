# Zsh Configurations & Fixes

Esta carpeta contiene scripts y configuraciones modulares para la terminal Zsh.

## ide_fix.zsh

Este script soluciona los problemas visuales al usar la terminal integrada de ciertos IDEs (como Apache NetBeans o VS Code).

**¿Qué hace?**
Desactiva el tema complejo de Powerlevel10k (que suele "romperse" al no tener soporte completo de fuentes o colores en emuladores de terminal limitados) y carga en su lugar un prompt minimalista pero funcional, que incluye soporte para ver la rama actual de Git. 

Esto es especialmente útil para poder realizar _commits_ o ejecutar comandos cómodamente dentro del IDE sin que la terminal se vea corrupta.

### Recomendación de Fuente

Para la mejor compatibilidad de íconos y caracteres tanto en el prompt minimalista como en Powerlevel10k, se recomienda tener configurada la fuente **JetBrainsMono Nerd Font** en tu terminal principal y en las configuraciones del IDE.
