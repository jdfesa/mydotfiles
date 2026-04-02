# === INICIO SNIPPET: FIX PARA TERMINALES DE IDEs (NetBeans / VS Code) ===

# 1. Detectar si estamos en NetBeans
IS_NETBEANS=false
if [[ -n "$NETBEANS_USERDIR" ]] || [[ "$__CFBundleIdentifier" == "org.apache.netbeans" ]]; then
    IS_NETBEANS=true
fi

# 2. Desactivar p10k instant prompt si estamos en un IDE
if [[ "$TERM_PROGRAM" != "vscode" ]] && [[ "$IS_NETBEANS" == false ]]; then
  if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
    source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
  fi
fi

# 3. Cargar Powerlevel10k SOLO si NO estamos en un IDE
if [[ "$TERM_PROGRAM" != "vscode" ]] && [[ "$IS_NETBEANS" == false ]]; then
  source /usr/local/share/powerlevel10k/powerlevel10k.zsh-theme
  [[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
fi

# 4. Mostrar prompt minimalista con Git si estamos en un IDE
if [[ "$TERM_PROGRAM" == "vscode" ]] || [[ "$IS_NETBEANS" == true ]]; then
  setopt promptsubst             
  autoload -Uz vcs_info
  zstyle ':vcs_info:*' enable git
  zstyle ':vcs_info:git:*' formats '(%b)'   
  precmd() { vcs_info }          
  PROMPT='%F{cyan}%1~%f %F{green}${vcs_info_msg_0_}%f → '
fi

# === FIN SNIPPET ===