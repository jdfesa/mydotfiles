# Linkarzu Dotfiles Inventory

## Scope

La auditoria comparo el estado actual de este repo, su historial Git y una copia
temporal de `linkarzu/dotfiles-latest` en la revision registrada en
`source.toml`. El objetivo no es declarar autoria, sino localizar material que
probablemente fue importado o adaptado y que necesita una decision consciente.

## Confirmed Or Strongly Derived Areas

| Area local | Relacion observada | Evidencia resumida |
|---|---|---|
| `shared/kitty/` | Importacion fuerte | Las 11 sesiones y gran parte de la configuracion coinciden con el upstream |
| `shared/ghostty/` | Importacion fuerte | El archivo principal conserva una similitud aproximada del 97.7% y 35 shaders coinciden exactamente |
| `shared/colorscheme/` | Derivacion fuerte | Variables y varias paletas conservan estructura y contenido similares |
| `os/macos/packages/homebrew/` | Derivacion fuerte | Un Brewfile coincide y los manifiestos principales son muy similares |
| `shared/btop/` | Importacion/adaptacion | Dos temas coinciden y `btop.conf` conserva alta similitud |
| `shared/fastfetch/` | Adaptacion probable | `config.jsonc` conserva estructura y contenido similares |
| `shared/tmux/` | Importacion historica reducida | El historial y `REMOVED_REFERENCE.md` registran la fuente importada |
| `shared/sesh/` | Importacion historica adaptada | El historial documenta la importacion y el posterior ajuste de rutas |
| `shared/yazi/` | Importacion/adaptacion | Activos y defaults coinciden; los archivos operativos fueron adaptados |
| `shared/lazygit/` | Importacion historica, hoy reescrita | El default coincide, pero la configuracion activa ya difiere y usa documentacion oficial |

## Reference Or Influence Only

| Area local | Clasificacion | Motivo |
|---|---|---|
| `shared/nvim/` | `reference-only` para Neobean | Neobean aporta ideas, pero LazyVim es la base oficial y su boilerplate no debe atribuirse a Linkarzu |
| AeroSpace, Hammerspoon y Sketchybar | Influencia no confirmada | La configuracion actual tiene poca o ninguna coincidencia directa con la revision auditada |
| Starship y Zsh | Influencia no confirmada | La similitud actual es insuficiente para afirmar una derivacion concreta |

## Foreign Session Inventory

Kitty conserva sesiones llamadas `blogpost`, `dotfiles`, `dots-private`,
`glove80`, `home`, `lua`, `networking`, `obsidian`, `scripts`, `skitty` y
`toucan`. Esos nombres describen proyectos y teclados del flujo de Linkarzu, no
el trabajo actual de este repositorio.

## Transitive Sources

- Los shaders de Ghostty indican como origen
  `https://github.com/hackrmomo/ghostty-shaders`.
- La coleccion de temas de Kitty incluye licencia y procedencia propias.
- El flavor Dracula de Yazi pertenece a un proyecto externo.

Una coincidencia llegada a traves del repo de Linkarzu no convierte a Linkarzu
en autor del recurso original. Cada activo debe conservar la atribucion real.

