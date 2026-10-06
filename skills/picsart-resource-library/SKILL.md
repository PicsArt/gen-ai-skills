---
name: picsart-resource-library
description: Publish or version reusable Picsart characters, props, locations, brands, and project resources in remote storage with verified receipts.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, resource-library, publishing, versioning]
---

# Resource library

Publish or version reusable resources in remote storage and prove each save with a read-back.

## When to Use

- The user wants to publish or version a character, prop, location, brand, or project resource.
- A save must be confirmed by receipts, not assumed from generation or film registry state.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [remote resources](../picsart-workflows/references/remote-resources.md) for storage routes, durable references, and publication checks.
- Read [the Library contract](../picsart-workflows/references/drive-library.md) for canonical paths, identity, metadata, and pagination.

## How to Run

Follow the Procedure below.

## Quick Reference

- Resource categories: characters, props, locations, brands, and project resources.

## Procedure

1. Identify the requested publication, version, or project save.
2. Resolve the user's Drive root and category folder before selecting a resource.
3. Use [asset reuse](../picsart-asset-reuse/SKILL.md) for discovery and reference selection.
4. Preserve source folder IDs, media IDs, plain URLs, roles, and available descriptions.
5. For publication, inspect the established writer's schema and destination behavior before submitting.
6. Create or revise only the resource and destination authorized by the task.
7. Retain the original when publishing an intentional variant, unless replacement was requested.
8. Read back the saved folder and files through the established adapter.
9. Return source and destination identities, selected references, and confirmed save receipts.

## Pitfalls

- Treat failed discovery as unavailable, rather than an empty Library.
- Do not infer semantic tags from reduced listing responses.
- Keep film registry locks separate from shared Library membership.
- Generation auto-save does not establish Library publication.
- If the available writer cannot target the canonical Library, report that limitation before claiming publication.
- Record storage metadata actually returned; do not invent a required manifest or character DNA schema.

## Verification

- Claim publication only from the read-back in step 8 and the receipts in step 9.
