# ~/.bashrc: executfzf --walker-skip=.git,.venv,node_modules,.idea --walker-root=${HOME}/projectsed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

alias vi='nvim'
export EDITOR=nvim

alias k=kubectl
source <(kubectl completion bash)
#complete -o default -F __start_kubectl k

# add Pulumi to the PATH
export PATH=$PATH:/home/piotr/.pulumi/bin
unset HTTP_PROXY
unset http_proxy
# allows to run windows apps from wsl
sudo update-binfmts --disable cli

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion



source ~/projects/sealbashfunctions/complete_alias/complete_alias
#source ~/projects/sealbashfunctions/git-completion.sh
#source ~/projects/sealbashfunctions/git-prompt.sh
export GIT_PS1_SHOWDIRTYSTATE=1
source <(helm completion bash)
source ~/projects/sealbashfunctions/kube-ps1.sh
#export PS1='[\u@\h $AZ_ACCOUNT_NAME $(kube_ps1) $(__git_ps1 " (%s)") \w ]\$ '
source ~/projects/sealbashfunctions/az_k8s_functions.sh

source ~/projects/sealbashfunctions/ssh-agent-functions.sh

eval `startOrAttachSshAgent`
#ssh-add-check-existing ~/.ssh/id_rsa
ssh-add-check-existing ~/.ssh/id_ed25519
ssh-add-check-existing ~/.ssh/azuredevops-tksteel_id_rsa

eval "$(fzf --bash)"

set -o vi

vv() {
    if [ -z "$1" ]; then
	fzf  --walker-skip=.git,.venv,node_modules,.idea --walker-root=${HOME}/projects --bind 'enter:become(vim {})'
	else
		nvim "$@"
	fi
}
alias cdp='cd ~/projects/'

#cd ~/projects && tmux

# Update PS1 to include the Git branch on the right
function pc {
  #[ -d .git ] && git name-rev --name-only @
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

PS1='\e];\s\a\n\e[33m\w \e[36m$(pc)\e[m\n$ '
alias gcm='git commit -m'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gpl='git pull'
alias gf='git fetch'
alias gplr='git pull --rebase'
alias glg='git log --oneline --graph --decorate'
alias gss='git status -s'
alias gd='git diff'
alias gph='git push'
alias gpsu='git push --set-upstream origin $(git rev-parse --abbrev-ref HEAD)'
alias gbr='git branch'
alias gad='git add'

