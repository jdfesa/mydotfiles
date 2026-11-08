# Tmux on Linux

El entrypoint Linux carga `shared/tmux/tmux.conf` sin modificarlo y aplica
solo las diferencias de plataforma: barra inferior y portapapeles Wayland/X11.
Los perfiles derivados de `arch-workstation` incluyen `layers/linux-tmux` y
enlazan el archivo en `~/.config/tmux/tmux.conf`.

Para aprender el uso diario, consulta [Daily Workflow](../../../shared/tmux/daily-workflow.md).
Para practicar por niveles, usa [Tmux Training](../../../shared/tmux/training/README.md).
Para recordar una tecla, usa [Tmux Cheatsheet](../../../shared/tmux/tmux-cheatsheet.md).
Esta página se centra en instalar y verificar la capa Linux.

## Installation

Necesita `tmux`, `git`, `bash`, `zsh`, `python` e `inetutils` del manifiesto base
de Arch. [inetutils](https://archlinux.org/packages/core/x86_64/inetutils/files/)
proporciona `hostname`, que Resurrect invoca al resolver
la ruta de guardado. Si falta en un entorno ya instalado:

```sh
rtk proxy sudo pacman -S --needed inetutils
```

Para copiar al sistema, usa `wl-clipboard` en Wayland o `xclip` en X11.

```sh
scripts/link --dry-run layers/linux-tmux
scripts/link layers/linux-tmux
scripts/doctor layers/linux-tmux
os/linux/tmux/install-plugins
```

El instalador descarga [TPM](https://github.com/tmux-plugins/tpm) en
`~/.tmux/plugins/tpm` y los plugins declarados en el archivo compartido en
`${XDG_CONFIG_HOME:-$HOME/.config}/tmux/plugins`. No actualiza clones existentes
ni reemplaza configuraciones ajenas. Usa un socket temporal para instalar y
cargar los plugins sin iniciar ni recargar el servidor tmux habitual.

El monitor de CPU/memoria crea su propio `venv` e instala `psutil` según sus
dependencias upstream. Los plugins y sus entornos no se versionan: se recrean
desde GitHub. La primera instalación necesita acceso de red a GitHub y PyPI.
Si falla, revisa el error antes de abrir la sesión de trabajo; no se considera
completada una instalación con placeholders sin resolver.

## Workflow

Inicia un proceso nuevo de Kitty para leer el entrypoint actualizado sin
recargar las ventanas que ya están abiertas:

```sh
kitty --detach --config "$HOME/mydotfiles/os/linux/kitty/kitty.conf"
```

Dentro de esa nueva instancia, crea o recupera la sesión:

```sh
tmux new-session -A -s mydotfiles -c "$HOME/mydotfiles"
```

El prefijo único es **Ctrl+Espacio**. Tras soltarlo, `c` crea una ventana,
`\` divide izquierda/derecha, `-` divide arriba/abajo, `m` maximiza/restaura
y `d` desconecta sin cerrar los procesos. Consulta la
[guía compartida](../../../shared/tmux/README.md) para el resto de atajos.
Kitty no inicia tmux automáticamente.

En modo copia (`prefijo`, `[`), `v` inicia la selección y `y` la copia tanto
al buffer de tmux como al portapapeles del sistema. El helper prioriza
`wl-copy` si hay `WAYLAND_DISPLAY`; con `DISPLAY` usa `xclip`. Sin backend
gráfico conserva el buffer de tmux y muestra un aviso. `prefijo`, `P` pega
ese buffer. Las variables Wayland se actualizan al adjuntar un cliente.

`vim-tmux-navigator` habilita `Ctrl+h/j/k/l` entre paneles desde el shell. La
configuración Linux de Kitty deja pasar esas teclas cuando tmux está en primer
plano. El lado Neovim requiere integración propia, todavía no declarada en
este checkout. La alternativa común es prefijo y flechas; consulta la
[auditoría](../../../shared/tmux/training/compatibility.md#contextual-extensions).
No se cambian atajos globales del compositor ni la configuración macOS.
La barra omite la batería cuando `/sys/class/power_supply` no contiene una:
el script upstream presupone su existencia y falla en equipos de escritorio.

## Verification

```sh
scripts/test-linux-terminal
scripts/validate-profiles
```

Las pruebas usan un `HOME`, un socket y backends de clipboard falsos; no
escriben el portapapeles real ni tocan servidores activos. Si Kitty está
disponible, también validan sus dos entrypoints con el parser instalado.

Para la comprobación física, usa esa instancia nueva cuando sea conveniente,
entra a tmux y prueba prefijo, divisiones, navegación, copia y
barra inferior. No cierres ni recargues ventanas con trabajo pendiente.
Resurrect/Continuum pueden reconstruir una disposición después de reiniciar,
pero no mantienen vivos los procesos. Sus archivos de estado, historial y
contenido de paneles son privados y deben permanecer fuera del repositorio.
