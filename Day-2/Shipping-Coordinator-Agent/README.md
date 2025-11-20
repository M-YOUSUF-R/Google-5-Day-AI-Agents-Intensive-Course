# Shipping Coordinator Agent

## Description:
If tools are long-running or needed human approval before completing an action?

Example: A shipping agent should ask for approval before placing a large order.
```
User asks → Agent calls tool → Tool PAUSES and asks human → Human approves → Tool completes → Agent responds
```
This is called a Long-Running Operation (LRO) - the tool needs to pause, wait for external input (human approval), then resume.
## Agenda:
- Auto-approves small orders (≤5 containers)
- Pauses and asks for approval on large orders (>5 containers)
- Completes or cancels based on the approval decision
This demonstrates the core long-running operation pattern: **`pause → wait for human input → resume`**.

