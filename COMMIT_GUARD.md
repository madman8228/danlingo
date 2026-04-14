# Root Commit Guard

The root repository now enforces a pre-commit guard:

- Blocks temporary/debug files in staged changes
- Blocks UTF-8 BOM in staged text files
- Blocks obvious mojibake markers and replacement char `U+FFFD`

## Enable

Run at repository root:

```bash
git config core.hooksPath .githooks
```

## Manual Check

```bash
node scripts/guard-staged-files.js
```

