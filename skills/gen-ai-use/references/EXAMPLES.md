# Example Workflows

End-to-end recipes that combine multiple `gen-ai` commands.

## Generate and iterate (image → video)

Start from an image, then animate it:

```bash
# Generate initial image
gen-ai generate --model flux-2-pro --prompt "cyberpunk cityscape at night"

# Turn it into a video
gen-ai generate --model kling-v3-pro --image ~/Downloads/result.png \
  --prompt "camera slowly pans across the city"
```

## Batch comparison across models

Run the same prompt against multiple image models side by side. Useful for picking a model for a given aesthetic:

```bash
cat > /tmp/compare.json <<'JSON'
{
  "jobs": [
    { "id": "flux",    "model": "flux-2-pro",             "prompt": "a golden retriever in a field of sunflowers" },
    { "id": "gemini",  "model": "gemini-3.1-flash-image", "prompt": "a golden retriever in a field of sunflowers" },
    { "id": "gpt",     "model": "gpt-image-1.5",          "prompt": "a golden retriever in a field of sunflowers" }
  ]
}
JSON
gen-ai batch run /tmp/compare.json -c 3 -o ./compare-out
```

Results land in `./compare-out/<id>.<ext>` plus `./compare-out/results.json`. See [BATCH.md](BATCH.md) for manifest schema details.
