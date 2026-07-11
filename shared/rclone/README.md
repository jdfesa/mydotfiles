# Rclone

`rclone-sync` conserva el flujo interactivo encontrado en la maquina Arch, pero
evita rutas personales fijas y ejecuta primero una simulacion.

Por defecto sincroniza entre `gdrive:/` y `$HOME/MyDrive`:

```sh
rclone-sync pull
rclone-sync push
```

Ambos comandos usan `--dry-run`. Para aplicar los cambios:

```sh
rclone-sync pull --apply
rclone-sync push --apply
```

Se pueden cambiar los extremos sin modificar el script:

```sh
RCLONE_REMOTE=backup:/Documentos RCLONE_LOCAL_DIR="$HOME/Documents" \
  rclone-sync pull
```

La configuracion y las credenciales de Rclone permanecen fuera de Git.
