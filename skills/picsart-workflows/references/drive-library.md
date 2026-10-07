# Shared Drive Library

Picsart Agents and Playground reuse the same user-owned library.
Check this library before generating a replacement character, prop, or location.
Keep supplied references and requested design changes as the task's requirements.

## Canonical paths

| Asset type | Drive path |
| --- | --- |
| Character or cast member | `/Assets/Library/Characters/<asset-name>` |
| Prop or product object | `/Assets/Library/Props/<asset-name>` |
| Location or set | `/Assets/Library/Locations/<asset-name>` |
| Brand | `/Assets/Library/Brands/<asset-name>` |

These paths start at the user's Drive root.
`My files` is a display label, not a path segment.
Keep the canonical names and resolve current folder IDs.
Do not hard-code another account's folder IDs.
A film project's `Library` and the global `Film Assets` folder are separate stores.
`picsart_list_assets` does not list this shared library.

## Read and select

1. Start with the supplied asset ID or library mention, when available.
2. Otherwise, descend through Assets, Library, and the required category.
3. Match structural folder names after trimming, ignoring case.
4. Prefer canonical casing when structural names have multiple matches.
5. Resolve duplicate asset names by folder ID and relevant context.
6. Read the asset folder and its media files.
7. Keep the folder ID, name, category, description, roles, and plain source URLs.
8. Select the reference that supplies the required view or scene detail.
9. Check the model's input limits before attaching references.

The direct asset folder ID is its identity.
Its category parent supplies the asset type.
There is no required manifest or DNA JSON for shared-library discovery.
Descriptions are native folder fields and may need an individual entry read.

Tags supply `role:<name>` and `primary`.
When any role or primary tag exists, those tags control both values.
Otherwise, use the filename convention `<slug>[_primary][_<role>].<extension>`.
The primary token immediately follows the slug.
Missing tags in a reduced response do not prove that tags are absent.

The default image priority is a tagged sheet, tagged collage, primary view, then another available view.
Keep ordinary views separate from sheet, collage, source-sheet, and voice carriers.
Never pass an archived source sheet or voice file as an ordinary visual view.
Reuse voice metadata or audio only when the model supports it.

## Interfaces and limits

MCP: use `picsart_drive({ action: "list" })` and descend by `folderUid`.
Follow `hasNext` for every listing.
The normalized response omits semantic tags and native folder descriptions.
Use verified raw metadata when roles or carrier identity matter.
Otherwise, report the filename-based selection as provisional.

SDK: `ai.drive.listDetailed({ folder: { uid, name } })` reads a known asset folder.
This reduced reader has a 100-item limit and omits semantic metadata.
Do not use it as a complete library scan.
`folders`, `allFolders`, and `findFolder` can provision the configured root.
CLI folder listing inherits this behavior and cannot resolve the canonical path.

Neither reader returns complete semantic metadata; report roles inferred from filenames as provisional.
Continue pagination until complete.

Do not treat a failed read as an empty library.
Do not create, rename, or relocate folders during discovery.
Reuse preserves the source folder and asset identity across tools.
Film registry saves and generation auto-saves do not automatically publish into this shared library.
