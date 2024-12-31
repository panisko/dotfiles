# ZSH options
setopt glob_dots  
setopt extended_glob  

setopt append_history


# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# --- ZSH exports ---

export MYVIMRC=~/.config/nvim/init.lua
export YAZI_CONFIG_HOME=~/.config/yazi

export PATH="/opt/homebrew/opt/curl/bin:$PATH"
export PATH=/opt/homebrew/bin:$PATH
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"

# ----- ZSH autocompletion  -----
# zsh autocompetion
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# completion using arrow keys (based on history)
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward


# ----- Bat (better cat) -----

export BAT_THEME=tokyonight_night

# ---- Eza (better ls) -----

alias ls="eza --icons=always"

# ---- TheFuck -----

# thefuck alias
eval $(thefuck --alias)
eval $(thefuck --alias fk)

# ---- Zoxide (better cd) ----
eval "$(zoxide init zsh)"

alias cd="z"


# Set up fzf key bindings and fuzzy completion
eval "$(fzf --zsh)"

# --- setup fzf theme ---
fg="#CBE0F0"
bg="#011628"
bg_highlight="#143652"
purple="#B388FF"
blue="#06BCE4"
cyan="#2CF9ED"

export FZF_DEFAULT_OPTS="--color=fg:${fg},bg:${bg},hl:${purple},fg+:${fg},bg+:${bg_highlight},hl+:${purple},info:${blue},prompt:${cyan},pointer:${cyan},marker:${cyan},spinner:${cyan},header:${cyan}"


export PATH="$PATH:/Applications/WezTerm.app/Contents/MacOS"

# --- Aliases ---
alias vi='nvim'
alias vim='nvim'
alias eza='eza --icons=always'
alias ltr='eza -olrt=modified'
alias ll='eza -la --icons'
alias ls='eza -1 --icons'
alias nvc='nvim ~/dotfiles/nvim/.config/nvim/init.lua'


# --- Random vars ---
export EDITOR=nvim
source /opt/homebrew/share/powerlevel10k/powerlevel10k.zsh-theme

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
export PROJECTS=/Volumes/work/projects
export ANSIBLE_INVENTORY=${PROJECTS}/ansible/inventory/inventory.yml
