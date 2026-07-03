# AeroSpace Concepts

Este documento explica el modelo mental de esta configuracion. La referencia rapida de teclas esta en [KEYBINDINGS.md](KEYBINDINGS.md), y la mnemotecnia de workspaces esta en [WORKSPACES.md](WORKSPACES.md).

## Workspaces vs Spaces de macOS

| Concepto | macOS Spaces | AeroSpace workspaces |
|---|---|---|
| Que son | Escritorios virtuales nativos de macOS | Espacios virtuales gestionados por AeroSpace |
| Cambio | Gestos, `Ctrl + flechas`, Mission Control | Atajos directos de AeroSpace |
| Control por teclado | Limitado | Foco, movimiento, ruteo, monitores y layouts |
| API | No hay API publica completa | CLI de AeroSpace |

AeroSpace trabaja mejor si usas un solo Space nativo de macOS y dejas que AeroSpace maneje los workspaces. Mezclar ambos modelos suele agregar friccion: animaciones de Mission Control, workspaces duplicados y ventanas que parecen estar en lugares distintos.

## Arbol de Ventanas

AeroSpace organiza las ventanas como un arbol:

```text
Workspace U
├── Ghostty
└── Contenedor horizontal
    ├── Chrome
    └── VS Code
```

Las ventanas son hojas. Los contenedores agrupan ventanas y tienen dos propiedades importantes:

- **Layout**: `tiles` o `accordion`.
- **Orientacion**: horizontal o vertical.

## Layouts

**Tiles** muestra todas las ventanas visibles y repartidas en pantalla. Es el layout mas natural para ajustar tamanos con resize.

**Accordion** apila varias ventanas dentro del mismo espacio visual. Normalmente ves una ventana principal y navegas entre ventanas con foco. Es util cuando queres bajar ruido visual, pero resize puede sentirse menos obvio.

Regla practica:

- Si queres comparar o redimensionar dos ventanas, usa `tiles`.
- Si queres concentrarte en una ventana dentro de un grupo, usa `accordion`.

## Modos vs Layouts

No son lo mismo:

| Capa | Ejemplos | Que cambia |
|---|---|---|
| Modo de teclado | `main`, `resize`, `service` | Que hacen las teclas temporalmente |
| Layout de workspace | `tiles`, `accordion` | Como se ven y se agrupan las ventanas |

Ejemplo: podes estar en layout `accordion` y entrar al modo `[R]` de resize. El modo cambia el teclado; el layout cambia la estructura visual.

## Normalizacion

La config activa:

```toml
enable-normalization-flatten-containers = true
enable-normalization-opposite-orientation-for-nested-containers = true
```

Eso hace que AeroSpace simplifique el arbol automaticamente:

- Si un contenedor tiene un solo hijo, se elimina.
- Los contenedores anidados alternan orientacion para mantener una estructura predecible.

Esta decision favorece un setup facil de entender mientras se aprende el window manager.

## Floating

Algunas ventanas flotan sobre el mosaico, como dialogos o herramientas auxiliares. Tambien podes alternar manualmente una ventana entre floating y tiling desde modo servicio:

```text
Meh + ; -> F
```

Floating sirve para ventanas pequenas, temporales o poco compatibles con tiling. Para trabajo diario, el objetivo es que la mayoria de ventanas importantes sigan en tiling.

## Sketchybar

Sketchybar cumple dos roles para AeroSpace:

- Muestra los workspaces persistentes `U I O P Y N`.
- Muestra el modo activo con un indicador temporal: `[S]` para service, `[R]` para resize.

Los detalles tecnicos de esa integracion viven en [SCRIPTS.md](SCRIPTS.md).
