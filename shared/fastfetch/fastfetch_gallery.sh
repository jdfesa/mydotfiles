#!/usr/bin/env bash

# Inicialización
current_dir=""
declare -a PRESETS

echo "Cargando presets..."

# ==============================================================================
# 1. CARGA DE PRESETS EN MEMORIA
#    Parsea la salida de fastfetch --list-presets y construye un array.
# ==============================================================================
while IFS= read -r line; do
  # Ignorar líneas vacías
  [[ -z "$line" ]] && continue

  # 1. Si termina en /, actualizamos el directorio actual (ej: "examples/")
  if [[ "$line" == */ ]]; then
    current_dir=$(echo "$line" | xargs) # xargs trim whitespace
    continue
  fi

  # 2. Si es un archivo .jsonc, lo agregamos al array
  if [[ "$line" == *".jsonc"* ]]; then
    # Limpiamos caracteres de árbol (barras verticales y espacios al inicio)
    clean_name=$(echo "$line" | sed 's/^[ |]*//')

    if [[ "$line" == *"|"* ]]; then
      # Pertenece a la carpeta actual
      full_path="${current_dir}${clean_name}"
    else
      # Está en la raíz
      full_path="${clean_name}"
      # Resetear current_dir si volvemos a la raíz (depende del formato de salida, 
      # pero por seguridad asumimos que los root items no tienen indentación)
      current_dir="" # Esto podría necesitar ajuste si fastfetch mezcla, pero usualmente agrupa.
                     # Para fastfetch actual, la estructura es jerárquica.
                     # Sin embargo, la lógica original asumía que si no hay pipe, es root.
    fi
    
    PRESETS+=("$full_path")
  fi
done < <(fastfetch --list-presets)

total_presets=${#PRESETS[@]}

if [ "$total_presets" -eq 0 ]; then
  echo "Error: No se encontraron presets de fastfetch."
  exit 1
fi

# ==============================================================================
# 2. BUCLE DE NAVEGACIÓN
# ==============================================================================
index=0

while true; do
  clear
  preset="${PRESETS[$index]}"

  # UI Header
  echo "================================================================================"
  echo "  🎨 FASTFETCH GALLERY  |  Tema $((index+1)) de $total_presets"
  echo "  📂 Preset: $preset"
  echo "================================================================================"
  echo "  [➡ / n / Enter] Siguiente   [⬅ / p] Anterior   [q] Salir"
  echo "--------------------------------------------------------------------------------"
  echo ""

  # Ejecutar fastfetch con filtro de IP y forzando color
  # --pipe false fuerza a fastfetch a emitir códigos de color aunque detecte pipe
  # sed filtra patrones de IP
  fastfetch --config "$preset" --pipe false | sed -E 's/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/HIDDEN_IP/g'

  echo ""
  echo "--------------------------------------------------------------------------------"
  read -rsn1 -p "  Comando >> " key

  # Lógica de Control
  case "$key" in
    q|Q)
      echo -e "\n\n👋 ¡Hasta luego!"
      break
      ;;
    p|P|B|b|$'\x1b') # Detectar flechas es complejo en bash puro con read -n1, pero 'p'/'b' funciona
      # Si es secuencia de escape (flechas), leemos más
      if [[ "$key" == $'\x1b' ]]; then
        read -rsn2 -t 0.1 key2
        if [[ "$key2" == "[D" ]]; then # Flecha Izquierda
             ((index--))
        elif [[ "$key2" == "[C" ]]; then # Flecha Derecha
             ((index++))
        fi
      else
        ((index--))
      fi
      ;;
    *)
      # Por defecto (Enter, Espacio, n, cualquier otra) avanza
      ((index++))
      ;;
  esac

  # Navegación Circular (Carousel)
  if [ "$index" -ge "$total_presets" ]; then
    index=0
  elif [ "$index" -lt 0 ]; then
    index=$((total_presets - 1))
  fi

done