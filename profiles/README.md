# Profiles

Los perfiles declaran que fuentes del repositorio se enlazan en un entorno.
No contienen copias de configuraciones.

Cada archivo `*.links` usa una entrada por linea:

```text
ruta/relativa/al/repo|$HOME/ruta/de/destino
```

Reglas:

- la fuente siempre es relativa a la raiz del repositorio;
- el destino debe comenzar con `$HOME/`;
- las lineas vacias y las que comienzan con `#` se ignoran;
- los destinos existentes que no sean symlinks nunca se reemplazan
  automaticamente;
- `scripts/link` crea o repara los enlaces;
- `scripts/doctor` comprueba que fuentes y destinos coincidan.

Perfiles iniciales:

- `macos-main.links`: configuracion activa de la Mac principal;
- `arch-dwm.links`: se agregara cuando DWM tenga configuracion reproducible.

