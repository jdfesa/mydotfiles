# Zoxide

`zoxide` es una herramienta de navegacion inteligente para la terminal. Aprende las carpetas que visitas con frecuencia y luego te permite saltar a ellas con una busqueda corta.

## Estado

Instalado, pero todavia no activado en Zsh dentro de este repo.

## Para que sirve

En vez de escribir rutas largas como:

```bash
cd ~/mydotfiles
```

con zoxide activo podrias escribir:

```bash
z mydot
```

`zoxide` calcula la carpeta mas probable segun tu historial y te lleva ahi.

## Relacion con Sesh

`sesh` puede usar `zoxide` para descubrir carpetas frecuentes automaticamente. Por eso `sesh list` sin flags intenta consultar zoxide.

En nuestro flujo inicial de `sesh` no dependemos de eso. Usamos:

```bash
sesh list -c
sesh picker -c
```

La bandera `-c` limita la lista a las sesiones definidas en `~/mydotfiles/sesh/sesh.toml`.

## Instalacion

```bash
brew install zoxide
```

Ya esta incluido en `brew/00-base/Brewfile`.

## Activacion futura

Para integrarlo con Zsh habria que agregar esto a `~/.zshrc`:

```bash
eval "$(zoxide init zsh)"
```

No lo activamos todavia porque cambia el flujo diario de navegacion en la terminal. Conviene probar primero `sesh` con sesiones explicitas y luego decidir si queremos que zoxide aprenda carpetas frecuentes.

## Pendiente

- Decidir si se activa en `~/.zshrc`.
- Integrarlo con `sesh` sin tener que usar siempre `-c`.
- Revisar el script de Kitty basado en zoxide antes de usarlo como flujo diario.
