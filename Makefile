.PHONY: install help clean nvim tmux

help:
	@echo "Available commands:"
	@echo "links - creates links"
	@echo "install - Install all required applications via snap"
	@echo "nvim - installs neovim"
	@echo "clean   - Clean temporary files"

install: 
	if [ $$(uname -s)  = "Linux" ]; then \
		sudo snap install nvim --classic; \
		sudo snap install node --classic; \
		sudo snap install go --classic; \
		sudo snap install podamn; \
		sudo snap install postman; \
		sudo snap install code --classic; \
	fi

clean:
	rm -rf ~/.cache/nvim
	rm -rf ~/.local/state/nvim
	rm -rf ~/.config/nvim
	rm -rf ~/.config/tmux

tmux: 
	mkdir -p ~/.config/tmux; \
	ln -sf $(PWD)/tmux/tmux.conf ~/.config/tmux/tmux.conf ;\
	[ ! -d ~/.config/tmux/plugin ] && git clone https://github.com/tmux-plugins/tpm ~/.config/tmux/plugin || true 
nvim:
	mkdir -p ~/.config; \
	[ ! -d ~/.config/nvim ] && git clone https://github.com/panisko/kickstart.nvim.git ~/.config/nvim || true

links: install nvim
	if [ $$(uname -s) = "Linux" ]; then \
		ln -sf $(PWD)/bash/bashrc ~/.bashrc; \
	else \
		ln -sf $(PWD)/zsh/zshrc ~/.zshrc; \
	fi
