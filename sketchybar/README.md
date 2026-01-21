<h1 align="center">
  SketchyBar Configuration (Lua)
</h1>

<p align="center">
  <b>Una configuración moderna, rápida y mantenible escrita en Lua.</b>
</p>

Esta configuración es una evolución completa migrada de Bash a **Lua** (usando SbarLua). Ofrece un rendimiento superior, animaciones más fluidas y una estructura de código más limpia y mantenible.

---

## 🚀 Instalación y Dependencias

### Prerrequisitos
Para que esta configuración funcione correctamente, necesitas instalar las siguientes dependencias. Usa Homebrew para facilitar el proceso:

```sh
# 1. Instalar Sketchybar (si no lo tienes)
brew tap FelixKratz/formulae
brew install sketchybar

# 2. Instalar utilidades esenciales
# jq: Necesario para parsear JSON (usado por el widget del Clima)
# lua: Lenguaje base de la configuración
brew install lua jq switchaudio-osx media-control imagemagick

# 3. Instalar Fuentes (CRÍTICO)
# Sin estas fuentes, verás rectángulos o texto roto en lugar de iconos.
brew install --cask font-sketchybar-app-font font-maple-mono-nf-cn
brew install --cask font-hack-nerd-font
```

### Instalar SbarLua (API de Lua para Sketchybar)
Esta configuración requiere `SbarLua` para funcionar. Sketchybar por defecto usa sh, pero nosotros usamos este plugin para lógica avanzada.

```sh
git clone --depth 1 --quiet https://github.com/FelixKratz/SbarLua.git /tmp/sbarlua
cd /tmp/sbarlua && make install
```

### Instalar Configuración
Si estás en este repo, probablemente ya tienes los archivos. Simplemente asegúrate de que `.config/sketchybar` apunte a esta carpeta.

```sh
# Ejemplo de link simbólico si clonaste en otro lado
ln -sf ~/path/to/mydotfiles/sketchybar ~/.config/sketchybar
```

---

## 📂 Estructura del Proyecto

A diferencia de las configuraciones clásicas en Bash (que lanzan un proceso por cada item), esta configuración carga un solo entorno Lua, lo que reduce drásticamente el uso de CPU.

- **`init.lua`**: Punto de entrada. Carga la configuración base y lanza el bucle de eventos.
- **`settings.lua`**: Variables globales (Fuentes, Colores, Padding). Aquí definimos `ID_STYLE = nil` para tener espacios numéricos.
- **`items/`**: Definición de cada widget.
  - **`weather/`**: Script avanzado de clima (`weather.lua` + `weather.sh`).
  - **`monitor/`**: Scripts de sistema (RAM, CPU).
  - **`front_app/`**: Lógica de la aplicación activa.
- **`helpers/`**: Funciones de utilidad y mapas de iconos.

---

## 🌟 Widgets Destacados y Personalizaciones

Hemos realizado varias mejoras clave sobre la configuración base:

### 1. Clima (Weather)
- **Script Híbrido**: Usa `weather.sh` para hacer la petición a `wttr.in` y `weather.lua` para renderizarlo.
- **Dependencia**: Requiere `jq` instalado y en el path (verificado en `/opt/homebrew/bin/jq`).
- **Iconos Dinámicos**: Muestra sol, nubes, lluvia, etc., dependiendo del estado real.

### 2. Monitor de RAM Preciso
- **Problema Anterior**: El comando `memory_pressure` nativo a veces se congelaba o daba datos abstractos.
- **Solución**: Implementamos `ram.sh` que usa `vm_stat` para calcular el uso real de memoria (App + Wired + Compressed).
- **Resultado**: Un porcentaje de uso de RAM extremadamente preciso y actualizado cada 5 segundos.

### 3. Espacios de Trabajo (Workspaces)
- **Estilo Numérico**: Se desactivó el mapeo "Grip" (letras griegas) en favor de números claros (1, 2, 3...) para coincidir con los atajos de teclado de **AeroSpace**.
- **Configuración**: Controlado en `settings.lua` (`ID_STYLE = nil`).

### 4. Aplicación Frontal (Front App)
- **Estilo Visual**: Muestra el icono **real** de la aplicación (imagen a color del sistema) junto a su nombre.
- **Implementación**: Usa `icon.background.image` en `front_app.lua` apuntando a `app.<NombreApp>`, lo que permite a Sketchybar extraer el icono oficial de la app directamente desde macOS.

---

## 🔧 Troubleshooting

### "Veo cuadrados en lugar de iconos"
- **Causa**: Falta la fuente `sketchybar-app-font`.
- **Solución**: Ejecuta `brew install --cask font-sketchybar-app-font` y recarga la barra (`sketchybar --reload`).

### "El clima no carga"
- **Causa**: Probablemente `jq` no está instalado o no está en el PATH.
- **Verificación**: Ejecuta `which jq` en tu terminal. Si no sale nada, instala con `brew install jq`.

### "Los espacios tienen nombres raros"
- Revisa `settings.lua`. Si quieres números, asegúrate de que `ID_STYLE` sea `nil`. Si quieres letras griegas, ponlo en `"greek_uppercase"`.

---

## 🎨 Temas
La configuración soporta múltiples temas definidos en `themes/`. Por defecto usamos una variante oscura estilizada. Puedes cambiar los colores editando `settings.lua` o importando otro archivo de tema en `init.lua`.
