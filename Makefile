.PHONY: help switch build check update clean

FLAKE ?= .#panisko
HM ?= nix run github:nix-community/home-manager/release-25.05 --

help:
	@echo "Available commands:"
	@echo "switch - Apply the Home Manager configuration"
	@echo "build  - Build the Home Manager activation package"
	@echo "check  - Evaluate flake outputs"
	@echo "update - Update flake inputs"
	@echo "clean  - Remove local build output"

switch:
	$(HM) switch --flake $(FLAKE)

build:
	$(HM) build --flake $(FLAKE)

check:
	nix flake check

update:
	nix flake update

clean:
	rm -rf result
