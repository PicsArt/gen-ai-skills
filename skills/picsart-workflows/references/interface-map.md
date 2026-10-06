# Picsart interface map

All `picsart-*` skills use one MCP server. Use this file to pick a tool group and to follow the shared execution rules.

## Server

| Field | Value |
| --- | --- |
| Name | `picsart` |
| URL | `https://api.picsart.com/gen-ai/mcp` |
| Auth | OAuth. The host opens the sign-in on first connect. No API key. |

If the server is not connected, tell the user to connect it. Continue planning work that needs no tool call. Never invent tool results or renders.

## Discover tools at runtime

The names below identify tools. They are not a fixed host namespace.
The host may prefix them with a server namespace (for example `mcp__<server>__` before the tool name).
Read the live tool list and each tool's schema before the first call.
Call a tool only when the connected server lists it.
Model catalogs change. Do not hard-code a model's duration, reference count, ratio, or resolution from an example.

## Tool groups

| Group | Tools |
| --- | --- |
| Models and catalog | `picsart_model_catalog`, `picsart_list_models` (visual picker), `picsart_model_choice`, `picsart_model_params` |
| Preflight and prompts | `picsart_preflight`, `picsart_prompt_verify` |
| Generate and jobs | `picsart_generate`, `picsart_job_status`, `picsart_render_monitor` |
| Dedicated edits | `picsart_remove_bg`, `picsart_change_bg`, `picsart_enhance`, `picsart_vectorize` |
| Drive and assets | `picsart_drive`, `picsart_list_assets`, `picsart_asset_review`, `picsart_save_asset`, `picsart_delete_asset`, `picsart_view_image` |
| Account | `picsart_credits` |
| Local file upload | `picsart_media_upload` (opens an upload widget) |
| Scenes, analysis, export | `picsart_media_*` (for example `picsart_media_quickstart`, `picsart_media_get_scene_schema`, `picsart_media_validate_scene`, `picsart_media_export`, `picsart_media_contact_sheet`), `picsart_scene_editor` |
| Film boards | `picsart_film_setup`, `picsart_shotlist_board`, `picsart_film_compile_prompt`, `picsart_film_compile_asset_prompt` |
| Motion boards | `picsart_motion_setup`, `picsart_scene_editor` |

## Generation chain

1. `picsart_model_params({ model })`: read the parameter schema for the actual model.
2. `picsart_preflight({ model, params })`: validate the candidate payload and estimate credits. `params` includes `prompt`. `credits: null` means the price is unavailable.
3. `picsart_generate({ model, prompt, ...params, async: true })`: submit. Set `async: true` explicitly for recoverable media jobs. Text models stay synchronous.
4. `picsart_job_status({ job, model, prompt?, saveToDrive? })`: poll the original job handle until a terminal state.

Inputs use camel case, such as `aspectRatio`. `extra` carries supported model-specific parameters.
The job handle has `id` and `workflow`. Preserve it in its original shape.
Preserve save settings and inspect the returned save status. Do not promise that polling cannot write Drive metadata.

`picsart_media_*` analysis and export tools return their own receipt. Follow `tools.jobStatus` from that receipt. Do not assume that `picsart_job_status` accepts it.

## Local inputs

Tools take URLs, not local paths. For a local file, call `picsart_media_upload({ accept, purpose })`. It opens a widget and does not return the URL in the same call. Read the user's next turn and widget context for the URL. Do not put a local path in a media URL field.

## Film assets

- Browse project references with `picsart_list_assets({ projectFolderUid, scope: "library" })`. Use `scope: "assets"` for working versions or `"all"` for both. Without `projectFolderUid` it reads the global flat Film Assets folder only.
- Browse ordinary media with `picsart_drive({ action: "list", folderUid, page, pageSize })`. Follow pagination.
- Review with `picsart_asset_review({ purpose, assets: [{ url, tag, label, ... }] })`. Read the verdict from widget context on the next turn. Opening the board or silence is not approval.
- Lock with `picsart_save_asset({ assetType, name, tag, portraitUrl, descriptor, sheetVersion, status: "locked", projectFolderUid? })`. Only `locked: true` in the result confirms the lock. `saved: true` alone does not.

See [Drive Library](drive-library.md), [media production](media-production.md), and [remote resources](remote-resources.md).

## Credits and paid calls

- Check `picsart_credits({})` or the preflight estimate before a large or strict-budget job.
- Do not retry a paid call after a credit or storage error until the user says they are ready.
- Do not retry a paid call whose acceptance is ambiguous. Poll the original handle.
- A host timeout can leave a paid job active. A timeout does not mean generation failed. Do not submit again to recover a missing response.
- Plan, credit, or Drive storage links in a result or error may be shared with the user exactly as returned.
- Preserve asset URLs verbatim. A URL's shape does not establish its lifetime; use result metadata.

## Non-MCP alternatives

Use these only when the user asks for a terminal or code route. They are not equivalent to every MCP tool.

| Task | gen-ai CLI | `@picsart/ai-sdk` |
| --- | --- | --- |
| Connect | `gen-ai login`; `gen-ai whoami` | `createClient({ apiUrl, fetch })` |
| Discover | `gen-ai models`; `gen-ai models info MODEL --json` | `catalog`; `Model(id).meta()` |
| Schema | `gen-ai validate --model MODEL --schema` | `Model(id).params().toSchema()` |
| Validate | `gen-ai validate --model MODEL --file payload.json --json` | `Model(id).validate(params)` |
| Price | `gen-ai pricing MODEL --json` | `ai.getCredits(model, params)` (may return `null`) |
| Generate media | `gen-ai generate --model MODEL --prompt-file prompt.txt --no-input --json --no-open` | `ai.generate(model, params)`; or `ai.submit` then `ai.result(model, id)` |
| Recover media | No generic job-poll command | `ai.result(model, id)`; `ai.subscribe(model, id)` |
| Balance | `gen-ai credits` | Not established |
| Drive | `gen-ai list`, `upload`, `download`, `upload-to-drive` | `ai.drive` when configured |

- CLI flags use kebab case (`--aspect-ratio`). Check each command's installed help before you build a request.
- `gen-ai validate --json` can succeed with empty stdout. Use exit code 0 as success. Validation accepts unknown keys; build requests from the schema.
- `gen-ai login` opens an external browser.
- CLI `--max-cost` blocks only a known excessive estimate; with unknown pricing it warns and continues.
- `gen-ai batch run` keeps async handles only in memory. Do not use it when durable submission receipts are required.
- `ai.submit` returns a generation ID string. Do not exchange it with an MCP job handle.
- `gen-ai upload PATH --json` returns per-file `url`, `driveUid`, and error fields. Inspect every result.
- For CLI usage detail, see the [gen-ai-use](../../gen-ai-use/SKILL.md) skill.
