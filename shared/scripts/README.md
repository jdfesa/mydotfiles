# Shared Scripts

Coleccion de utilidades personales portables entre macOS y GNU/Linux.

Cada script independiente o pequeña suite vive en su propia carpeta para que
su codigo, documentacion, pruebas y archivos auxiliares no se mezclen con los
de otras utilidades:

```text
shared/scripts/
  cpu-watch/
    cpu-watch
    README.md
  another-script/
    another-script
    README.md
```

## Reglas de ubicacion

- Scripts portables de uso personal: `shared/scripts/<name>/`.
- Scripts exclusivos de una plataforma: `os/<system>/scripts/<name>/`.
- Scripts internos de una herramienta: dentro de la carpeta de esa
  herramienta.
- Mantenimiento transversal de `mydotfiles`: `scripts/` en la raiz.

Un script pequeño conserva igualmente su propia carpeta cuando necesita README
o puede crecer con pruebas y archivos auxiliares. Varios ejecutables que forman
una misma utilidad comparten carpeta.

## Inventario

Este README funciona como indice general. Cada script nuevo debe agregar una
fila con su proposito, compatibilidad y punto de entrada; la documentacion
detallada permanece dentro de su propia carpeta.

| Script | Proposito | Compatibilidad | Ejecutable |
|---|---|---|---|
| [CPU Watch](cpu-watch/README.md) | Detectar carga de CPU, mostrar procesos responsables y ofrecer una terminacion confirmada. | macOS y Linux | `cpu-watch/cpu-watch` |
