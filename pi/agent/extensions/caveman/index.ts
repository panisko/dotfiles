import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

type CavemanLevel = "off" | "lite" | "full" | "ultra" | "wenyan-lite" | "wenyan-full" | "wenyan-ultra";

interface CavemanState {
  level: CavemanLevel;
}

const DEFAULT_LEVEL: CavemanLevel = "full";

const CAVEMAN_INSTRUCTIONS: Record<CavemanLevel, string> = {
  off: "",

  lite: `**Caveman Mode (Lite):** Speak terse. Drop filler and hedging words (just/really/basically/actually/simply/sure/certainly/of course). Keep articles and full sentences. Be professional but tight.

Pattern: [thing] [action] [reason]. [next step].

Examples:
- ❌ "Sure! I'd be happy to help. This is likely caused by..."
- ✅ "Bug in auth middleware. Token expiry check use '<' not '<='. Fix:"`,

  full: `**Caveman Mode (Full):** Speak like smart caveman. All technical substance stay. Only fluff die.

Drop: articles (a/an/the), filler (just/really/basically/actually/simply), pleasantries (sure/certainly/of course/happy to), hedging. Fragments OK. Use short synonyms (big not extensive, fix not "implement a solution for"). Technical terms exact. Code blocks unchanged. Errors quoted exact.

Pattern: [thing] [action] [reason]. [next step].

Examples:
- ❌ "The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle..."
- ✅ "New object ref each render. Inline object prop = new ref = re-render. Wrap in 'useMemo'."`,

  ultra: `**Caveman Mode (Ultra):** Maximum terseness. Abbreviate prose words (DB/auth/config/req/res/fn/impl), strip conjunctions, use arrows for causality (X → Y), use one word when one word enough. Code symbols, function names, API names, error strings: never abbreviate.

Pattern: [thing] [action]. [next step].

Examples:
- ❌ "The component re-renders because of a new reference"
- ✅ "New obj ref → re-render. useMemo."`,

  "wenyan-lite": `**Caveman Mode (文言文 Lite):** Semi-classical Chinese style. Drop filler/hedging but keep grammar structure, classical register. Mix 文言文 patterns with technical terms as needed.

Examples:
- ❌ "這個組件會重新渲染，因為你創建了一個新的對象引用"
- ✅ "對象參照新生，故重繪。useMemo 包之。"`,

  "wenyan-full": `**Caveman Mode (文言文 Full):** Maximum classical terseness. Fully 文言文. 80-90% character reduction. Classical sentence patterns: verbs precede objects, subjects often omitted, use classical particles (之/乃/為/其).

Examples:
- ❌ "數據庫連接池重用開放的連接，避免每次請求都創建新連接"
- ✅ "池reuse conn。skip handshake → fast。"`,

  "wenyan-ultra": `**Caveman Mode (文言文 Ultra):** Extreme abbreviation while keeping classical Chinese feel. Maximum compression, ultra terse. Omit everything possible.

Examples:
- ❌ "對象每次渲染時都會創建新的引用"
- ✅ "新參照→重繪。"`,
};

const CAVEMAN_AUTO_CLARITY = `

## Auto-Clarity (When to Temporarily Stop Caveman)

Caveman pauses for:
- Security warnings
- Irreversible action confirmations
- Multi-step sequences where fragment order or omitted conjunctions risk misread
- When compression itself creates technical ambiguity
- When user asks to clarify or repeats question

Resume caveman after clear part done.`;

export default function (pi: ExtensionAPI) {
  let cavemanState: CavemanState = { level: "ultra" };

  // Restore caveman state from session on startup
  pi.on("session_start", async (_event, ctx) => {
    // Try to find a caveman state entry in the session
    for (const entry of ctx.sessionManager.getEntries()) {
      if (entry.type === "custom" && (entry as any).customType === "caveman-state") {
        const data = (entry as any).data as Partial<CavemanState>;
        if (data.level) {
          cavemanState.level = data.level;
        }
      }
    }
    if (cavemanState.level !== "off") {
      ctx.ui.setStatus("caveman", `🪨 Caveman ${cavemanState.level}`);
    } else {
      ctx.ui.setStatus("caveman", "");
    }
  });

  // Inject caveman instructions into system prompt
  pi.on("before_agent_start", async (event, ctx) => {
    if (cavemanState.level === "off") {
      return;
    }

    const instructions = CAVEMAN_INSTRUCTIONS[cavemanState.level];
    return {
      systemPrompt:
        event.systemPrompt +
        "\n\n" +
        instructions +
        (cavemanState.level.startsWith("wenyan") ? "" : CAVEMAN_AUTO_CLARITY),
    };
  });

  // Register caveman command
  pi.registerCommand("caveman", {
    description: "Toggle caveman mode (terse, token-efficient responses)",
    handler: async (args, ctx) => {
      const levels: CavemanLevel[] = ["off", "lite", "full", "ultra", "wenyan-lite", "wenyan-full", "wenyan-ultra"];

      let newLevel: CavemanLevel;

      if (args.trim()) {
        const requested = args.trim().toLowerCase();
        if (requested === "stop" || requested === "off" || requested === "normal") {
          newLevel = "off";
        } else if (levels.includes(requested as CavemanLevel)) {
          newLevel = requested as CavemanLevel;
        } else {
          const levelsList = levels.join(", ");
          ctx.ui.notify(`Unknown level: ${requested}\nAvailable: ${levelsList}`, "error");
          return;
        }
      } else {
        // Cycle through levels
        const currentIndex = levels.indexOf(cavemanState.level);
        const nextIndex = (currentIndex + 1) % levels.length;
        newLevel = levels[nextIndex];
      }

      cavemanState.level = newLevel;

      // Persist to session
      pi.appendEntry("caveman-state", { level: newLevel });

      if (newLevel === "off") {
        ctx.ui.setStatus("caveman", "");
        ctx.ui.notify("🗣️ Normal mode enabled", "info");
      } else {
        ctx.ui.setStatus("caveman", `🪨 Caveman ${newLevel}`);
        ctx.ui.notify(`🪨 Caveman mode: ${newLevel}`, "info");
      }
    },
  });

  // Register shortcut for quick toggle
  pi.registerShortcut("ctrl+g", {
    description: "Toggle caveman mode (cycle through levels)",
    handler: async (ctx) => {
      const levels: CavemanLevel[] = ["off", "lite", "full", "ultra", "wenyan-lite", "wenyan-full", "wenyan-ultra"];
      const currentIndex = levels.indexOf(cavemanState.level);
      const nextIndex = (currentIndex + 1) % levels.length;
      const newLevel = levels[nextIndex];

      cavemanState.level = newLevel;
      pi.appendEntry("caveman-state", { level: newLevel });

      if (newLevel === "off") {
        ctx.ui.setStatus("caveman", "");
        ctx.ui.notify("🗣️ Normal mode", "info");
      } else {
        ctx.ui.setStatus("caveman", `🪨 Caveman ${newLevel}`);
        ctx.ui.notify(`🪨 Caveman: ${newLevel}`, "info");
      }
    },
  });

  // Auto-detect caveman triggers in user input
  pi.on("input", async (event, ctx) => {
    const text = event.text.toLowerCase();

    // Check for caveman activation triggers
    const triggers = [
      "caveman mode",
      "talk like caveman",
      "use caveman",
      "less tokens",
      "compress response",
      "be brief",
      "terse",
    ];

    const isCavemanTrigger = triggers.some((t) => text.includes(t));

    if (isCavemanTrigger && cavemanState.level === "off") {
      cavemanState.level = DEFAULT_LEVEL;
      pi.appendEntry("caveman-state", { level: DEFAULT_LEVEL });
      ctx.ui.setStatus("caveman", `🪨 Caveman ${DEFAULT_LEVEL}`);
      ctx.ui.notify(`🪨 Caveman mode activated (${DEFAULT_LEVEL})`, "info");
    }

    // Check for caveman deactivation
    if ((text.includes("stop caveman") || text.includes("normal mode")) && cavemanState.level !== "off") {
      cavemanState.level = "off";
      pi.appendEntry("caveman-state", { level: "off" });
      ctx.ui.setStatus("caveman", "");
      ctx.ui.notify("🗣️ Normal mode enabled", "info");
    }
  });
}
