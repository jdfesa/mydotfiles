# Yazi

Configuracion para [Yazi](https://yazi-rs.github.io/), un gestor de archivos en terminal.

## Estado

Activo y enlazado desde:

```bash
~/.config/yazi -> ~/mydotfiles/shared/yazi
```


## Que aporta

- Muestra archivos ocultos y symlinks por defecto.
- Layout mas amplio: `ratio = [1, 4, 3]`, pensado para navegar con preview visible.
- Metadata de tamano por linea mediante `linemode = "size"`.
- Openers por tipo de archivo:
  - textos y JSON: `$EDITOR`, VS Code o revelar en Finder;
  - imagenes: abrir con macOS o revelar en Finder;
  - audio/video: abrir con macOS o inspeccionar con `ffprobe`;
  - comprimidos: extraer con `7zz`.
- Busqueda con `fd` y `rg`.
- Atajos para copiar rutas, cambiar linemode, ordenar y saltar a carpetas frecuentes.
- Tema Dracula, mantenido porque ya estaba instalado como flavor local.

## Dependencias

Base:

```bash
brew install yazi fd ripgrep sevenzip
```

Opcional, para previews mas ricos:

```bash
brew install ffmpeg poppler imagemagick jq
```

`yazi --debug` muestra que en esta maquina ya existen varias dependencias utiles: `fd`, `rg`, `ffprobe`, `pdftoppm`, `magick`, `fzf`, `zoxide`, `7zz` y `jq`.

## Keymaps principales

- `<Esc>` o `q`: salir.
- `o`: crear archivo o carpeta.
- `<Enter>`: abrir seleccion.
- `O`: elegir opener interactivamente.
- `r`: renombrar.
- `.`: alternar archivos ocultos.
- `dd`: enviar a papelera.
- `DD`: borrar permanentemente.
- `yy`: copiar seleccion.
- `xx`: cortar seleccion.
- `p`: pegar.
- `cc`: copiar ruta absoluta.
- `cd`: copiar directorio padre.
- `cf`: copiar nombre de archivo.
- `cn`: copiar nombre sin extension.
- `s`: buscar archivos con `fd`.
- `S`: buscar contenido con `rg`.
- `f`: filtrar el directorio actual.
- `ms`, `mm`, `mp`, `mn`: cambiar linemode.
- `,a`, `,m`, `,s`, `,n`: ordenar por nombre, modificado, tamano o natural.
- `gh`: home.
- `gc`: `~/.config`.
- `gd`: `~/Downloads`.
- `gr`: `~/mydotfiles`.
- `g<Space>`: cambiar de directorio interactivamente.
- `t`: nueva tab.
- `[` y `]`: tab anterior/siguiente.

## Rollback

Para volver al comportamiento minimo anterior, dejar:

```toml
[mgr]
show_hidden = true
```

Y en `keymap.toml` conservar solo:

```toml
[mgr]

prepend_keymap = [
  { on = "<Esc>", run = "quit", desc = "Exit the process" },
  { on = "o", run = "create", desc = "Create a file (ends with / for directories)" },
  { on = [ "d", "d" ], run = "remove", desc = "Trash selected files" },
  { on = [ "y", "y" ], run = "yank", desc = "Yank selected files (copy)" },
]
```

Si todavia no hiciste commit:

```bash
git restore shared/yazi/yazi.toml shared/yazi/keymap.toml shared/yazi/README.md
```

## Ideas pendientes

- Evaluar `smart-enter` para entrar/abrir con menos friccion.
- Evaluar `mime-ext` para detectar mejor tipos raros.
- Evaluar `yatline` si se quiere una statusline mas rica.
- Evaluar integracion con Neovim mediante `mikavilpas/yazi.nvim` si la config real de Neovim se versiona en este repo.
