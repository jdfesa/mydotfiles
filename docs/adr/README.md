# Architecture Decision Records

Esta carpeta contiene decisiones de arquitectura del repositorio.

Los nombres de archivo y titulos principales se escriben en ingles para mantener
coherencia con el resto de la documentacion tecnica. El contenido explicativo se
escribe en espanol.

Esta convencion tambien se aplica a nombres de carpetas y archivos tecnicos del
repositorio.

## Decision Index

- [0001: Use A Single Multi-OS Dotfiles Repository](0001-use-a-single-multi-os-dotfiles-repository.md)
- [0002: Use Layered Dotfiles Organization](0002-use-layered-dotfiles-organization.md)
- [0003: Keep Symlinks Now, Evaluate Chezmoi Later](0003-keep-symlinks-now-evaluate-chezmoi-later.md)
- [0004: Use Standard Linux Runtime Paths](0004-use-standard-linux-runtime-paths.md)
- [0005: Group Shared Configurations](0005-group-shared-configurations.md)
- [0006: Separate Hosts From Profiles](0006-separate-hosts-from-profiles.md)
- [0007: Isolate External Reference Material](0007-isolate-external-reference-material.md)

## When To Add An ADR

Agregar un ADR cuando la decision:

- afecta la estructura del repositorio;
- cambia la estrategia de instalacion o restauracion;
- define una convencion que varias herramientas deben seguir;
- separa responsabilidades entre `shared/`, `os/`, `profiles/`, inventarios
  `hosts/`, documentacion de maquinas y valores locales;
- evita volver a discutir una decision importante en el futuro.

No hace falta un ADR para cambios pequenos como aliases, opciones visuales,
keymaps puntuales, temas o ajustes internos de una sola herramienta.

## Format

Cada ADR usa este formato:

```text
# English Decision Title

Status: Accepted
Date: YYYY-MM-DD

## Context

## Decision

## Consequences
```
