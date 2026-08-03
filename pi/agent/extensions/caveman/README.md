# Caveman Extension for Pi

🪨 **Why use many token when few do trick?**

Caveman mode for pi — reduces response tokens by ~75% while keeping technical accuracy. Speak terse, stay smart.

## Installation

The extension is already installed in `~/.pi/agent/extensions/caveman/`. It auto-loads with pi.

## Quick Start

### Activate Caveman

Use the `/caveman` command:

```
/caveman full      # Default caveman (most balanced)
/caveman lite      # Minimal compression (keep articles + full sentences)
/caveman ultra     # Maximum compression (abbreviate everything)
/caveman wenyan    # Classical Chinese style (文言文)
/caveman off       # Normal mode (disable caveman)
```

Or use the keyboard shortcut **`Ctrl+G`** to cycle through levels.

### Auto-Activation

Caveman auto-activates when you mention:
- "caveman mode"
- "talk like caveman"
- "use caveman"
- "less tokens"
- "compress response"
- "be brief"
- "terse"

Example:
```
please talk like caveman
```
→ Automatically enables caveman mode.

## Intensity Levels

### `lite` - Professional Terseness
Keep articles + full sentences. Drop only filler/hedging.

| Before | After |
|--------|-------|
| "Sure, I'd be happy to help. The issue is likely caused by..." | "Bug: token validation logic incorrect. Fix by checking '<' not '<='." |

### `full` - Classic Caveman (Default)
Drop articles, fragments OK, short synonyms. Maximum readability/compression balance.

| Before | After |
|--------|-------|
| "The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle. I'd recommend using useMemo..." | "New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`." |

### `ultra` - Extreme Compression
Abbreviate prose (DB/auth/config/req/res/fn/impl), use arrows for causality, omit conjunctions.

| Before | After |
|--------|-------|
| "Database connection pooling reuses open connections instead of creating new ones per request..." | "Pool = reuse DB conn. Skip handshake → fast under load." |

### `wenyan-lite` - Semi-Classical Chinese
文言文 style with modern technical terms. Drop filler, keep grammar structure.

```
組件頻重繪，以每繪新生對象參照故。以 useMemo 包之。
```

### `wenyan-full` - Full Classical Chinese
Maximum 文言文 compression (80-90% character reduction).

```
新參照→重繪。useMemo。
```

### `wenyan-ultra` - Ultra-Classical Compression
Extreme abbreviation with classical feel.

```
新參照→重。
```

## Rules per Level

### lite
- ✅ Keep: articles (a/an/the), full sentences, pleasantries
- ✅ Drop: filler (just, really, basically, actually, simply), hedging

### full
- ✅ Keep: technical terms, code blocks, error messages
- ✅ Drop: articles, filler, pleasantries, hedging
- ✅ Use: fragments, short synonyms, pattern: `[thing] [action] [reason]. [next step].`

### ultra
- ✅ Keep: code symbols, function names, API names, error strings
- ✅ Drop: prose conjunctions, subjects when obvious
- ✅ Use: abbreviations (DB/auth/config/req/res), arrows (X → Y)

### wenyan-\*
- ✅ Classical patterns: verbs precede objects, subjects often omitted
- ✅ Classical particles: 之/乃/為/其
- ✅ Modern tech terms: useMemo, DB, API, etc.

## Auto-Clarity Exceptions

Caveman automatically **pauses** for safety/clarity when:

- **Security warnings** — Full detail required
- **Irreversible action confirmations** — Risk of misread unacceptable
- **Multi-step sequences** — Fragment order/omitted conjunctions risk confusion
- **Technical ambiguity** — When compression itself creates misread risk
- **User clarification requests** — Resume after clarification done

Example (destructive operation):

```
⚠️ WARNING: This will permanently delete all rows in the users table and cannot be undone.

DROP TABLE users;

[Full detail here. No caveman abbreviation.]

→ Caveman resumes. Verify backup exist first.
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+G` | Cycle through caveman levels (off → lite → full → ultra → wenyan-lite → ...) |

## Commands

```
/caveman                  # Cycle to next level
/caveman lite             # Switch to lite mode
/caveman full             # Switch to full mode (default)
/caveman ultra            # Switch to ultra mode
/caveman wenyan-lite      # Switch to semi-classical Chinese
/caveman wenyan-full      # Switch to full classical Chinese
/caveman wenyan-ultra     # Switch to ultra classical Chinese
/caveman off              # Disable caveman mode
/caveman stop             # Alias for 'off'
/caveman normal           # Alias for 'off'
```

## Status Bar

When caveman is active, the status bar shows:

```
🪨 Caveman full
```

When disabled:

```
(empty)
```

## Persistence

- Caveman state is **saved in your session** and survives reloads
- Caveman applies to **all responses** until you disable it
- No drift back to normal mode after many turns
- Only turns off via explicit `/caveman off` or "stop caveman" in your message

## How It Works

### System Prompt Injection

When caveman is active, the extension injects detailed instructions into the system prompt:

```
**Caveman Mode (Full):** Speak like smart caveman. All technical substance stay. Only fluff die.

Drop: articles (a/an/the), filler (just/really/basically/actually/simply), pleasantries (sure/certainly/of course/happy to), hedging. Fragments OK. Use short synonyms (big not extensive, fix not "implement a solution for"). Technical terms exact. Code blocks unchanged. Errors quoted exact.

Pattern: [thing] [action] [reason]. [next step].
```

### State Management

Caveman state is stored as custom entries in your session file (`.pi/sessions/`), so it persists across reloads and `/resume`.

## Examples

### Example 1: Quick Bug Fix

**Without caveman:**
> "The issue you're experiencing is caused by the token validation logic not checking for token expiration correctly. I'd recommend modifying the comparison operator from `<` to `<=` in the middleware to ensure all expired tokens are caught."

**With caveman (full):**
> "Bug: token validation use `<` not `<=`. Fix:"

### Example 2: Architecture Discussion

**Without caveman:**
> "The approach you've outlined is good, but you might want to consider using a connection pool to reuse database connections instead of creating new ones for each request. This avoids the overhead of establishing a new connection every time, which can significantly improve performance under high load."

**With caveman (full):**
> "Pool reuse open DB connections. Skip handshake overhead. ~3× faster under load."

### Example 3: Security Warning (Auto-Clarity)

**Always full detail** (caveman pauses):
> "⚠️ **WARNING:** This command will DROP all data in the `users` table permanently. Cannot be undone. Ensure backups exist first."

**Then resumes caveman:**
> "Verify backup exist. Then run."

## Troubleshooting

### Caveman turned off unexpectedly?

Check if you said "stop caveman" or "normal mode" — these auto-deactivate it.

### State not persisting?

Caveman state is stored in your session file. Make sure you're using a persistent session (`/resume`, not ephemeral).

### Want to customize instructions?

Edit the `CAVEMAN_INSTRUCTIONS` object in `~/.pi/agent/extensions/caveman/index.ts` and run `/reload`.

## Related Projects

- **[caveman](https://github.com/JuliusBrussee/caveman)** - The original caveman skill (multi-agent support)
- **[caveman-code](https://github.com/JuliusBrussee/caveman-code)** - Full terminal coding agent with integrated caveman mode

## License

MIT — Same as caveman project.
