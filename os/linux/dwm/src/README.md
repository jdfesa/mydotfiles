# DWM 6.5 personal build

Este directorio contiene el arbol fuente mantenido por estos dotfiles. La
configuracion efectiva vive en `config.def.h`; `config.h` es un artefacto de
build y no debe editarse ni versionarse.

## Parches integrados

- bartoggle keybinds;
- bulkill;
- colorbar;
- fixmultimon;
- focusfullscreen;
- focusmaster-return;
- focusmonmouse;
- hide vacant tags;
- preventfocusshift;
- restartsig;
- spawntag;
- stacker;
- statuscmd;
- sticky;
- swallow;
- vanitygaps;
- xrdb.

La existencia de un parche en esta lista no obliga a conservarlo. Cada cambio
futuro debe evaluarse por su utilidad en la configuracion personal.

## Build

No ejecutar `make install` directamente en este directorio. Usar:

```sh
os/linux/dwm/scripts/build
os/linux/dwm/scripts/test-nested
os/linux/dwm/scripts/install-session
```

El procedimiento completo y el rollback se documentan en `../README.md`.
