# Troubleshooting

## Dry-run to inspect the payload

Always the first diagnostic step. Validates parameters without sending the request and, with `--debug`, prints the full resolved payload:

```bash
gen-ai generate --model flux-2-pro --prompt "test" --dry-run --debug
```

## Common issues

| Issue | Solution |
|-------|----------|
| "Not authenticated" | Run `gen-ai login` |
| "Model not found" | Check exact ID with `gen-ai models` (e.g. `flux-2-pro`, not `flux-1.1-pro`; `seedance-i2v` is `disabled: true`) |
| "Invalid parameter" | Use `--dry-run` to validate params |
| Timeout on large video | Increase patience — video models can take minutes |
| "Credit insufficient" | Check balance with `gen-ai pricing <model>` |
| `--image (-i) is empty — check your shell variable expanded correctly.` | Your shell expanded `$VAR` to `""`. `echo $IMG`; re-export. |
| `File error: /path/to/file — file not found and not an http(s) URL` | The path doesn't exist locally and isn't a URL. Verify with `ls -la "$path"`. |
| `--shot-type is required when --multi-shot is set` | Add `--shot-type customize` (Kling V3 only allows `customize`). |
| `Shot durations sum to Ns but --duration is Ms — they must match for shot_type=customize` | Adjust either `--duration` or the `--multi-prompt-duration` values to match. |
| `Nonexistent flags: --ref-img` | Removed alias. Use `-i`, `--video-urls`, or `--audio-urls` for references. |
| "Unexpected argument: …" after `-o <path>` | `-o` is `--open` (boolean). Use `--download <dir>` (alias `--out`) to save to a directory. |
| Model selector opens despite `-m -p` | The shell variable was empty (see first row) or `-p` is missing. The auto-scripted route activates only when all required inputs are present. |
| "How do you want to use this model?" prompt for a text-only generation | You didn't pass `-p`. Either add `--prompt` (or pipe stdin) or pick `Describe with text only` in the wizard. |
| Multi-shot 400 from API ("`multi_prompt index must start from 1 and be consecutive`") | Update the CLI — `multiPrompt[].index` is now auto-numbered locally. |
| Vendor 400 ("file URL unreachable" / `audio_url failed to download`) | Try the prod alias (vendor workers reach prod uploads more reliably than stage). |

## Batch-specific issues

For batch runs, the fastest diagnostic path is:

1. Re-run the manifest with `--dry-run` to surface schema errors.
2. Inspect `<output>/results.json` and filter for `status !== "completed"` — failures carry the upstream error message.
3. Use `gen-ai batch resume <output>/results.json` to retry only the failed jobs.

See [BATCH.md](BATCH.md) for the full batch reference.
