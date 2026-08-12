# Helium on Arch Linux

Helium es el navegador predeterminado de `arch-desktop`. Firefox permanece
instalado como alternativa de recuperacion desde los repositorios oficiales.

## Package Source

La pagina oficial de Helium publica Linux como beta y ofrece AppImage/tarball,
pero no un repositorio Arch. Se usa `helium-browser-bin` desde AUR porque:

- integra el tarball Linux oficial firmado por Helium;
- registra todos los archivos con pacman;
- permite auditar y actualizar el paquete como una unidad;
- evita copiar manualmente binarios bajo `/opt`.

El AUR no es confiable por definicion. `scripts/install` fija y comprueba:

- version `0.15.4.1-1`;
- commit AUR `108cb9ad9251ed783070620165efae38bd8765e2`;
- SHA-256 del `PKGBUILD` y `.SRCINFO` revisados;
- fingerprint de la clave de firma upstream;
- hashes y firma del tarball mediante `makepkg --verifysource`.

La build se realiza como usuario normal. `sudo` se usa solamente para instalar
el paquete local generado con `pacman -U`.

## Installation

Previsualizar:

```bash
os/linux/helium/scripts/install
```

Ejecutar preferentemente desde una terminal grafica XFCE:

```bash
os/linux/helium/scripts/install --execute
```

El instalador tambien registra `helium.desktop` para HTTP, HTTPS y HTML, y lo
establece como navegador predeterminado mediante XDG.

## Validation

```bash
pacman -Q helium-browser-bin
command -v helium-browser
xdg-settings get default-web-browser
xdg-mime query default x-scheme-handler/https
```

Resultados esperados:

```text
helium-browser-bin 0.15.4.1-1
/usr/bin/helium-browser
helium.desktop
helium.desktop
```

## Updates

No ejecutar automaticamente una version nueva del AUR. Para actualizar:

1. obtener el nuevo commit;
2. revisar diff de `PKGBUILD`, `.SRCINFO`, patches y scripts;
3. confirmar nueva clave/firma y fuentes;
4. actualizar las constantes de `scripts/install` y `aur-reviewed.txt`;
5. construir, inspeccionar e instalar;
6. probar en XFCE/X11 y Hyprland/Wayland.

El cache/build vive fuera de Git bajo `$XDG_CACHE_HOME` o `~/.cache`.
