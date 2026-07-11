# Operacion

Estado documentado el 2026-07-05.

## Comandos frecuentes

Sincronizar plugins:

```bash
nvim --headless "+Lazy! sync" +qa
```

Abrir gestor de plugins dentro de Neovim:

```vim
:Lazy
```

Abrir Mason:

```vim
:Mason
```

Health check:

```bash
nvim --headless "+checkhealth lazy lazyvim vim.lsp" "+write! /tmp/nvim-health.txt" +qa
sed -n '1,220p' /tmp/nvim-health.txt
```

Formatear Lua de la config:

```bash
~/.local/share/nvim/mason/bin/stylua ~/mydotfiles/shared/nvim/lua
```

Ver plugins instalados desde el lockfile sin depender de `jq`:

```bash
node -e 'const fs=require("fs"); const lock=JSON.parse(fs.readFileSync("shared/nvim/lazy-lock.json","utf8")); console.log(Object.keys(lock).sort().join("\n"));'
```

Motivo: en esta maquina el comando `jq` de la shell fallo por una dependencia
Node faltante. Eso no afecta Neovim, pero el comando anterior evita depender de
ese binario para inspeccionar el lockfile.

## Validaciones usadas

Arranque simple:

```bash
nvim --headless "+lua print('ok')" +qa
```

Validar Java LSP:

```bash
mkdir -p /tmp/lazyvim-java-test/src/main/java
printf '<project><modelVersion>4.0.0</modelVersion><groupId>test</groupId><artifactId>test</artifactId><version>1.0.0</version></project>\n' > /tmp/lazyvim-java-test/pom.xml
printf 'public class Test { public static void main(String[] args) { System.out.println("hi"); } }\n' > /tmp/lazyvim-java-test/src/main/java/Test.java
nvim --headless /tmp/lazyvim-java-test/src/main/java/Test.java "+lua vim.defer_fn(function() for _, client in ipairs(vim.lsp.get_clients({ bufnr = 0 })) do print('lsp client', client.name) end; vim.cmd('qa') end, 8000)"
```

Resultado esperado:

```text
lsp client jdtls
```

Validar Python LSP:

```bash
mkdir -p /tmp/lazyvim-python-test
printf 'print("hi")\n' > /tmp/lazyvim-python-test/main.py
nvim --headless /tmp/lazyvim-python-test/main.py "+lua vim.defer_fn(function() for _, client in ipairs(vim.lsp.get_clients({ bufnr = 0 })) do print('lsp client', client.name) end; vim.cmd('qa') end, 5000)"
```

Resultado esperado:

```text
lsp client pyright
lsp client ruff
```

Validar Markdown:

```bash
mkdir -p /tmp/lazyvim-md-test
printf '# Test\n\nhello\n' > /tmp/lazyvim-md-test/test.md
nvim --headless /tmp/lazyvim-md-test/test.md "+lua vim.defer_fn(function() for _, client in ipairs(vim.lsp.get_clients({ bufnr = 0 })) do print('lsp client', client.name) end; print('wrap', vim.wo.wrap); vim.cmd('qa') end, 5000)"
```

Resultado esperado:

```text
lsp client marksman
wrap true
```

## Troubleshooting

### `jdtls` falla en Mason

No usar `MasonInstall jdtls`.

Usar:

```bash
brew install jdtls
command -v jdtls
```

La config de LazyVim esta preparada para usar el binario del sistema.

Validar:

```bash
command -v jdtls
brew list --versions jdtls
```

No usar `jdtls --version` como health check. El wrapper puede intentar arrancar
Eclipse/JDT LS y escribir estado en `~/.eclipse`. La validacion importante para
esta config es que `command -v jdtls` exista y que al abrir un proyecto Java
Neovim levante el cliente `jdtls`.

### Warning de diccionario espanol

Si aparece un warning sobre `es.utf-8.spl`, revisar
`shared/nvim/lua/config/options.lua`.

Estado actual:

```lua
vim.opt.spelllang = { "en" }
```

### `tree-sitter (CLI)` no instalado

Instalar:

```bash
brew install tree-sitter-cli
```

Luego:

```bash
nvim --headless "+checkhealth lazy lazyvim" "+write! /tmp/nvim-health.txt" +qa
```

### Mason binarios no aparecen en la shell

Es normal que binarios como `pyright`, `ruff` o `marksman` no aparezcan con `command -v` en la shell.

Mason los agrega al PATH dentro de Neovim. En disco viven en:

```text
~/.local/share/nvim/mason/bin
```

Para validar desde Neovim:

```vim
:Mason
:LspInfo
```

### Al actualizar plugins algo se rompe

Primero revisar que cambio:

```vim
:Lazy
```

Luego:

```bash
git diff shared/nvim/lazy-lock.json
```

Si el problema viene de una actualizacion de plugin, se puede volver al commit
anterior del lockfile desde Git. No editar el lockfile a mano salvo emergencia y
siempre dejar documentado el motivo.
