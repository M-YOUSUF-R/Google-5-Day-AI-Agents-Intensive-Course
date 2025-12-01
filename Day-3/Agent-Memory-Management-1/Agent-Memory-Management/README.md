# Agent Memory Management-1
## Session:
A session is a container for conversations. It encapsulates the conversation history in a chronological manner and also records all tool interactions and responses for a single, continuous conversation. A session is tied to a user and agent; it is not shared with other users. Similarly, a session history for an Agent is not shared with other Agents.
### In ADK, a Session is comprised of two key components Events and State:

**📝 Session.Events:**

While a session is a container for conversations, Events are the building blocks of a conversation.

*Example of Events:*

- User Input: A message from the user (text, audio, image, etc.)
- Agent Response: The agent's reply to the user
- Tool Call: The agent's decision to use an external tool or API
- Tool Output: The data returned from a tool call, which the agent uses to continue its reasoning

**{} Session.State:**

`session.state` is the Agent's scratchpad, where it stores and updates dynamic details needed during the conversation. Think of it as a global `{key, value}` pair storage which is available to all subagents and tools.\
![session.state image](https://storage.googleapis.com/github-repo/kaggle-5days-ai/day3/session-state-and-events.png)

## How to manage sessions?¶
An agentic application can have multiple users and each user may have multiple sessions with the application. To manage these sessions and events, ADK offers a Session Manager and Runner.

1. **SessionService: The storage layer**

    - Manages creation, storage, and retrieval of session data
    - Different implementations for different needs (memory, database, cloud)
2. **Runner: The orchestration layer**

    - Manages the flow of information between user and agent
    - Automatically maintains conversation history
    - Handles the Context Engineering behind the scenes

**Think of it like this:**
- Session = A notebook 📓
- Events = Individual entries in a single page 📝
- SessionService = The filing cabinet storing notebooks 🗄️
- Runner = The assistant managing the conversation 🤖

## Presistent Session with `InMemorySessionService()`
**ADK offers different types of sessions suitable for different needs. As a start, we'll start with a simple Session Management option `InMemorySessionService`**
### **Input:** *in `tempmemory.py`*
```py
await run_session(
    runner,
    a1, # it will be forgotten after the program / kernel restart.
    #a2, # it has no Idea about `a1`.
    # a3, # it as it reminds , it will answer all questions.
    "stateful-agentic-session"
)
```
### **Output:**
```powershell
Agent-Memory-Management-1> python main.py

 ### Session: stateful-agentic-session
session created...

User >  Hi, I am Yousuf! What is the capital of United States?
gemini-2.5-flash>  Hi Yousuf! The capital of the United States is Washington, D.C.

User >  Hello! What is my name?
gemini-2.5-flash>  Hello Yousuf!
```
### **Input:** *in `tempmemory.py`*
```py
await run_session(
    runner,
    # a1, # it will be forgotten after the program / kernel restart.
    a2, # it has no Idea about `a1`.
    # a3, # it as it reminds , it will answer all questions.
    "stateful-agentic-session"
)
```
### **Output:**
```powershell
Agent-Memory-Management-1> python .\main.py

 ### Session: stateful-agentic-session
session created...

User >  What did I ask you about earlier?
gemini-2.5-flash>  I'm sorry, but as an AI, I don't have memory of past conversations. Each interaction is fresh for me. Could you please remind me what you asked about earlier?

User >  And remind me, what's my name?
gemini-2.5-flash>  I'm sorry, but I don't know your name. I don't retain personal information or memory of past conversations. Each interaction with me is independent.
```
### *It seems that, when the code run again/ kenrel restarted , As previous history was saved temporarily , AI didn't fetched data and faild to get the context.*

## Persistent Sessions with `DatabaseSessionService()`
**While `InMemorySessionService` is great for prototyping, real-world applications need conversations to survive restarts, crashes, and deployments. Let's level up to persistent storage!**\
**So we upgrade to DatabaseSessionService using SQLite. This gives us persistence without needing a separate database server for this demo.**
### **Input:** *in `dbmemory.py`*
```py
await run_session(
    runner,
    a1, # initial input
    "test-db-session-01",
)
```
### **Output:**
```powershell
Agent-Memory-Management-1> python .\app.py

 ### Session: test-db-session-01
session created...

User >  Hi, I am Yousuf! What is the capital of United States?
gemini-2.5-flash>  Hi Yousuf! The capital of the United States is Washington, D.C.

User >  Hello! What is my name?
gemini-2.5-flash>  Your name is Yousuf!
```
### **Input:** *in `dbmemory.py`*
```py
await run_session(
    runner,
    a2,# input changed...
    "test-db-session-01",
)
```
### **Output:**
```powershell
Agent-Memory-Management-1> python .\app.py

 ### Session: test-db-session-01
session found...

User >  What did I ask you about earlier?
gemini-2.5-flash>  You asked me about the capital of the United States and what your name is.

User >  And remind me, what is my name?
gemini-2.5-flash>  Your name is Yousuf.
```
### *It seems that, though the code run again/ kenrel restarted , previous history was saved and AI fetched data from database based on the session.*

## Choosing the Right SessionService:
| Service | Use Case | 	Persistence | Best For |
|---------|----------|--------------|----------|
| `InMemorySessionService` | Development & Testing | ❌ Lost on restart | 	Quick prototypes |
| `DatabaseSessionService` | Self-managed apps | ✅ Survives restart | Small to medium apps |
| Agent Engine Sessions | Production on GCP | ✅ Fully managed | Enterprise scale |

