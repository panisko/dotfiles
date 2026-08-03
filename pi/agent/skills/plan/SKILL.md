---
name: plan
description: Workflow planning system that creates detailed work plans before execution. Pi creates and displays a comprehensive plan, waits for user approval, and only proceeds with work after explicit confirmation.
---

# Planning Skill

This skill implements a structured planning workflow to ensure work is reviewed before execution.

## Overview

The planning skill enables a two-phase workflow:
1. **Planning Phase**: Pi analyzes the task, creates a detailed plan, and presents it to the user
2. **Execution Phase**: After user approval, Pi executes the work according to the plan

## How to Use

### Phase 1: Create a Plan

When you need pi to plan work before doing anything:

```
I need to [describe the work]. Please create a plan first and wait for my approval before proceeding.
```

Pi will:
1. Analyze the task
2. Break it down into logical steps
3. Identify potential risks or considerations
4. Present the plan clearly in a structured format

### Phase 2: Review and Approve

You will see the plan with:
- **Objective**: What will be accomplished
- **Steps**: Numbered, sequential actions
- **Estimated Impact**: Files/systems that will be affected
- **Risks/Considerations**: Potential issues to be aware of
- **Alternatives**: Other approaches if applicable

Review the plan carefully, then respond with:
- ✅ **Approve**: `Proceed with the plan` or `Yes, continue`
- ❌ **Reject/Modify**: `No, please modify the plan to...` or suggest changes

### Phase 3: Execute (After Approval Only)

Once approved, pi executes the work step-by-step:
- Follows the approved plan
- Provides progress updates after each major step
- Reports completion with results
- Offers to modify, undo, or continue if needed

## Plan Format Template

```
## 📋 PLAN: [Task Name]

**Objective**: [What will be accomplished]

### Steps
1. [First action] - [brief description]
2. [Second action] - [brief description]
3. [Third action] - [brief description]
...

### Estimated Impact
- **Files to create/modify**: [list]
- **Systems affected**: [list]
- **Data impact**: [describe]

### Risks & Considerations
- [Risk or consideration 1]
- [Risk or consideration 2]

### Alternatives
- **Option A**: [alternative approach]
- **Option B**: [alternative approach]

---
**Ready to proceed? Please confirm or suggest modifications.**
```

## Integration Examples

### Example 1: Code Refactoring

User: "Refactor the authentication module to use async/await. Show me a plan first."

Pi creates plan → User reviews → User approves → Pi refactors code

### Example 2: Database Schema Changes

User: "Plan a migration to add user roles. I want to see the plan before you make changes."

Pi creates plan → User reviews for SQL correctness → User approves → Pi creates migration

### Example 3: Multi-file Configuration

User: "I need to set up Docker for this project. Create a plan and wait for approval."

Pi creates plan → User reviews Docker setup → User suggests modifications → Pi adjusts plan → User approves → Pi creates Dockerfile and docker-compose.yml

## Best Practices

1. **Be Specific in Requests**: Include context about scope, constraints, and priorities
2. **Review Plans Carefully**: Check for logical errors, missing steps, or unintended side effects
3. **Approve or Modify**: Don't leave plans hanging; provide clear feedback
4. **Save Important Plans**: Copy complex plans for your records
5. **Provide Context on Rejection**: If rejecting, explain what should change

## Forcing Plan Mode

If pi doesn't automatically use planning, you can explicitly invoke this skill:

```
/skill:plan [describe what you want planned]
```

This ensures the planning workflow is followed for that task.

## Environment Variables & Settings

To make planning the default behavior, add to your `.pi/settings.json`:

```json
{
  "defaultWorkflow": "planning",
  "requireApprovalForChanges": true
}
```

## Troubleshooting

**Q: Pi isn't waiting for approval after showing the plan**
- A: Explicitly say "wait for my approval" or "don't proceed until I say so"
- Use `/skill:plan` to force the planning workflow

**Q: The plan is too detailed/not detailed enough**
- A: Tell pi: "Show me a higher-level plan" or "Add more technical details"

**Q: I want to modify the plan**
- A: Describe the changes: "In step 3, also add X" or "Skip step 5 and instead do Y"

## See Also

- [Work Execution Workflow](references/execution.md)
- [Plan Templates](references/templates.md)
