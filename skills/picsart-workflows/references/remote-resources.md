# Remote resources and reusable libraries

## Find before creating

Use remote storage as the source of reusable media and editable work. Start with supplied assets and explicit project references. Then search the [shared Drive Library](drive-library.md) for characters, props/products, locations/sets, and brands. Follow folder IDs and pagination; names are not unique identities. A failed read does not mean the library is empty.

The canonical shared paths are `/Assets/Library/Characters`, `/Assets/Library/Props`, `/Assets/Library/Locations`, and `/Assets/Library/Brands`. Resolve their IDs in the current account. Do not create folders while discovering resources. Use a supplied project folder for working media and revisions. Do not invent shared category paths for voices, music, or templates; discover the existing organization or choose a project destination within the requested storage task.

The shared library and a film project's locked `Library` are different stores. `picsart_list_assets({ projectFolderUid, scope: "library" })` reads a film's locked references. It does not search the shared library. Ordinary generation saves and film registry saves do not automatically publish resources into shared categories.

## Keep reusable identity

A shared asset folder ID is the asset identity. Preserve its category, description, file IDs, plain media URLs, and available roles. Native role/primary tags take precedence over filename conventions, as explained in the library contract. Reduced MCP/SDK listings can omit metadata; do not guess that missing tags are absent.

Keep visual views, gridded sheets, archived source sheets, and voice carriers separate. Choose only references supported by the selected model or scene. Record selection by ID and version instead of saying “use the latest character” without specifying which one. A stored character is a reusable reference; storage does not train an identity model or guarantee generated continuity.

Suggested resource records are workflow state, not a new mandatory Drive schema:

| Field | Purpose |
| --- | --- |
| Asset folder ID and category | Stable shared identity and resource type |
| File IDs, URLs, and roles | Selected view, sheet, voice carrier, or artwork |
| Version and source identity | Connect a new variant to the original |
| Description and fixed traits | Reuse character, prop, location, or brand constraints consistently |
| Approval state and evidence | Distinguish proposed, reviewed, and locked resources |
| Usage restrictions, when supplied | Preserve resource-specific use limits |
| Dependent scene/shot IDs | Identify work affected by a changed resource |

Keep this record as a JSON file in the workspace project folder. Do not invent tag fields in a reduced response or require DNA JSON for discovery.

`picsart_drive` file attributes (`action: "update"`) do not set native role/primary tags or an existing folder's description. When those fields are required, ask the user to set them in Picsart Drive.

## Save and verify within the task

For requested remote storage, use `picsart_drive`. It creates folders, uploads media (image, video, audio) from a URL or chat attachment, updates file attributes, and moves items. For URL upload, use the returned result URL and item identity. Keep working versions separate from approved reusable resources. Preserve original files when creating a variant.

When the task includes resumable work, keep editable scenes and dependency records in the workspace project folder and final media on Drive. Do not claim that previewing or editing a scene saves it remotely. Use current returned plain URLs as tool inputs and download URLs only for user downloads. Never infer lifetime from a URL's shape.

Read back the destination after a save when needed to establish its identity and contents. A stale folder listing does not mean the preceding write failed. Inspect the operation result before retrying. Record the returned file/folder ID and save outcome; if uncertain, report uncertainty without repeating a possibly successful write.

For film references, `picsart_save_asset` is the registry writer. Use actual asset-review approval when promoting a reference to `status: "locked"`. Only `locked: true` confirms the lock. A durable draft save remains a draft. Do not infer a film lock from shared-library membership.

Shared-library publication is explicit: select the canonical category and asset folder, save the approved resource through the supported writer, retain role/description metadata where supported, and verify the resulting resource. Publication must be part of the user's request. Keep unrelated organization, moves, or deletion outside a reuse workflow.

## Handoff

Carry selected resource IDs and versions through planning, generation, composition, revision, and delivery. Return remote source references, working scene/project references when saved, final outputs, and confirmed save receipts. Mark provisional filename selections and missing metadata. If persistence fails, preserve available task state and identify the unsaved part.

Current exposed contracts and interface limitations are in the [interface map](interface-map.md). These rules do not assume MCP/CLI/SDK storage parity.
