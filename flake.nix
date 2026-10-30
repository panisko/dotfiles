{
  description = "panisko dotfiles managed with Nix flakes and Home Manager";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

    home-manager = {
      url = "github:nix-community/home-manager/release-25.05";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    tpm = {
      url = "github:tmux-plugins/tpm";
      flake = false;
    };

    # Pi Coding Agent upstream flake
    pi = {
      url = "github:earendil-works/pi/stable";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ nixpkgs, home-manager, ... }:
    let
      lib = nixpkgs.lib;
      supportedSystems = [
        "aarch64-darwin"
        "x86_64-darwin"
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = f: lib.genAttrs supportedSystems (system: f nixpkgs.legacyPackages.${system});

      mkHome = { system, username, homeDirectory ? null }:
        home-manager.lib.homeManagerConfiguration {
          pkgs = import nixpkgs {
            inherit system;
            config.allowUnfree = true;
          };

          extraSpecialArgs = { inherit inputs; };

          modules = [
            ./home
            {
              home.username = username;
              home.homeDirectory =
                if homeDirectory != null
                then homeDirectory
                else if lib.hasSuffix "-darwin" system
                then "/Users/${username}"
                else "/home/${username}";
            }
          ];
        };
    in
    {
      formatter = forAllSystems (pkgs: pkgs."nixfmt-rfc-style");

      homeModules.default = import ./home;

      # Expose helper to allow custom configurations
      lib = { inherit mkHome; };

      homeConfigurations = {
        # macOS Apple Silicon (M1/M2/M3/M4) - default macOS profile
        panisko = mkHome {
          system = "aarch64-darwin";
          username = "panisko";
        };
        "panisko-darwin-arm" = mkHome {
          system = "aarch64-darwin";
          username = "panisko";
        };

        # macOS Intel
        "panisko-darwin-intel" = mkHome {
          system = "x86_64-darwin";
          username = "panisko";
        };

        # Linux x86_64 - default Linux profile
        "panisko-linux" = mkHome {
          system = "x86_64-linux";
          username = "panisko";
        };

        # Linux ARM64 (Raspberry Pi, Cloud ARM, etc.)
        "panisko-linux-arm" = mkHome {
          system = "aarch64-linux";
          username = "panisko";
        };
      };
    };
}
