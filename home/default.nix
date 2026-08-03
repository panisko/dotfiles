{ config, lib, pkgs, inputs, ... }:

let
  homeDir = config.home.homeDirectory;
in
{
  home.stateVersion = lib.mkDefault "25.05";

  programs.home-manager.enable = true;

  xdg.enable = true;

  home.packages = with pkgs; [
    bashInteractive
    bat
    bc
    coreutils
    eza
    fd
    fzf
    gawk
    gcc
    git
    gnugrep
    go
    jq
    kubectl
    kitty
    luarocks
    neovim
    nodejs_22
    openjdk17
    pass
    playerctl
    podman
    python3
    python3Packages.pip
    ripgrep
    ruby_3_4
    talosctl
    thefuck
    tmux
    unzip
    uv
    yazi
    zoxide
    zsh
    pkgs."kubernetes-helm"
    pkgs."zsh-autosuggestions"
    pkgs."zsh-powerlevel10k"
    pkgs."zsh-syntax-highlighting"
  ];

  home.sessionPath = [
    "${homeDir}/.cargo/bin"
    "${homeDir}/.local/bin"
    "${homeDir}/.lmstudio/bin"
  ];

  home.sessionVariables = {
    BAT_THEME = "tokyonight_night";
    EDITOR = "nvim";
    MYVIMRC = "${homeDir}/.config/nvim/init.lua";
    POWERLEVEL10K_DIR = "${pkgs."zsh-powerlevel10k"}/share/zsh-powerlevel10k";
    PROJECTS = if pkgs.stdenv.isDarwin then "/Volumes/work/projects" else "${homeDir}/projects";
    XDG_CONFIG_HOME = "${homeDir}/.config";
    YAZI_CONFIG_HOME = "${homeDir}/.config/yazi";
    ZSH_AUTOSUGGESTIONS_DIR = "${pkgs."zsh-autosuggestions"}/share/zsh-autosuggestions";
    ZSH_SYNTAX_HIGHLIGHTING_DIR = "${pkgs."zsh-syntax-highlighting"}/share/zsh-syntax-highlighting";
  };

  home.file = {
    ".bashrc".source = ../bash/bashrc;
    ".p10k.zsh".source = ../p10k/.p10k.zsh;
    ".tmux/plugins/tpm" = {
      source = inputs.tpm;
      recursive = true;
    };
    ".zshrc".source = ../zsh/zshrc;
  };

  xdg.configFile = {
    "kitty" = {
      source = ../kitty/.config/kitty;
      recursive = true;
    };
    "nvim/doc" = {
      source = ../nvim/doc;
      recursive = true;
    };
    "nvim/init.lua".source = ../nvim/init.lua;
    "nvim/lua" = {
      source = ../nvim/lua;
      recursive = true;
    };
    "tmux/tmux.conf".source = ../tmux/tmux.conf;
  };
}