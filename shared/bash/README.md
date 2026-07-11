# Bash

Configuracion interactiva minima y portable para Bash. Mantiene los ejecutables
personales en `~/.local/bin`, siguiendo XDG y la convencion usada por el perfil
de Arch.

La integracion de NVM es opcional: solo se carga si ya existe bajo
`${XDG_CONFIG_HOME:-$HOME/.config}/nvm`. Este repositorio no instala NVM ni
versiona sus runtimes.
