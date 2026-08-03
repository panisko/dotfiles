# Planning Best Practices

## For Creating Better Plans

### Be Clear About Scope
- Define what's included and what's NOT included
- Specify any constraints or limitations
- Mention existing dependencies or integrations

### Include Risk Assessment
- Identify potential issues upfront
- Note any breaking changes
- Highlight backwards compatibility concerns
- Mention performance implications

### Provide Context
- Explain the "why" behind the request
- Share business objectives or user needs
- Mention any recent related changes
- Note any time constraints

### Ask for Specifics
Request that the plan include:
- "Show me which files will be affected"
- "Include validation/testing steps"
- "List any dependencies or prerequisites"
- "Provide rollback instructions"
- "Suggest any alternatives"

## For Reviewing Plans

### Use This Checklist

- [ ] **Logical Flow**: Are steps in the right order?
- [ ] **Completeness**: Are any obvious steps missing?
- [ ] **Risk**: Are there unaddressed risks?
- [ ] **Clarity**: Do I understand what will happen?
- [ ] **Scope**: Does it match what I asked for?
- [ ] **Alternatives**: Have alternatives been considered?
- [ ] **Dependencies**: Are prerequisites handled?
- [ ] **Testing**: Is testing included?
- [ ] **Rollback**: Can this be undone if needed?
- [ ] **Impact**: Are all affected systems/files listed?

### Common Issues to Look For

1. **Wrong Order**: Steps that should be sequential are listed in wrong order
2. **Missing Steps**: Common prerequisite steps are skipped
3. **Scope Creep**: Plan includes things you didn't ask for
4. **Assumptions**: Plan assumes facts you need to verify
5. **Unclear Details**: Vague descriptions of what will happen
6. **No Testing**: Testing steps are missing
7. **No Rollback**: No way to undo if things go wrong
8. **Dependencies**: Required setup or other work isn't mentioned

### When to Request Changes

Definitely request changes if:
- You don't understand a step
- A step seems risky without explanation
- Critical steps appear to be missing
- The plan doesn't match your requirements
- You see a safer or simpler approach

Don't approve until you're confident about the plan.

## For Executing Plans

### Before Approving Execution

1. **Read the entire plan** - Don't skim
2. **Ask questions** - If anything is unclear
3. **Check prerequisites** - Verify setup is complete
4. **Backup if needed** - Create backups before destructive operations
5. **Notify stakeholders** - If changes affect other people

### During Execution

1. **Monitor progress** - Watch each step complete
2. **Review changes** - Check files/systems as they're modified
3. **Test incrementally** - Verify functionality after major steps
4. **Interrupt if needed** - Don't hesitate to stop if something looks wrong

### After Execution

1. **Verify completeness** - Check all expected changes were made
2. **Test thoroughly** - Run full test suite or manual tests
3. **Document changes** - Note what was changed and why
4. **Backup results** - Save working state before further changes

## Communication Tips

### Clear Request
```
❌ Bad: "Set up the database"
✅ Good: "Set up PostgreSQL 14 for development, create the schema from 
         schema.sql, and load sample data from fixtures/. Wait for my 
         approval before making any changes."
```

### Specific Feedback
```
❌ Bad: "This doesn't look right"
✅ Good: "In step 3, I'm concerned about the order. Let's check the 
         dependency on step 2 first. Can we reorder these?"
```

### Approval Decision
```
❌ Bad: "OK"
✅ Good: "Looks good! The plan addresses all my concerns. Go ahead and 
         execute it."
```

## When Planning Is Most Valuable

Use the planning workflow for:
- ✅ Complex multi-step changes
- ✅ Changes affecting multiple files
- ✅ Infrastructure/configuration changes
- ✅ Potentially breaking changes
- ✅ High-risk operations
- ✅ First-time integrations
- ✅ Significant refactoring
- ✅ Database schema changes

Less critical for:
- Simple single-file edits
- Quick fixes you fully understand
- Low-risk formatting changes
- Small documentation updates

(But you can still use planning if you want!)

## Handling Plan Disagreements

If pi's plan doesn't match your vision:

1. **Be specific about what's wrong**
   - "Step 4 is too risky because..."
   - "We need to also handle X scenario"
   - "This approach won't work because..."

2. **Provide alternative guidance**
   - "Instead, let's..."
   - "Can we combine steps 2 and 3?"
   - "I think we should use Y tool instead of X"

3. **Let pi revise**
   - Allow pi to reconsider
   - Ask pi to explain the revised reasoning
   - Review the updated plan

4. **Escalate if stuck**
   - Break the plan into smaller pieces
   - Ask for a completely different approach
   - Request pi's reasoning for specific choices

## Reusable Plans

For recurring tasks:

1. **Save successful plans** - Copy the plan format for future reference
2. **Template common workflows** - Build templates for usual operations
3. **Version your plan templates** - Update as processes improve
4. **Share with team** - Let others benefit from tested plans

Example: Save database migration plans, deployment checklists, release procedures, etc.
