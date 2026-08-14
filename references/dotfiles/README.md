# Dotfiles Dossiers

Cada subdirectorio documenta una fuente externa sin versionar su arbol completo.
El nombre sigue `<owner>-<repository>` y contiene:

- `source.toml`: identidad, revision auditada y estado de licencia;
- `inventory.md`: componentes encontrados y posible relacion con este repo;
- `review.md`: decisiones `keep`, `adapt`, `remove` o `reference-only`;
- `evidence.md`: comandos, hashes, fechas y limites de la auditoria.

Un dossier no convierte el material en configuracion activa. Las adaptaciones
se implementan aparte en la capa canonica correspondiente y se validan primero
en el canary.

