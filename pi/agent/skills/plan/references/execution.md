# Execution Workflow

This document describes how pi executes work after plan approval.

## Execution Phases

### 1. Verification
Before executing any plan, pi will:
- Verify the current state matches the plan's assumptions
- Alert you to any deviations
- Ask for clarification if needed

### 2. Progressive Execution
Pi executes the plan step-by-step:
- Completes one major step
- Reports results
- Confirms readiness for next step (if risky or has dependencies)

### 3. Checkpoints
For complex plans, pi creates checkpoints:
- After each major milestone
- Before any destructive operations
- Before operations affecting multiple systems

At checkpoints, you can:
- Continue to next step
- Skip remaining steps
- Request a modified approach
- Pause and resume later

### 4. Completion
After all steps complete, pi:
- Summarizes what was done
- Shows any warnings or errors encountered
- Provides rollback instructions if applicable
- Offers next steps

## Approval Commands

These commands are recognized after a plan is presented:

### Approve Plan
- "proceed with the plan"
- "yes, continue"
- "approved"
- "go ahead"
- "execute the plan"

### Request Modifications
- "no, please modify the plan to..."
- "in step 3, also do..."
- "skip step 2"
- "add a step that..."
- "can you make this less risky?"

### Pause/Cancel
- "hold on, let me think about this"
- "pause"
- "cancel"
- "nevermind"

## During Execution

### Stopping Execution
At any time during execution, you can:
- "stop" or "pause" - Halts current work
- "abort" - Cancels remaining steps
- "undo last step" - Rolls back if possible

### Getting Updates
- "what step are we on?" - Shows progress
- "show me what was changed" - Displays modifications made so far
- "summarize progress" - Full status report

## After Execution

### Verification
- Review all changes made
- Test functionality if applicable
- Confirm everything works as expected

### Rollback
If issues occur, request:
- "undo those changes"
- "rollback to previous state"
- "revert the last N steps"

Pi will provide rollback instructions (manual steps if full rollback isn't possible).

## Error Handling

If pi encounters an error during execution:
- Execution pauses
- Error is explained
- You decide to: continue, retry, skip step, or abort
- Pi waits for your instruction

## Audit Trail

After execution, pi can provide:
- Complete list of files created/modified
- Before/after comparisons
- Commit message suggestions (for git operations)
- Documentation of what was changed and why
