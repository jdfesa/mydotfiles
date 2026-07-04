# Lazygit Sources

Referencias para aprender Lazygit sin depender de memoria ni de una configuracion ajena.

## Oficiales

- [Lazygit repository](https://github.com/jesseduffield/lazygit): README, demos, instalacion y vision general.
- [Configuration docs](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md): esquema de `config.yml`, `gui`, `git.paging`, `customCommands`, `keybinding` y `os`.
- [Default keybindings](https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md): mapa completo de teclas por panel.
- [Custom Commands Compendium](https://github.com/jesseduffield/lazygit/wiki/Custom-Commands-Compendium): ejemplos de comandos personalizados, incluyendo commits convencionales y flujos con GitHub CLI.
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/): formato de mensajes usado por el comando `<C-v>`.

## Ruta corta de aprendizaje

1. Leer el README oficial solo hasta `Usage`.
2. Abrir un repo con cambios descartables y recorrer paneles sin ejecutar acciones peligrosas.
3. Practicar:
   - stage/unstage de archivo completo;
   - stage parcial de hunks;
   - commit normal;
   - stash y pop;
   - cambio de rama.
4. Recien despues revisar rebase interactivo, squash/fixup, reset y revert.

## Teclas que conviene memorizar primero

- `?`: ayuda contextual.
- `tab`: cambiar panel.
- flechas o `j/k`: moverse.
- `space`: stage/unstage.
- `c`: commit.
- `P`: push.
- `p`: pull.
- `s`: stash.
- `z`: undo.
- `y`: copiar al clipboard, configurado en este repo.

## Notas

Lazygit ejecuta Git real por debajo. Si una accion no se entiende, conviene mirar primero que comando Git representa y practicarlo en un repo de prueba.
