# Audio en Linux

Diagnostico y recuperacion de audio especificos de Linux. Esta capa no depende
de XFCE, Hyprland, X11 ni Wayland: ALSA expone el hardware y PipeWire con
WirePlumber administra los dispositivos de la sesion del usuario.

## Arch Desktop: Realtek ALC892

Solucion validada auditivamente el 2026-08-12 con auriculares analogicos en el
conector **verde trasero**. El usuario confirmo reproduccion correcta en
YouTube.

### Sintomas

- YouTube mostraba que no podia renderizar audio y sugeria reiniciar el equipo.
- PipeWire elegia `Built-in Audio Digital Stereo (IEC958)` aunque los
  auriculares estaban conectados por jack.
- Al forzar `output:analog-stereo`, el sink aparecia pero `pw-play` fallaba con
  `no target node available`.
- Reiniciar PipeWire y WirePlumber no alcanzaba: el perfil volvia a S/PDIF.

### Causa

El ALC892 de esta maquina informa `Line Out` y `Headphones` como no disponibles.
WirePlumber descarta por eso el perfil analogico normal y prefiere S/PDIF. A
nivel ALSA, ademas, el control `Front` correspondiente al conector verde
trasero estaba silenciado.

Los conectores traseros tienen funciones distintas:

- verde: salida analogica (`Front`, nodo HDA `0x14`);
- rosa: entrada de microfono;
- azul: entrada de linea.

El conector verde frontal para auriculares corresponde al control `Headphone`
y al nodo HDA `0x1b`.

### Solucion validada

1. Usar el perfil `pro-audio`, que expone directamente los PCM fisicos y no
   depende de la deteccion defectuosa del jack:

   ```sh
   pactl set-card-profile alsa_card.pci-0000_00_1b.0 pro-audio
   ```

2. Elegir la salida analogica `hw:1,0`, no la digital `hw:1,1`:

   ```sh
   wpctl status
   wpctl set-default ID_DEL_SINK_ANALOGICO
   ```

   El nombre estable validado mediante la compatibilidad PulseAudio es:

   ```text
   alsa_output.pci-0000_00_1b.0.pro-output-0
   ```

3. Evitar que ALSA silencie la salida trasera y dejar el hardware a 0 dB. El
   volumen cotidiano se controla una sola vez desde PipeWire:

   ```sh
   amixer -c 1 sset 'Auto-Mute Mode' Disabled
   amixer -c 1 sset Master 100% unmute
   amixer -c 1 sset Front 100% unmute
   amixer -c 1 sset Headphone 100% unmute
   wpctl set-volume @DEFAULT_AUDIO_SINK@ 0.50
   ```

   No conviene poner PipeWire, `Master` y `Front` todos al 50 %, porque sus
   atenuaciones se multiplican y el resultado puede quedar casi inaudible.

4. Probar explicitamente el sink analogico:

   ```sh
   pw-play \
     --target=alsa_output.pci-0000_00_1b.0.pro-output-0 \
     /usr/share/sounds/alsa/Front_Center.wav
   ```

5. Si un navegador ya habia creado su stream contra el sink incorrecto,
   recargar la pestaña o reiniciar el navegador.

### Verificacion

```sh
pactl info | grep 'Default Sink'
pactl list short sinks
wpctl status
amixer -c 1 sget Master
amixer -c 1 sget Front
```

Estado final validado:

- perfil de la placa Realtek: `pro-audio`;
- sink: `pro-output-0` / `ALC892 Analog` / `hw:1,0`;
- ALSA `Master` y `Front`: 100 %, sin mute;
- `Auto-Mute Mode`: desactivado;
- volumen efectivo PipeWire: 50 %;
- salida fisica: jack verde trasero.

Los identificadores numericos de `wpctl` cambian al reiniciar los servicios. Se
debe identificar nuevamente el sink analogico por nombre; no hay que copiar un
ID numerico viejo. Falta validar si WirePlumber y ALSA restauran todo este
estado despues de reiniciar la computadora. Hasta entonces, esta guia es el
procedimiento manual de recuperacion.

## Sesiones graficas simultaneas

No conviene mantener XRDP/XFCE y Hyprland activos simultaneamente para el mismo
usuario mientras se diagnostica audio. Ambas sesiones comparten los servicios
systemd de usuario, D-Bus, PipeWire y WirePlumber; una aplicacion remota puede
crear streams o cambiar dispositivos de la sesion local.
