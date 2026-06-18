# Picsart Variable Data API — MCP Tool Reference

## Overview

The Picsart **Variable Data Content API** turns a single design **Replay** (a Picsart template/recipe) into many personalized renders by combining the template with a small data file (CSV/JSON). It is the engine behind bulk personalized marketing assets — think 50 different postcards, social ads, or product mockups produced from one template plus a spreadsheet of names, prices, photos, or copy.

A **Replay** is a saved Picsart editing recipe. It can contain placeholder fields ("variable data") of two types: `image` and `text`. You discover what fields a Replay exposes with `vd-describe-variable-data-content`, then feed values for those fields via a CSV (header row + up to 50 data rows) to generate one output per row.

- **Base URL:** `https://vd-api.picsart.io/v1`
- **Auth:** `X-Picsart-API-Key` header (handled by the MCP server)
- **Async model:** export operations return `202 Accepted` with a `transaction_id`. Poll the matching `-getresult` tool until `status` indicates completion and the result URL(s) are returned.

## Tool Index

| MCP tool | Purpose | Key inputs | Sync/async |
|---|---|---|---|
| `vd-describe-variable-data-content` | List the variable fields (image/text) defined in a Replay template | `template` / `template_url` / `template_id` | sync |
| `vd-export-replay` | Render a Replay as-is to a Print-Ready PDF | `file` / `file_url`, `format` | async → `vd-export-replay-getresult` |
| `vd-export-replay-getresult` | Fetch the finished file for a `vd-export-replay` job | `transaction_id` | poll |
| `vd-export-variable-data-content` | Bulk-render a Replay with per-row data into PDF/PNG/JPG/MP4/REPLAY | template + data CSV + `mapping`, `format` | async → `vd-export-variable-data-content-getresult` |
| `vd-export-variable-data-content-getresult` | Fetch the finished outputs for a variable-data export job | `transaction_id` | poll |
| `vd-credits-balance` | Return remaining credit balance for the API key | — | sync |

---

## Replay

### `vd-export-replay`

- **Method/Path:** `POST /export/replay`
- **Purpose:** Export a Replay file as-is (no per-row variable data) into a Print-Ready PDF. Runs asynchronously to keep performance predictable for larger files.

**Inputs** (multipart/form-data; flattened from `FileParameters` + `ExportReplayParameters`):

- `file` (binary, optional) — Source Replay file. If set, the other source parameters must be empty.
- `file_url` (string URI, optional, max length 2083) — Source Replay URL. If set, the other source parameters must be empty.
- `format` (string, optional, default `PDF`, enum: `PDF`) — Output format. Currently only `PDF` (Print-Ready PDF) is supported; more formats planned.

Exactly one source parameter (`file` or `file_url`) must be provided.

**Output:** `202` with `{ transaction_id, status }`. The rendered file is not returned inline.

**Async?** Yes. Poll `vd-export-replay-getresult` with the returned `transaction_id`.

**Tips:**
- Use this when you just want to convert a Replay to a print-ready file without injecting any variable data.
- If you need variable substitutions (per-row personalization), use `vd-export-variable-data-content` instead.
- `file_url` must be publicly reachable by Picsart's servers.

---

### `vd-export-replay-getresult`

- **Method/Path:** `GET /export/replay/{transaction_id}`
- **Purpose:** Retrieve the finished result (e.g. PDF URL) for an earlier `vd-export-replay` call.

**Inputs:**

- `transaction_id` (string, required, path) — The ID returned by `vd-export-replay`.

**Output:**
- While the job is still running: `202` with `{ transaction_id, status }` — keep polling.
- On completion: `200` with `{ data: { id, url }, status }`. `url` points at the generated file.

**Async?** This is the polling endpoint paired with `vd-export-replay`.

**Tips:**
- Poll with a small backoff (e.g. 1–3s) until you get the `200` shape with a `url`.
- The `url` is the downloadable result; persist it promptly if you need it long-term.

---

## Variable Data Content

### `vd-describe-variable-data-content`

- **Method/Path:** `POST /variable-data-content/describe`
- **Purpose:** Inspect a Replay and list its variable-data fields so you know which column headers your CSV needs. Returns each field's `tag` (name) and `type` (`image` or `text`), plus whether the Replay is animated.

**Inputs** (multipart/form-data; flattened from `TemplateParameters`):

- `template_id` (string, optional) — Source template ID from Picsart Inventory. If set, the other template source parameters must be empty.
- `template` (binary, optional) — Source Replay file. If set, the other template source parameters must be empty.
- `template_url` (string URI, optional, max length 2083) — Source Replay URL. If set, the other template source parameters must be empty.

Exactly one of `template_id`, `template`, or `template_url` must be provided.

**Output:** `200` with
```
{
  "data": {
    "tags": [ { "type": "image" | "text", "tag": "<field name>" }, ... ],
    "aminated": <bool>
  },
  "status": "..."
}
```
(Field name `aminated` is preserved verbatim from the spec; it indicates whether the Replay is animated.)

**Async?** No — this is a synchronous lookup.

**Tips:**
- Call this first when you don't know the template's schema; use the returned `tag` names as your CSV column headers and as the left-hand side of the `mapping` argument.
- `type: image` fields expect URLs (or image IDs) in the data; `type: text` fields expect plain strings.

---

### `vd-export-variable-data-content`

- **Method/Path:** `POST /export/variable-data-content`
- **Purpose:** Bulk-render a Replay against a data file (CSV) — one output per data row, with each row's values substituted into the Replay's variable fields. This is the main workhorse for personalized batch generation.

**Inputs** (multipart/form-data; flattened from `TemplateParameters` + `DataFileParameters` + `ExportVariableDataContentParameters`):

Template source (provide exactly one):
- `template_id` (string, optional) — Source template ID from Picsart Inventory.
- `template` (binary, optional) — Source Replay file.
- `template_url` (string URI, optional, max length 2083) — Source Replay URL.

Data source (provide exactly one):
- `data` (string, optional) — Source data file inline as a string. Comma separated values only. First line must be the header row with column names. Only the first 50 data rows are processed.
- `data_file` (binary, optional) — Source data CSV file as an attachment. First line must be the header row. Only the first 50 data rows are processed.
- `data_file_url` (string URI, optional, max length 2083) — URL to a CSV file. First line must be the header row. Only the first 50 data rows are processed.

Export options:
- `mapping` (string, optional) — Comma-separated mapping of fields. Use this to map CSV column names onto the Replay's variable tags when they don't match exactly.
- `format` (string, optional, default `PDF`, enum: `PDF`, `PNG`, `JPG`, `MP4`, `REPLAY`) — Output format for each row. `MP4` is useful for animated Replays; `REPLAY` re-emits a personalized Replay file rather than a flattened render.

**Output:** `202` with `{ transaction_id, status }`.

**Async?** Yes. Poll `vd-export-variable-data-content-getresult` with the returned `transaction_id`.

**Tips:**
- Hard limit: only the first 50 data rows are processed — split larger batches into multiple jobs.
- For `image`-type variables, put a publicly reachable image URL (or a Picsart image ID) in the corresponding CSV cell.
- If your CSV headers already match the Replay's variable tags exactly, you can usually omit `mapping`.
- Use `format: REPLAY` when downstream tooling expects a Replay file (e.g. for further programmatic edits) rather than a final image/PDF/video.

---

### `vd-export-variable-data-content-getresult`

- **Method/Path:** `GET /export/variable-data-content/{transaction_id}`
- **Purpose:** Retrieve the finished outputs (e.g. list of PDF URLs, one set per data row) for an earlier `vd-export-variable-data-content` call.

**Inputs:**

- `transaction_id` (string, required, path) — The ID returned by `vd-export-variable-data-content`.

**Output:**
- While the job is still running: `202` with `{ transaction_id, status }` — keep polling.
- On completion: `200` with
  ```
  {
    "status": "...",
    "data": [
      { "urls": ["<url>", ...] },
      ...
    ]
  }
  ```
  One entry per processed row; `urls` holds the generated file(s) for that row.

**Async?** This is the polling endpoint paired with `vd-export-variable-data-content`.

**Tips:**
- Order of entries in `data` corresponds to the order of rows in your CSV.
- A single row may yield multiple URLs (e.g. multi-page PDFs or multi-frame outputs); always iterate `urls`.
- Download or persist returned URLs promptly — treat them as time-limited.

---

## Utilities

### `vd-credits-balance`

- **Method/Path:** `GET /balance`
- **Purpose:** Check the remaining credits on the API key used for the call.

**Inputs:** none.

**Output:** `200` with `{ credits: <integer> }`. Response headers also expose `X-Picsart-Credit-Available` and rate-limit counters.

**Async?** No.

**Tips:**
- Call before launching a large `vd-export-variable-data-content` job so you can fail fast if credits are low (each row consumes credits).
- Useful as a connectivity / auth smoke test.

---

## End-to-end workflow

The canonical flow for bulk personalized exports is **describe → export → poll**:

1. **Describe** the Replay to discover its variable fields.
   - Call `vd-describe-variable-data-content` with `template_id`, `template`, or `template_url`.
   - Read `data.tags[]` — note each `tag` name and whether it is `image` or `text`.
2. **Build your CSV** so that its header row uses those `tag` names (or any names you'll map via `mapping`), then one row per personalized output (max 50). For `image` tags, put URLs/IDs; for `text` tags, put strings.
3. **Submit the bulk export.**
   - Call `vd-export-variable-data-content` with the same template source, your CSV (`data` / `data_file` / `data_file_url`), an optional `mapping`, and a `format` (`PDF`, `PNG`, `JPG`, `MP4`, or `REPLAY`).
   - Capture `transaction_id` from the `202` response.
4. **Poll for completion.**
   - Call `vd-export-variable-data-content-getresult` with the `transaction_id`.
   - While the response is `202`, wait briefly and retry.
   - When it returns `200`, read `data[i].urls` — one entry per CSV row.
5. **Use the URLs** (download, attach to emails, hand off to a CMS, etc.) before they expire.

For a one-off, non-personalized export the flow is simpler: `vd-export-replay` → poll `vd-export-replay-getresult` → grab `data.url`.

### Pseudo-code tool-call sequence

```
# Step 1 — discover the template's variables
describe = call_tool(
    "vd-describe-variable-data-content",
    template_url="https://example.com/postcard.replay",
)
field_names = [t["tag"] for t in describe["data"]["tags"]]
# e.g. ["first_name", "discount_code", "product_image"]

# Step 2 — prepare a CSV string (header row + up to 50 data rows)
csv_data = (
    "first_name,discount_code,product_image\n"
    "Alice,SAVE10,https://cdn.example.com/p1.jpg\n"
    "Bob,SAVE20,https://cdn.example.com/p2.jpg\n"
)

# Step 3 — kick off the bulk export
job = call_tool(
    "vd-export-variable-data-content",
    template_url="https://example.com/postcard.replay",
    data=csv_data,
    format="PDF",
    # mapping="first_name:first_name,discount_code:discount_code,product_image:product_image"
)
txid = job["transaction_id"]

# Step 4 — poll until done
while True:
    result = call_tool("vd-export-variable-data-content-getresult", transaction_id=txid)
    if result.get("data"):
        break
    sleep(2)

# Step 5 — collect the URLs (one entry per CSV row)
for row in result["data"]:
    for url in row["urls"]:
        download(url)
```

For the simpler "export Replay as PDF" flow:

```
job = call_tool("vd-export-replay", file_url="https://example.com/poster.replay", format="PDF")
txid = job["transaction_id"]

while True:
    result = call_tool("vd-export-replay-getresult", transaction_id=txid)
    if result.get("data", {}).get("url"):
        break
    sleep(2)

pdf_url = result["data"]["url"]
```
