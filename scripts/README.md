# Scripts

Esta carpeta queda reservada para scripts transversales del repositorio:
bootstrap, linking, instalacion y mantenimiento general de `~/mydotfiles`.

No usar esta carpeta como deposito general de scripts de macOS, Linux o Windows.
Los scripts especificos de un sistema operativo deben vivir en su capa:

```text
os/macos/
os/linux/
os/windows/
```

Ejemplo: un helper de X11 vive en `os/linux/x11/scripts/`, no en `scripts/`.

La lista de abajo es un inventario historico de ideas vistas en un paquete
importado. No copie el arbol completo porque muchos scripts dependen de Yabai,
Karabiner, Kanata, BetterTouchTool, OBS, rutas privadas o LaunchAgents.

## Candidatos para adaptar

- `misc/240-systemTask.sh`: abre un selector `fzf` para ejecutar scripts. Buena idea para un menu propio de mantenimiento.
- `misc/200-micMute.sh`: mute/unmute de microfono con `SwitchAudioSource`, `osascript` y Sketchybar. Interesante, pero hay que adaptarlo a tu Sketchybar Lua.
- `300-micSelector.sh` y `301-audioSelector.sh`: selectores de audio. Utiles si usas varios dispositivos.
- `misc/500-switchApp.sh`: cambia/focaliza apps usando Yabai. No sirve directo porque tu window manager es AeroSpace, pero la idea se puede reescribir para `open -a` o AeroSpace.
- `misc/550-skhdSession.sh`: abre sesiones de Kitty desde atajos. Puede servir si seguimos desarrollando tu flujo de Kitty.
- `misc/549-kittyMainSocket.sh`: detecta el socket principal de Kitty para remote control. Relevante porque tu Kitty ya usa `allow_remote_control`.
- `701-ipFinder.sh`: utilidad simple para IP/red; candidato de baja friccion.
- `600-testNotification.sh`: prueba de notificaciones; puede servir para debug de Sketchybar/scripts.

## Scripts que no conviene copiar todavia

- Scripts de Yabai: no se adaptan mientras uses AeroSpace.
- Scripts de OBS/streaming: dependen de escenas, nombres y rutas privadas.
- `400-autoPushGithub.sh`: automatiza pushes via LaunchAgent; demasiado invasivo para este repo por ahora.
- Scripts que llaman `btt://`: dependen de BetterTouchTool.
- Scripts que fuerzan un usuario concreto: deben reescribirse para `jd` o, mejor, para `$USER`.

## Regla de adopcion

Cada script que entre a este repo debe:

1. Vivir en la capa correcta: herramienta compartida, `os/`, `hosts/`,
   `profiles/` o `scripts/` transversal.
2. Tener rutas basadas en `~/mydotfiles`, `$HOME`, XDG o variables.
3. Tener README o comentario de uso.
4. No depender de Yabai/Karabiner/Kanata/skhd/BTT salvo que se indique explicitamente.
5. Poder ejecutarse manualmente antes de conectarlo a atajos o servicios.
6. No traer rutas activas de otra maquina, usuario o estructura de repo externa.
7. No guardar secretos, contrasenas, tokens ni claves privadas en Git.

Ver tambien:

- `docs/ARCHITECTURE.md`
- `docs/adr/0004-use-standard-linux-runtime-paths.md`
