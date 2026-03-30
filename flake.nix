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
  };

  outputs = inputs@{ nixpkgs, home-manager, ... }:
    let
      lib = nixpkgs.lib;
      supportedSystems = [ "aarch64-darwin" "x86_64-linux" ];
      forAllSystems = f: lib.genAttrs supportedSystems (system: f nixpkgs.legacyPackages.${system});

      mkHome = { system, username }:
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
                if lib.hasSuffix "-darwin" system
                then "/Users/${username}"
                else "/home/${username}";
            }
          ];
        };
    in
    {
      formatter = forAllSystems (pkgs: pkgs."nixfmt-rfc-style");

      homeModules.default = import ./home;

      homeConfigurations = {
        panisko = mkHome {
          system = "aarch64-darwin";
          username = "panisko";
        };

        "panisko-linux" = mkHome {
          system = "x86_64-linux";
          username = "panisko";
        };
      };
    };
}