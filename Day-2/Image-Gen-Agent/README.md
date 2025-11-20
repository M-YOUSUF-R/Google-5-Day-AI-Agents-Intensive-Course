# Image Generator Agent

## Human-in-the-Loop :
If tools are long-running or needed human approval before completing an action.
this example describe the process to add human approval with agentic workflow.

Example: A image-gen agent should ask for approval before generating a large number of image.
```
User asks → Agent calls tool → Tool PAUSES and asks human → Human approves → Tool completes → Agent responds
```
This is called a Long-Running Operation (LRO) - the tool needs to pause, wait for external input (human approval), then resume.
## Agenda:
- Auto-generate small number of images (≤1 image)
- Pauses and asks for approval on large number of images (>1 images)
- Completes or cancels based on the approval decision
This demonstrates the core long-running operation pattern: **`pause → wait for human input → resume`**.
