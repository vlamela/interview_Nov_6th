# Senior Python Engineer: Review and Improve a Quota Pilot

## Scenario

This fictional service issues upload URLs and reports stored-file metadata.
A pilot quota check has been added before a wider rollout. Clients can retry
requests, several uploads can happen concurrently, and storage operations can fail.

A support report says that `DE` accepts a new 200-byte upload with a 500-byte
quota even though it has 230 stored bytes and 100 bytes reserved by an upload
in progress. Review the design, reproduce the issue with the supplied demo,
and agree on a small fix before coding.

This is a **40-minute engineering discussion and change**, not a typing-speed
test. No automated test writing is required. Prioritize correctness and a clear
explanation over building a complete production system. Documentation lookup is
allowed; agree on AI-assistant usage with the interviewer before starting.

## Setup

Prerequisites: Python 3.12+ and uv (<https://docs.astral.sh/uv/>).
From this directory, or the root of the extracted exercise repository:

```sh
uv sync --locked
uv run python demo.py
uv run ruff check .
uv run ruff format --check .
```

Use the demo to observe the reported behavior. The implementation is complete
and runnable, but that does not imply it is correct. No test framework is included
in this candidate project. You need no cloud accounts, Docker, HTTP server,
database server, or parent repository files. Complete setup before the interview.

Pydantic models are supplied, not a framework-knowledge test. Construct them with
named arguments, read their attributes, and use `Model.model_validate(dict(row))`
when mapping SQL rows. Validation errors inherit from `ValueError`. Ask for a
brief walkthrough if this API is unfamiliar; no custom validators are required.

## Part 1: Review Before Coding

Read `service.py`, trace the quota calculation, and ask clarifying questions.
Explain your two highest-priority correctness or operational risks, the
guarantee you would want in production, and the smallest useful change today.
Spoken reasoning or short notes are enough; no formal design document is required.

Discuss the difference between issuing a URL, reserving capacity, and completing
an upload. Consider concurrent requests, retries, expiry, remote failures, and
whether the declared file size can be trusted. You do not need to implement all
of these concerns. Clarify business rules with the interviewer rather than
assuming that status names or the existing code define the intended policy.

## Part 2: Propose and Implement a Small Fix

Investigate the reported behavior and explain its cause. Propose the smallest
useful correction and agree on its scope and business rules with the interviewer
before coding.

Preserve existing public interfaces, schema, seed data, and unrelated behavior.
Use the supplied timestamp and database connection. This change must not create,
update, or delete database records.

Demonstrate your change using the supplied demo, explain its limitations, and
describe what you would address next for production. A complete reservation
lifecycle or concurrency-safe quota system is not required in this session.

## Part 3: Walkthrough and Manual Checks

Choose a few representative inputs yourself. Explain the outcome you expect
before running each case, then compare it with the observed behavior.

Each invocation creates a fresh seeded database. The demo also accepts
`--market`, `--filename`, `--size-bytes`, `--quota-bytes`, and `--now`.
Run `uv run python demo.py --help` to see the available options. It prints the
decision and storage call count, not the signed URL. A quota rejection is a
normal result, so both accepted and rejected decisions exit successfully.

You do not need to write or run automated tests. Explain which additional cases
you would verify before rollout and what these manual checks cannot prove.
Threads, distributed locks, PostgreSQL, and a full upload lifecycle are not
implementation requirements.

## Project Map

- `upload_exercise/models.py`: supplied immutable Pydantic contracts and input safety.
- `upload_exercise/service.py`: working URL operations and the quota pilot under review.
- `upload_exercise/storage.py`: storage interface and fake; no network or real signing.
- `upload_exercise/database.py`: schema, fixed seed data, and connection factory.
- `upload_exercise/repository.py`: completed stored-file queries, available for reference.
- `demo.py`: command-line reproduction and manual-check entry point.

The database contains metadata only. Each `create_database()` call opens a separate
in-memory database; closing that connection discards it. Pass the supplied connection
through the operation. The service generates fake URLs; it does not upload or delete files.

## Out of Scope

New HTTP endpoints, authentication, deployment, migrations, real storage, async
execution, automated test writing, and a complete reservation lifecycle. Review
and discuss production concerns, but implement only the agreed small correction.