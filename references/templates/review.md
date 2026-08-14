# Source Review

## Decisions

| Area | Estado | Decision | Validation |
|---|---|---|---|
| Example | `pending-review` | Comprender antes de usar | No iniciada |

Estados permitidos: `pending-review`, `keep`, `adapt`, `remove` y
`reference-only`.

## Promotion Checklist

- [ ] Se comprende el comportamiento y sus dependencias.
- [ ] Se verificaron licencia y atribucion.
- [ ] Se eliminaron rutas, nombres y proyectos ajenos.
- [ ] La adaptacion vive en la capa canonica correcta.
- [ ] Se probo manualmente y con validaciones automatizadas.
- [ ] Se califico en el canary antes de produccion.
- [ ] Se documento rollback cuando el cambio puede afectar el trabajo diario.
