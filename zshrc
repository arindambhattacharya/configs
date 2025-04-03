ZSH_THEME="powerlevel10k/powerlevel10k"

# Configure plugin variables before loading plugins
#
export ZVM_VI_INSERT_ESCAPE_BINDKEY=jk

# git clone https://github.com/jeffreytse/zsh-vi-mode \
#   $ZSH_CUSTOM/plugins/zsh-vi-mode
plugins=(brew git zsh-vi-mode z fzf zsh-autosuggestions zsh-syntax-highlighting)

source ~/.aliases
