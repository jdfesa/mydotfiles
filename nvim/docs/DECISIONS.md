# Decisiones

Estado documentado el 2026-07-05.

## Distro

Se reemplazo AstroNvim por LazyVim.

Motivo:

- La config AstroNvim anterior era casi plantilla base y no tenia personalizacion valiosa.
- LazyVim tiene buena documentacion, buen sistema de extras y una comunidad grande.
- Es una base razonable para aprender Neovim sin copiar una configuracion enorme desde el dia uno.

La migracion no fue tediosa porque Neovim separa configuracion, data, state y
cache. Al no haber personalizacion valiosa, se podia reemplazar la config y
reconstruir plugins/datos generados.

## AstroNvim vs LazyVim

No son la misma distro y sus atajos exactos no deben asumirse iguales.

Similitudes:

- Ambas son distribuciones sobre Neovim.
- Ambas usan `lazy.nvim` como gestor moderno de plugins.
- Ambas se apoyan en una capa de atajos con `<leader>`.
- Ambas usan `which-key.nvim` para descubrir combinaciones.

Diferencias relevantes:

- LazyVim organiza extensiones por `extras`.
- LazyVim recomienda configurar en `lua/config/` y `lua/plugins/`.
- AstroNvim tiene su propio set de plugins, comunidad y convenciones.
- El hecho de que un atajo exista en AstroNvim no significa que exista igual en LazyVim.

Decision local:

- Usar LazyVim como base.
- Conservar `Space` como leader.
- Usar `,` como localleader para mantener continuidad mental con AstroNvim y
  evitar que el localleader quede en `\`.

## Teclado y capas

Separacion mental:

- `Hyper` y `Meh`: sistema operativo, AeroSpace, ventanas y terminal.
- `Space`: leader de Neovim.
- `,`: localleader de Neovim.

Esto evita mezclar atajos del sistema con atajos del editor y facilita migrar a Linux mas adelante.

Los atajos propios viven bajo `<leader>N` para no contaminar categorias de LazyVim.

## Notas

El vault inicial es:

```text
/Users/jd/Documents/ObsidianVault
```

Atajos propios:

- `Space N f`: buscar notas.
- `Space N g`: buscar texto en notas.
- `Space N d`: abrir/crear nota diaria.

No se instalo `obsidian.nvim` todavia. La primera fase es editar Markdown bien,
entender LazyVim y no agregar una capa de workflow compleja antes de necesitarla.

Esta decision se revisara despues de usar el flujo Markdown base. Si se adopta
`obsidian.nvim`, se debe documentar en `PLUGINS.md`, `KEYMAPS.md` y `NOTES.md`.

## Java

`jdtls` se gestiona con Homebrew, no con Mason.

Motivo:

- El 2026-07-05 Mason intento descargar un snapshot de Eclipse para `jdtls`.
- La URL respondia `200` en `HEAD`, pero `GET` devolvia `500 Internal Server Error`.
- Homebrew tenia `jdtls 1.60.0` estable y reproducible.

La configuracion vive en:

```text
nvim/lua/plugins/java.lua
```

No borrar esa excepcion sin validar que Mason pueda instalar `jdtls` de forma
estable y reproducible.

## Spellcheck

`spelllang` queda en ingles (`en`) por ahora.

Motivo:

- Al usar `en,es`, Neovim avisaba que faltaba `es.utf-8.spl`.
- Para notas en Markdown es mejor evitar warnings hasta instalar diccionarios de forma reproducible.

Pendiente posible:

- Documentar e instalar spellfiles de espanol si la correccion ortografica dentro de Neovim se vuelve parte del flujo diario.

## Luarocks

`lazy.nvim` tiene soporte para rocks, pero esta config lo deja deshabilitado:

```lua
rocks = {
  enabled = false,
}
```

Motivo:

- Evitar warnings de health por una capa que no se esta usando.
- Reducir dependencias externas durante la adopcion inicial.
- Reactivarlo solo si un plugin real lo requiere.

## Linkarzu / Neobean

`NEOBEAN` no es una distro instalada localmente en esta config. Es una configuracion personal de Linkarzu basada en LazyVim, visible en sus dotfiles y videos.

Criterio actual:

- Aprender LazyVim base.
- Tomar ideas puntuales despues.
- No copiar una config grande sin entender dependencias, atajos y mantenimiento.

## Criterio general

La prioridad de esta etapa no es tener la config mas impresionante. Es tener una
base estable, entendible, restaurable y suficientemente potente para:

- notas diarias;
- Python;
- Java;
- Markdown;
- configuraciones JSON/YAML/TOML;
- crecimiento gradual hacia otros lenguajes.
