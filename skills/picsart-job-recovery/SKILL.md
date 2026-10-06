---
name: picsart-job-recovery
description: Recover a Picsart generation result after a timeout or interruption without creating a duplicate job.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, job-recovery, job-status, receipts]
---

# Job recovery

Resume a timed-out or interrupted Picsart job from its receipt instead of paying for a duplicate.

## When to Use

- A Picsart generation timed out or the session was interrupted before the result arrived.
- The original job must be checked before any new paid attempt.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md). Locate the original receipt. Keep its model, prompt, job ID, workflow, and save settings.

## How to Run

Use the receipt's interface:

- Model MCP: pass the returned `job` object to `picsart_job_status`. Supply the original `model`. Retain the original prompt and save settings.
- Media MCP: pass the receipt's `job` to the tool named in `tools.jobStatus`. Do not substitute the generation status tool.
- SDK: call `ai.result(model, generationId)` or `ai.subscribe(model, generationId)`.
- CLI: inspect `gen-ai history last --json` or the saved batch report. `gen-ai batch status FILE --json` reads that report. It does not poll the backend.

## Quick Reference

| Receipt interface | Status check |
|---|---|
| Model MCP | `picsart_job_status` |
| Media MCP | `tools.jobStatus` |
| SDK | `ai.result` or `ai.subscribe` |
| CLI | `gen-ai history last --json` or the batch report |

## Procedure

1. Poll within a bounded waiting period. Retain the handle if the job is still active. A host timeout does not prove job failure.
2. On a terminal failure, record the error. Correct the cause before a new authorized attempt. Stop when the spending limit or attempt limit is reached.

## Pitfalls

- Do not use `gen-ai batch resume`, `redo`, or `replay` to check status. These commands can submit paid jobs.
- If the handle is missing, search only the task's saved receipts and authorized account results. Report the uncertainty. Do not submit a replacement solely because the result is absent. Do not claim cancellation without a verified cancellation operation and a confirmed result.

## Verification

- Report the job state that the status check returned, and keep the handle for any job still active.
