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
| "Model not found" | Check exact ID with `gen-ai models` |
| "Invalid parameter" | Use `--dry-run` to validate params |
| Timeout on large video | Increase patience — video models can take minutes |
| "Credit insufficient" | Check balance with `gen-ai pricing <model>` |

## Batch-specific issues

For batch runs, the fastest diagnostic path is:

1. Re-run the manifest with `--dry-run` to surface schema errors.
2. Inspect `<output>/results.json` and filter for `status !== "completed"` — failures carry the upstream error message.
3. Use `gen-ai batch resume <output>/results.json` to retry only the failed jobs.

See [BATCH.md](BATCH.md) for the full batch reference.
