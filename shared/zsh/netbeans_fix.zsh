# === INICIO SNIPPET: FIX PARA TERMINAL DE NETBEANS ===

# 1. Variable para detectar si estamos en NetBeans
IS_NETBEANS=false
if [[ -n "$NETBEANS_USERDIR" ]] || [[ "$__CFBundleIdentifier" == "org.apache.netbeans" ]]; then
    IS_NETBEANS=true
fi

# 2. Cargar Starship en todas partes EXCEPTO en NetBeans (no soporta TrueColor nativamente)
if [[ "$IS_NETBEANS" == false ]]; then
  eval "$(starship init zsh)"
fi

# 3. Prompt minimal para NetBeans (Evita bugs de renderizado pero mantiene iconos de Git)
if [[ "$IS_NETBEANS" == true ]]; then
  setopt promptsubst             
  autoload -Uz vcs_info
  zstyle ':vcs_info:*' enable git
  zstyle ':vcs_info:git:*' formats ' %F{magenta}%f %F{green} %b%f'   
  precmd() { vcs_info }          
  PROMPT='%F{cyan} %1~%f${vcs_info_msg_0_} ➔ '
fi

# === FIN SNIPPET ===
