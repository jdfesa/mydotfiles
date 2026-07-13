# Dmenu 5.4 personal build

Este directorio contiene el arbol fuente mantenido por estos dotfiles. Incluye
los parches `center` y `xresources` y se configura mediante `config.def.h`.

No ejecutar `sudo make install` directamente aqui. Usar:

```sh
os/linux/dmenu/scripts/build
os/linux/dwm/scripts/install-session
```

De esa forma los artefactos quedan fuera de Git y la instalacion conserva un
rollback verificable.
