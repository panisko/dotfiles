.PHONY: help switch build check update clean submodules

# In Makefiles, '#' is treated as a comment delimiter, so define an escaped hash
H := \#

# Auto-detect operating system and architecture
UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)

ifeq ($(UNAME_S),Darwin)
  ifeq ($(UNAME_M),arm64)
    DEFAULT_FLAKE := .$(H)panisko
  else
    DEFAULT_FLAKE := .$(H)panisko-darwin-intel
  endif
else
  ifeq ($(UNAME_M),aarch64)
    DEFAULT_FLAKE := .$(H)panisko-linux-arm
  else
    DEFAULT_FLAKE := .$(H)panisko-linux
  endif
endif

FLAKE ?= $(DEFAULT_FLAKE)
HM ?= nix run github:nix-community/home-manager/release-25.05 --

help:
	@echo "Available commands:"
	@echo "switch      - Apply Home Manager configuration (detected target: $(FLAKE))"
	@echo "build       - Build Home Manager activation package"
	@echo "check       - Evaluate flake outputs"
	@echo "update      - Update flake inputs (regenerates/updates flake.lock)"
	@echo "submodules  - Ensure git submodules (nvim, etc.) are initialized"
	@echo "clean       - Remove local build artifacts (result)"

submodules:
	@git submodule update --init --recursive

switch: submodules
	$(HM) switch --flake $(FLAKE) -b backup

build: submodules
	$(HM) build --flake $(FLAKE)

check:
	nix flake check

update:
	nix flake update

clean:
	rm -rf result
