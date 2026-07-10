# Use a Single Multi-OS Dotfiles Repository

Status: Accepted
Date: 2026-07-10

## Context

El repositorio actual nacio como una fuente de verdad para dotfiles de macOS.
Ahora tambien se quiere usar para experimentar con Arch Linux, maquinas
virtuales y un Windows 11 ocasional en un SSD separado.

La primera duda arquitectonica es si conviene crear un repositorio por sistema
operativo o mantener un repositorio centralizado.

Muchas herramientas son compartidas entre sistemas:

- Neovim;
- Git;
- Starship;
- Tmux;
- Lazygit;
- Yazi;
- Btop;
- Fzf;
- Ripgrep;
- Zoxide.

Si se separa por repositorio, estas configuraciones tenderian a duplicarse y
divergir.

## Decision

Mantener un unico repositorio central para dotfiles personales.

El repositorio se organizara con herramientas compartidas en carpetas propias y
capas especificas para sistema operativo, host y perfil cuando haga falta.

## Consequences

Ventajas:

- una sola fuente de verdad;
- menos duplicacion entre macOS, Linux y Windows;
- historial Git unificado;
- mas facil compartir decisiones entre sistemas;
- mejor base para una futura migracion a `chezmoi` o `stow`.

Costos:

- el repositorio necesita reglas claras para no mezclar responsabilidades;
- algunas carpetas seran especificas de un sistema operativo;
- los scripts de instalacion deberan detectar sistema, host y perfil.

Esta decision no obliga a migrar todo de inmediato. El repositorio puede seguir
funcionando con la estructura actual mientras se agregan capas nuevas de forma
gradual.

