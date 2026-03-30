# Dotfiles

This repository now uses Nix flakes and Home Manager as the single source of truth for packages and dotfiles.

## What it manages

- shell configuration for Zsh and Bash
- Neovim, Kitty, and tmux configuration files
- core CLI tools used by the shell config
- tmux plugin manager at `~/.tmux/plugins/tpm`

## Prerequisites

- Nix with `nix-command` and `flakes` enabled

## Install

1. Clone the repository.
2. If you previously linked files with `stow`, remove those links or let Home Manager back them up on first switch.
3. Apply the configuration:

```bash
nix run github:nix-community/home-manager/release-25.05 -- switch --flake .#panisko -b pre-nix
```

For Linux, use:

```bash
nix run github:nix-community/home-manager/release-25.05 -- switch --flake .#panisko-linux -b pre-nix
```

## Common commands

```bash
make switch
make build
make check
make update
```

Override the target if needed:

```bash
make switch FLAKE=.#panisko-linux
```


