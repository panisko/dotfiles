# Plan/Build Mode Extension for Pi

🎯 **Smart mode switching for structured development.**

Switch between **PLAN mode** (architecture & design), **BUILD mode** (implementation), and **HYBRID mode** (natural balance). Each mode has tailored instructions and tool restrictions.

## Installation

The extension is installed in `~/.pi/agent/extensions/plan-build-mode/`. It auto-loads with pi.

## Quick Start

### Commands

```bash
/mode plan              # 🎯 Switch to PLAN mode
/mode build             # 🔨 Switch to BUILD mode
/mode hybrid            # 🔄 Switch to HYBRID mode (default)
/mode                   # Cycle through modes
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Alt+P` | Switch to PLAN mode |
| `Ctrl+Alt+B` | Switch to BUILD mode |
| `Ctrl+Alt+H` | Switch to HYBRID mode |

### Status Bar

When a mode is active, the status bar shows:

```
🎯 PLAN      🔨 BUILD      🔄 HYBRID
```

## Three Modes Explained

### 🎯 PLAN MODE

**Focus:** Architecture, design, strategy. Think first, code later.

**What Claude does:**
- ✅ Design solutions before implementation
- ✅ Write pseudocode and flowcharts (ASCII/Mermaid)
- ✅ Break problems into steps
- ✅ Outline file structures and APIs
- ✅ Identify edge cases and risks
- ✅ Ask clarifying questions
- ✅ Compare approaches and tradeoffs

**Tools allowed:**
- ✅ `read` — Understand existing code
- ✅ `bash` — Explore/discovery only (e.g., `ls`, `grep`, `find`)
- ❌ `write`, `edit` — Not yet (saving for BUILD mode)

**Example workflow:**

```
You: How should I structure a React auth system?

Claude (in PLAN mode):
## Architecture Plan

1. **Structure:**
   - src/
     - auth/
       - hooks/ (useAuth, useLogin)
       - context/ (AuthContext)
       - types/ (User, AuthState)
     - api/ (auth endpoints)

2. **Flow:**
   User login → validate credentials → create JWT → store in secure cookie

3. **Implementation steps:**
   - [ ] Define types
   - [ ] Create auth context
   - [ ] Build useAuth hook
   - [ ] Add login endpoint
   - [ ] Add token refresh logic

4. **Edge cases:**
   - Token expiry
   - Concurrent requests
   - Page refresh with expired token

Ready to build? Switch to /mode build
```

### 🔨 BUILD MODE

**Focus:** Implementation, execution, iteration. Code fast, build complete.

**What Claude does:**
- ✅ Write code and create files
- ✅ Execute and test changes
- ✅ Fix errors and debug
- ✅ Push to completion
- ✅ Reference plans as context

**Tools allowed:**
- ✅ ALL tools — `write`, `edit`, `bash`, `read`, etc.
- ✅ Fast iteration and immediate testing

**Example workflow:**

```
You: /mode build

Claude (in BUILD mode):
🔨 BUILD MODE: Implement and execute quickly

You: Create the auth context and useAuth hook

Claude:
Created src/auth/context.ts with AuthContext provider.

Key changes:
- AuthProvider wraps app
- useAuth hook exposes user, login, logout
- Login validates credentials against backend
- Token stored in secure httpOnly cookie

Next: Creating useAuth hook tests...

[Runs tests, shows results]
```

### 🔄 HYBRID MODE (Default)

**Focus:** Natural balance. Plan when needed, build when clear.

**What Claude does:**
- ✅ Brief planning for complex decisions
- ✅ Quick building for straightforward work
- ✅ Suggest which mode fits next step
- ✅ Switch between modes naturally

**Tools allowed:**
- ✅ ALL tools — Use wisely based on context

**Example workflow:**

```
You: Build a payment system

Claude (in HYBRID mode):
## Quick plan:

Two paths:
1. Stripe integration (simple) → code it now
2. Custom payment processor (complex) → plan first

Starting with Stripe...

[Creates files, builds API]

For custom processor, should we /mode plan first? (y/n)
```

## Typical Workflow

### Large Feature Development

```
1. Start in HYBRID mode
2. Encounter complex architecture decision
   → /mode plan
   → Design solution with diagrams
3. Design complete
   → /mode build
   → Implement rapidly
4. Build complete
   → /mode plan (if needed for next phase)
   → Or stay in /mode build for bug fixes
```

### Quick Fixes

```
1. Stay in /mode build
2. Read code, identify bug, fix, test
3. Done
```

### Exploring a Large Codebase

```
1. /mode plan
2. Use bash, read to understand structure
3. Ask clarifying questions
4. → /mode build once direction is clear
```

## Mode Features

### System Prompt Injection

Each mode injects specific instructions:

**PLAN mode** emphasizes:
- Pseudocode and architecture
- Step-by-step planning
- Edge case identification
- Design decisions with tradeoffs

**BUILD mode** emphasizes:
- Code first, explanation second
- Clear diffs and changes
- Testing and validation
- Completion focus

**HYBRID mode** balances both:
- Natural switching
- Context-aware tool use
- Suggest next mode

### Tool Restrictions

| Mode | write | edit | bash | read | All Others |
|------|-------|------|------|------|-----------|
| PLAN | ❌ | ❌ | ✅ (read-only) | ✅ | ❌ |
| BUILD | ✅ | ✅ | ✅ | ✅ | ✅ |
| HYBRID | ✅ | ✅ | ✅ | ✅ | ✅ |

### State Persistence

- Mode is **saved in your session**
- Survives reloads and `/resume`
- Each session can have its own mode
- State stored as custom entries in session file

## Practical Examples

### Example 1: Refactor Large Module

```
You: I need to refactor the payment module

/mode plan

Claude: PLAN MODE
[Analyzes current structure]
[Proposes new architecture]
[Lists 8 steps with dependencies]

You: [Reviews plan]

/mode build

Claude: BUILD MODE
[Starts implementing step 1]
[Creates new files]
[Runs tests]
[Implements step 2]
...
```

### Example 2: Debug a Complex Issue

```
You: Why is my auth broken?

Claude (HYBRID mode): 
Let me explore...
[Uses bash to check logs]
[Uses read to examine code]

PLAN: Issue is token validation. Two solutions:
1. Fix validation logic (simple)
2. Redesign token flow (complex)

I'd suggest option 1. Switch to /mode build to fix?

You: Yes, /mode build

Claude: BUILD MODE
[Identifies exact bug]
[Fixes validation code]
[Runs tests to confirm]
```

### Example 3: New Feature from Scratch

```
You: Add email notifications

/mode plan

Claude: PLAN MODE
[Designs email queue system]
[Proposes worker process architecture]
[Lists edge cases: retry logic, rate limiting, bounce handling]

You: Looks good, implement it

/mode build

Claude: BUILD MODE
[Creates email service]
[Builds queue processor]
[Adds tests]
[Validates with manual testing]
```

## Advanced Usage

### Combine with Caveman Mode

Plan/Build Mode works great with Caveman Mode:

```bash
/caveman ultra
/mode plan

# Claude plans in terse caveman style
# "Arch: 3-layer. API → service → DB. Split auth to separate module."
```

### Combine with Other Extensions

- With `senior-code-reviewer`: Use PLAN mode to review architecture
- With `plan` skill: PLAN mode emphasizes structured breakdown
- With `caveman`: Saves tokens in all modes

## Troubleshooting

### "Why can't I write files in PLAN mode?"

PLAN mode intentionally restricts write/edit tools to force planning before implementation. This prevents jumping to code too early.

If you need to create files while planning, use HYBRID or BUILD mode.

### Mode reverted unexpectedly?

Mode state is session-specific. If you `/new` or `/resume` a different session, it will have its own mode setting.

### Want different tool restrictions?

Edit the `agent_start` handler in `~/.pi/agent/extensions/plan-build-mode/index.ts` and customize `setActiveTools()`.

## Keyboard Shortcuts

| Shortcut | Mode | Function |
|----------|------|----------|
| `Ctrl+Alt+P` | → PLAN | Design and architecture focus |
| `Ctrl+Alt+B` | → BUILD | Implementation focus |
| `Ctrl+Alt+H` | → HYBRID | Natural balance (default) |

## Implementation Details

### How It Works

1. **Session start** → Restore mode from previous session
2. **Before each agent turn** → Inject mode-specific system prompt
3. **After user message** → Control available tools based on mode
4. **Status bar** → Show current mode with emoji
5. **Session end** → Save mode state for next session

### Mode State Storage

Stored as custom entries in your `.pi/sessions/*.jsonl` session file:

```json
{
  "type": "custom",
  "customType": "plan-build-mode",
  "timestamp": 1234567890,
  "data": {
    "mode": "plan"
  }
}
```

### System Prompt Structure

Each mode adds ~500 characters to the system prompt:
- PLAN: Instructions for architecture/design
- BUILD: Instructions for implementation
- HYBRID: Instructions for natural balance

No performance impact — prompt is cached.

## FAQ

**Q: Can I use both PLAN and BUILD in the same session?**

A: Absolutely. Switch with `/mode plan`, `/mode build`, or shortcuts. State is saved to session.

**Q: What happens if I call a disallowed tool in PLAN mode?**

A: Claude won't attempt it — the tool restriction is in the active tools list, so it won't be offered to the LLM.

**Q: Should I start every project in PLAN mode?**

A: Not required. For simple changes, HYBRID or BUILD work fine. PLAN mode is best for:
- Complex architecture decisions
- Refactoring large modules
- Exploring unfamiliar codebases
- Designing new systems

**Q: Can I customize the instructions?**

A: Yes, edit the `PLAN_MODE_INSTRUCTIONS`, `BUILD_MODE_INSTRUCTIONS`, and `HYBRID_MODE_INSTRUCTIONS` constants in `index.ts` and run `/reload`.

## Related Extensions

- **Caveman Mode** (`~/.pi/agent/extensions/caveman/`) — Ultra-terse responses, saves tokens
- **Plan Skill** (pi built-in) — Structured workflow planning
- **Senior Code Reviewer** — Code quality improvements

## License

MIT — Same as pi.
