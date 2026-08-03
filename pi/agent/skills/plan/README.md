# Plan Skill

A structured workflow planning system for pi that ensures work is reviewed before execution.

## Quick Start

Tell pi you want a plan:
```
I need to [describe work]. Please create a plan first and wait for my approval before proceeding.
```

Pi will:
1. Create a detailed plan
2. Show it to you
3. Wait for your approval
4. Execute only after you approve

## Files

- **SKILL.md** - Main skill documentation and usage guide
- **references/templates.md** - Pre-built planning request templates
- **references/execution.md** - How execution works after approval
- **references/best-practices.md** - Comprehensive best practices guide

## Usage Examples

### Simple Example
```
User: "Plan how to refactor the auth module. Wait for my approval."
Pi: [Shows plan]
User: "Looks good, proceed."
Pi: [Executes the refactoring]
```

### Complex Example with Modifications
```
User: "Plan a database migration to add roles. Show me the plan first."
Pi: [Shows plan]
User: "I like the plan, but in step 3, also add an audit table."
Pi: [Updates plan with modifications]
User: "Perfect, proceed."
Pi: [Executes the updated plan]
```

## Installation

The skill is installed at:
```
~/.pi/agent/skills/plan/
```

It will be auto-discovered by pi and available as:
- `/skill:plan` command
- Automatic suggestion when planning is appropriate

## Integration

Make planning your default workflow by adding to `.pi/settings.json`:

```json
{
  "defaultWorkflow": "planning",
  "requireApprovalForChanges": true
}
```

Or use explicitly:
```
/skill:plan [describe what you want planned]
```

## Key Features

✅ Structured planning with clear phases
✅ User approval before execution  
✅ Risk assessment and alternatives
✅ Step-by-step execution with checkpoints
✅ Rollback capability
✅ Complete audit trail
✅ Customizable templates
✅ Best practices guide

## See Also

- [SKILL.md](SKILL.md) - Full documentation
- [Templates Guide](references/templates.md) - Planning request templates
- [Execution Workflow](references/execution.md) - How approved plans are executed
- [Best Practices](references/best-practices.md) - Tips for better planning
