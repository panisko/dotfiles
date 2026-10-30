# Dotfiles

A declarative, cross-platform development environment for **macOS** and **Linux**, managed using **Nix Flakes** and **Home Manager**.

---

## Table of Contents

1. [Managed Components](#what-it-manages)
2. [Setting Up a Brand New Machine](#setting-up-a-brand-new-machine)
   - [Step 1: Install System Prerequisites](#step-1-install-system-prerequisites)
   - [Step 2: Install Nix](#step-2-install-nix)
   - [Step 3: Enable Nix Flakes](#step-3-enable-nix-flakes)
   - [Step 4: Clone the Repository (with Submodules)](#step-4-clone-the-repository-with-submodules)
   - [Step 5: Apply Configuration with Home Manager](#step-5-apply-configuration-with-home-manager)
   - [Step 6: Post-Installation Steps](#step-6-post-installation-steps)
3. [Deep Dive: How It Works with Nix Flakes](#deep-dive-how-it-works-with-nix-flakes)
   - [Why Nix Flakes?](#why-nix-flakes)
   - [Flake Structure & Architecture](#flake-structure--architecture)
   - [The Role of `flake.lock` (Deterministic Repeatability)](#the-role-of-flakelock-deterministic-repeatability)
   - [Cross-Platform Architecture Support](#cross-platform-architecture-support)
   - [Adding or Customizing a User Profile](#adding-or-customizing-a-user-profile)
4. [Day-to-Day Operations & Makefile](#day-to-day-operations--makefile)
5. [Troubleshooting & FAQ](#troubleshooting--faq)

---

## What It Manages

- **Shells**: Zsh (with Powerlevel10k, autocompletions, syntax highlighting, fzf integration, zoxide) and Bash.
- **Editor**: Neovim (modular Kickstart configuration via Git submodule at `nvim/`).
- **Terminal & Multiplexer**: Kitty terminal emulator and Tmux (with TPM plugins, Tokyo Night theme, vim-tmux navigator).
- **Core Toolchain**: `ripgrep`, `fd`, `bat`, `eza`, `fzf`, `jq`, `yazi`, `uv`, `kubectl`, `podman`, `helm`, `pass`, etc.
- **Clipboard & Media**: Seamless OS clipboard integration (`pbcopy`/`pbpaste` on macOS; `wl-clipboard`/`xclip` on Linux) and MPRIS integration (`playerctl` on Linux).

---

## Setting Up a Brand New Machine

Follow these steps to bootstrap a fresh machine from scratch into a fully configured workstation.

### Step 1: Install System Prerequisites

#### On macOS
Open Terminal and install Apple Command Line Tools (provides `git`, `curl`, `clang`):
```bash
xcode-select --install
```

#### On Linux (Debian / Ubuntu / Fedora / Arch)
Install `curl`, `git`, and build utilities:
```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y curl git build-essential

# Fedora / RHEL
sudo dnf install -y curl git make gcc

# Arch Linux
sudo pacman -Syu --needed curl git base-devel
```

---

### Step 2: Install Nix

The recommended and fastest way to install Nix with multi-user daemon mode and sandboxing enabled is the Determinate Systems installer:

```bash
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install
```

*(Alternatively, the official Nix installer is: `sh <(curl -L https://nixos.org/nix/install) --daemon`)*

Once installed, restart your terminal or source the Nix environment:
```bash
# macOS & Linux (standard multi-user daemon)
. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
```

Verify that Nix is running:
```bash
nix --version
```

---

### Step 3: Enable Nix Flakes

If you used the Determinate Systems installer, flakes and the `nix-command` CLI are **already enabled by default**.

If you used the official Nix installer, ensure flakes are enabled by adding the experimental flags:
```bash
mkdir -p ~/.config/nix
cat <<EOF >> ~/.config/nix/nix.conf
experimental-features = nix-command flakes
EOF
```

---

### Step 4: Clone the Repository (with Submodules)

> **Important**: This repository uses a Git submodule for Neovim (`nvim`). Clone recursively so the editor configurations are fully populated:

```bash
git clone --recursive https://github.com/panisko/dotfiles.git ~/projects/dotfiles
cd ~/projects/dotfiles
```

If you already cloned without `--recursive`, initialize submodules manually:
```bash
git submodule update --init --recursive
```

---

### Step 5: Apply Configuration with Home Manager

The `Makefile` automatically inspects your operating system (`Darwin` vs `Linux`) and CPU architecture (`arm64` vs `x86_64`) to select the appropriate configuration target.

Run:
```bash
make switch
```

This executes:
1. Submodule integrity check (`git submodule update --init --recursive`).
2. Home Manager switch with automatic file backup (`-b backup`), safely saving any conflicting pre-existing config files with a `.backup` suffix instead of failing.

#### Manual or Explicit Target Execution

If you prefer to invoke Nix directly or need an explicit profile:

```bash
# macOS (Apple Silicon: M1 / M2 / M3 / M4)
nix run github:nix-community/home-manager/release-25.05 -- switch --flake .#panisko -b backup

# macOS (Intel)
nix run github:nix-community/home-manager/release-25.05 -- switch --flake .#panisko-darwin-intel -b backup

# Linux (x86_64)
nix run github:nix-community/home-manager/release-25.05 -- switch --flake .#panisko-linux -b backup

# Linux (ARM64, Raspberry Pi, Asahi Linux, Cloud ARM)
nix run github:nix-community/home-manager/release-25.05 -- switch --flake .#panisko-linux-arm -b backup
```

---

### Step 6: Post-Installation Steps

1. **Set Default Shell to Zsh**:
   ```bash
   # Add Home Manager zsh to allowed shells if needed
   command -v zsh | sudo tee -a /etc/shells
   chsh -s "$(command -v zsh)"
   ```
2. **Install Nerd Font for Kitty / Terminal**:
   The prompt (Powerlevel10k) and terminal icons (eza, yazi, neovim) require a Nerd Font (e.g., *JetBrainsMono Nerd Font* or *MesloLGS NF*).
   - macOS: Install via Homebrew `brew install --cask font-jetbrains-mono-nerd-font` or download from [Nerd Fonts](https://www.nerdfonts.com/).
   - Linux: Download TTF files to `~/.local/share/fonts/` and run `fc-cache -fv`.
3. **Initialize Tmux Plugins (TPM)**:
   Launch tmux:
   ```bash
   tmux
   ```
   Press `Ctrl-a` followed by `I` (capital `i`) to fetch and install tmux plugins declared in `tmux.conf`.
4. **Initialize Neovim**:
   Run `nvim`. Lazy.nvim will automatically bootstrap and install all configured Lua plugins.

---

## Deep Dive: How It Works with Nix Flakes

### Why Nix Flakes?

Traditional dotfiles setups rely on imperative symlink scripts or tools like GNU Stow, coupled with ad-hoc package managers (`brew`, `apt`, `pacman`). This leads to several issues:
- **Configuration Drift**: Packages installed on Machine A are forgotten on Machine B.
- **Platform Incompatibilities**: Linux packages and paths break on macOS and vice versa.
- **Non-Hermetic Installs**: Running `brew install` or `apt install` 6 months later pulls different package versions that might break configurations.

**Nix Flakes** solves this by providing:
1. **Declarative State**: Everything (tools, shell variables, symlinks, themes) is defined in pure code.
2. **Deterministic Inputs**: External inputs (nixpkgs channel, Home Manager release, TPM repository) are pinned in `flake.lock`.
3. **Hermetic Builds**: Nix packages are built in isolated sandboxes and installed into `/nix/store/<hash>-<name>`.
4. **Reproducibility**: Applying this flake on any machine running Nix will yield the exact same environment.

---

### Flake Structure & Architecture

```
dotfiles/
├── flake.nix              # Top-level flake manifest (inputs, outputs, targets)
├── flake.lock             # Exact SHA-256 commit pins for reproducible builds
├── Makefile               # Convenience commands with OS auto-detection
├── home/
│   └── default.nix        # Core Home Manager configuration (packages, env vars, links)
├── zsh/
│   └── zshrc              # Portable Zsh configuration
├── bash/
│   └── bashrc             # Portable Bash configuration
├── tmux/
│   └── tmux.conf          # Tmux configuration (with TPM fallback)
├── kitty/
│   └── .config/kitty/     # Kitty terminal configuration
├── nvim/                  # Git submodule (modular Neovim Kickstart)
└── p10k/
    └── .p10k.zsh          # Powerlevel10k theme configuration
```

#### How `flake.nix` Connects with Home Manager

1. **`inputs`**: Pinned upstream sources:
   - `nixpkgs`: Base package repository (`nixos-25.05`).
   - `home-manager`: User-environment manager (`release-25.05`).
   - `tpm`: Tmux Plugin Manager source repository.
2. **`outputs`**: Exposes:
   - `homeConfigurations`: A map of target profiles (`panisko`, `panisko-linux`, etc.).
   - `formatter`: Code formatting using `nixfmt-rfc-style`.
   - `lib.mkHome`: Reusable builder function that instantiates Home Manager for any `system` and `username`.

---

### The Role of `flake.lock` (Deterministic Repeatability)

When you run `nix flake update`, Nix generates or updates `flake.lock`. This file locks:
- The exact git commit hash of `nixpkgs`.
- The exact commit hash of `home-manager`.
- The exact commit hash of `tpm`.

Because `flake.lock` is committed to version control:
- Every machine pulls the exact same package versions.
- Updates are intentional: you upgrade your entire toolchain across all machines by running `make update` and committing the updated `flake.lock`.

---

### Cross-Platform Architecture Support

This repository supports four primary system targets:

| Target Identifier | OS | Architecture | Hardware Example |
| :--- | :--- | :--- | :--- |
| `panisko` / `panisko-darwin-arm` | macOS | `aarch64-darwin` | Apple Silicon (M1/M2/M3/M4) |
| `panisko-darwin-intel` | macOS | `x86_64-darwin` | Intel Mac |
| `panisko-linux` | Linux | `x86_64-linux` | Intel/AMD PC, Server, WSL2 |
| `panisko-linux-arm` | Linux | `aarch64-linux` | Raspberry Pi 4/5, AWS Graviton, Asahi |

#### Cross-Platform Adaptations in Code:
- **Paths**: `$HOME/projects` is the cross-platform standard. On machines with dedicated mount points (like `/Volumes/work/projects`), `zshrc` automatically detects and uses it without failing on systems without it.
- **Clipboard**: On macOS, `pbcopy` and `pbpaste` work natively. On Linux, `wl-clipboard` (Wayland) and `xclip` (X11) are automatically installed and aliased to `pbcopy`/`pbpaste`.
- **System-Specific Packages**: Linux-only utilities (`playerctl`, `wl-clipboard`, `xclip`) are declared conditionally via `lib.optional pkgs.stdenv.isLinux`.
- **Shell Theme & Autocomplete**: Sourcing checks `$POWERLEVEL10K_DIR`, `$ZSH_AUTOSUGGESTIONS_DIR`, and `$ZSH_SYNTAX_HIGHLIGHTING_DIR` supplied by Nix before falling back to system paths.

---

### Adding or Customizing a User Profile

If your username on a new machine is not `panisko` (e.g., `alice` on an M3 Mac or `ubuntu` on a cloud VM), you can easily declare it in `flake.nix`:

Open `flake.nix` and add your configuration to `homeConfigurations`:

```nix
homeConfigurations = {
  # Existing configurations...
  
  # Your custom machine:
  "alice" = mkHome {
    system = "aarch64-darwin"; # or "x86_64-linux"
    username = "alice";
  };
};
```

Apply it with:
```bash
make switch FLAKE=.#alice
```

---

## Day-to-Day Operations & Makefile

| Command | Action | Description |
| :--- | :--- | :--- |
| `make switch` | **Apply Config** | Checks submodules and applies Home Manager configuration |
| `make build` | **Dry-Run Build** | Builds the generation into `./result` without activating |
| `make check` | **Validate Flake** | Evaluates and type-checks flake outputs |
| `make update` | **Update Packages** | Updates flake inputs to latest upstream and updates `flake.lock` |
| `make submodules` | **Sync Submodules** | Updates all git submodules recursively |
| `make clean` | **Clean Artifacts** | Deletes `./result` symlink |

#### Overriding Flake Target
```bash
make switch FLAKE=.#panisko-linux
```

#### Rolling Back
Home Manager retains previous generations in the Nix store. If a change breaks your environment:
```bash
# List previous generations
home-manager generations

# Activate a previous generation
~/.local/state/nix/profiles/home-manager-*-link/activate
```

---

## Troubleshooting & FAQ

#### 1. "error: getting status of '.../nvim/init.lua': No such file or directory"
You cloned the repository without git submodules. Run:
```bash
git submodule update --init --recursive
```

#### 2. "Existing file '...' would be overwritten by Home Manager"
Home Manager avoids clobbering existing unmanaged files. Pass `-b backup` (the default in `make switch`) to automatically rename conflicting files to `*.backup`.

#### 3. "command not found: nix"
Ensure the Nix daemon profile is loaded in your current shell:
```bash
. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
```
Also verify `/nix/var/nix/profiles/default/bin` or `~/.nix-profile/bin` is in your `$PATH`.

#### 4. Tmux plugins are not loading
In tmux, press `Ctrl-a` then `Shift-i` (`prefix + I`) to fetch TPM plugins. Verify that `~/.tmux/plugins/tpm` exists.
