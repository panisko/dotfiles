import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

type WorkMode = "plan" | "build" | "hybrid";

interface ModuleState {
  mode: WorkMode;
}

const PLAN_MODE_INSTRUCTIONS = `## PLAN MODE 🎯

You are in **PLAN MODE**. Focus on planning, architecture, and strategy. Do NOT execute code yet.

**Your role:**
- Design solutions before implementation
- Write pseudocode and architecture diagrams (ASCII, Mermaid)
- Break problems into steps
- Outline file structures and APIs
- Identify edge cases and risks
- Ask clarifying questions
- Propose multiple approaches with tradeoffs

**Tool restrictions:**
- Use: bash (for exploration/discovery only), read (to understand existing code)
- Avoid: write, edit, file creation (these are for BUILD mode)

**Output style:**
- Architecture first, implementation second
- Use pseudocode, flowcharts, step-by-step plans
- Propose file structure and APIs before coding
- Number your steps clearly

**Example response:**
\`\`\`
## Architecture Plan

1. **Structure:**
   - src/
     - core/engine.ts (main logic)
     - api/handlers.ts (HTTP endpoints)
     - types/index.ts (shared types)

2. **Flow:**
   - User request → validate → fetch data → transform → respond

3. **Implementation steps:**
   - [ ] Define types
   - [ ] Create core engine
   - [ ] Add API handlers
   - [ ] Write tests

4. **Edge cases:**
   - Empty input handling
   - Concurrent requests
   - Network timeouts
\`\`\`

When ready to code, switch to BUILD mode: \`/mode build\` or \`/mode hybrid\``;

const BUILD_MODE_INSTRUCTIONS = `## BUILD MODE 🔨

You are in **BUILD MODE**. Focus on implementation and execution. Build fast, iterate quickly.

**Your role:**
- Write code, create files, refactor
- Execute and test your work
- Fix errors and validate
- Push to completion
- Reference plans as you go

**Tool restrictions:**
- Use: write, edit, bash, read (all tools enabled)
- Focus on execution
- Create and modify files freely

**Output style:**
- Code first, explanation second
- Show diffs and changes clearly
- Run tests and validate
- Report completion status

**Example response:**
\`\`\`
Created src/engine.ts with core logic.

Key changes:
- Export Engine class with run() method
- Handle concurrent requests via Promise.all()
- Timeout protection: 30s per request

Next: Create API handlers.
\`\`\`

When planning next steps, switch to PLAN mode: \`/mode plan\` or \`/mode hybrid\``;

const HYBRID_MODE_INSTRUCTIONS = `## HYBRID MODE 🔄

You are in **HYBRID MODE**. Balance planning and building as needed.

**Your role:**
- Plan when needed (complex decisions, architecture)
- Build when clear (straightforward implementation)
- Switch between modes naturally
- Suggest which mode fits next step

**Tool access:**
- All tools available
- Use wisely based on context

**Output style:**
- Start with brief plan if needed
- Then execute
- Explain reasoning as you go

**Example response:**
\`\`\`
PLAN: Need to handle two cases:
1. Simple validation (straight code)
2. Complex transformation (needs planning first)

BUILD: Starting with validation...

[Code creation + execution]

PLAN: Next, for transformation, we should:
- Separate concerns into layers
- Add caching layer

Ready to switch to /mode plan for architecture, or continue building?
\`\`\`

Use \`/mode plan\` or \`/mode build\` to lock into a single mode.`;

export default function (pi: ExtensionAPI) {
  let modeState: ModuleState = { mode: "plan" };

  // Restore mode state from session on startup
  pi.on("session_start", async (_event, ctx) => {
    for (const entry of ctx.sessionManager.getEntries()) {
      if (entry.type === "custom" && (entry as any).customType === "plan-build-mode") {
        const data = (entry as any).data as Partial<ModuleState>;
        if (data.mode) {
          modeState.mode = data.mode;
        }
      }
    }
    ctx.ui.setStatus("mode", getModeEmoji(modeState.mode) + " " + modeState.mode.toUpperCase());
  });

  // Inject mode-specific instructions into system prompt
  pi.on("before_agent_start", async (event, ctx) => {
    let modeInstructions = "";

    if (modeState.mode === "plan") {
      modeInstructions = PLAN_MODE_INSTRUCTIONS;
    } else if (modeState.mode === "build") {
      modeInstructions = BUILD_MODE_INSTRUCTIONS;
    } else {
      modeInstructions = HYBRID_MODE_INSTRUCTIONS;
    }

    return {
      systemPrompt: event.systemPrompt + "\n\n" + modeInstructions,
    };
  });

  // Control available tools based on mode
  pi.on("agent_start", async (_event, ctx) => {
    if (modeState.mode === "plan") {
      // Plan mode: only allow read, bash (for exploration), and think tools
      pi.setActiveTools(["read", "bash"]);
    } else {
      // Build/Hybrid mode: allow all tools
      pi.setActiveTools(pi.getAllTools().map(t => t.name)); // restore all tools
    }
  });

  // Register /mode command
  pi.registerCommand("mode", {
    description: 'Switch between plan, build, and hybrid modes',
    handler: async (args, ctx) => {
      const modes: WorkMode[] = ["plan", "build", "hybrid"];
      let newMode: WorkMode;

      if (args.trim()) {
        const requested = args.trim().toLowerCase();
        if (modes.includes(requested as WorkMode)) {
          newMode = requested as WorkMode;
        } else {
          ctx.ui.notify(`Unknown mode: ${requested}\nAvailable: ${modes.join(", ")}`, "error");
          return;
        }
      } else {
        // Cycle through modes
        const currentIndex = modes.indexOf(modeState.mode);
        const nextIndex = (currentIndex + 1) % modes.length;
        newMode = modes[nextIndex];
      }

      modeState.mode = newMode;
      pi.appendEntry("plan-build-mode", { mode: newMode });

      const emoji = getModeEmoji(newMode);
      const description = getModeDescription(newMode);

      ctx.ui.setStatus("mode", `${emoji} ${newMode.toUpperCase()}`);
      ctx.ui.notify(`${emoji} ${newMode.toUpperCase()}: ${description}`, "info");
    },
  });

  // Register shortcuts
  pi.registerShortcut("ctrl+alt+p", {
    description: "Switch to PLAN mode",
    handler: async (ctx) => {
      modeState.mode = "plan";
      pi.appendEntry("plan-build-mode", { mode: "plan" });
      ctx.ui.setStatus("mode", "🎯 PLAN");
      ctx.ui.notify("🎯 PLAN MODE: Design solutions before implementation", "info");
    },
  });

  pi.registerShortcut("ctrl+alt+b", {
    description: "Switch to BUILD mode",
    handler: async (ctx) => {
      modeState.mode = "build";
      pi.appendEntry("plan-build-mode", { mode: "build" });
      ctx.ui.setStatus("mode", "🔨 BUILD");
      ctx.ui.notify("🔨 BUILD MODE: Implement and execute quickly", "info");
    },
  });

  pi.registerShortcut("ctrl+alt+h", {
    description: "Switch to HYBRID mode",
    handler: async (ctx) => {
      modeState.mode = "hybrid";
      pi.appendEntry("plan-build-mode", { mode: "hybrid" });
      ctx.ui.setStatus("mode", "🔄 HYBRID");
      ctx.ui.notify("🔄 HYBRID MODE: Balance planning and building", "info");
    },
  });
}

function getModeEmoji(mode: WorkMode): string {
  return {
    plan: "🎯",
    build: "🔨",
    hybrid: "🔄",
  }[mode];
}

function getModeDescription(mode: WorkMode): string {
  return {
    plan: "Design solutions before implementation. Use read/bash for exploration only.",
    build: "Implement and execute. All tools enabled. Code first, iterate fast.",
    hybrid: "Balance planning and building. Switch modes naturally as needed.",
  }[mode];
}
