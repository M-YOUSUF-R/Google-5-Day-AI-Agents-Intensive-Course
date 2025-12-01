# Working with Session State
## why session state?
While we can do Context Compaction and use a database to resume a session, we face new challenges now. In some cases, we have key information or preferences that we want to share across other sessions.

In these scenarios, instead of sharing the entire session history, transferring information from a few key variables can improve the session experience.

## Creating custom tools for Session state management
Let's explore how to manually manage session state through `custom tools`. In this example, we'll identify a **transferable characteristic**, like a user's name and their country with other datas, and create tools to capture and save it.

## Key Concept:
- Tools can access `tool_context.state` to read/write session state
- Use descriptive key prefixes (`user:`, `app:`, `temp:`) for organization
- State persists across conversation turns within the same session
