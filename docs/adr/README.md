# Architecture Decision Records

Esta carpeta contiene decisiones de arquitectura del repositorio.

Los nombres de archivo y titulos principales se escriben en ingles para mantener
coherencia con el resto de la documentacion tecnica. El contenido explicativo se
escribe en espanol.

Esta convencion tambien se aplica a nombres de carpetas y archivos tecnicos del
repositorio.

## When To Add An ADR

Agregar un ADR cuando la decision:

- afecta la estructura del repositorio;
- cambia la estrategia de instalacion o restauracion;
- define una convencion que varias herramientas deben seguir;
- separa responsabilidades entre `config/`, `os/`, `profiles/`, documentacion de
  maquinas y valores locales;
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
