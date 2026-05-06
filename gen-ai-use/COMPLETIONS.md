# Shell completions

Generate tab-completion scripts for your shell.

```bash
# Bash — add to ~/.bashrc
eval "$(gen-ai completion bash)"

# Zsh — add to ~/.zshrc
eval "$(gen-ai completion zsh)"

# Fish — write directly to the completions directory
gen-ai completion fish > ~/.config/fish/completions/gen-ai.fish
```

After reloading your shell, tab-complete commands, subcommands, and flags.
