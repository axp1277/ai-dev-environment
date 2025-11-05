[ Skip to content ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#add-memory)
**We are growing and hiring for multiple roles for LangChain, LangGraph and LangSmith.[ Join our team!](https://www.langchain.com/careers)**
[ ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg) ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_light.svg) ](https://langchain-ai.github.io/langgraph/ "LangGraph")
LangGraph 
Add memory 
[ ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/?q= "Share")
Type to start searching
[ GitHub  ](https://github.com/langchain-ai/langgraph "Go to repository")
  * [ Guides ](https://langchain-ai.github.io/langgraph/)
  * [ Reference ](https://langchain-ai.github.io/langgraph/reference/)
  * [ Examples ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
  * [ Resources ](https://langchain-ai.github.io/langgraph/concepts/faq/)


[ ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg) ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_light.svg) ](https://langchain-ai.github.io/langgraph/ "LangGraph") LangGraph 
[ GitHub  ](https://github.com/langchain-ai/langgraph "Go to repository")
  * [ Guides  ](https://langchain-ai.github.io/langgraph/)
    * Get started 
      * [ Quickstart  ](https://langchain-ai.github.io/langgraph/agents/agents/)
      * LangGraph basics 
        * [ Overview  ](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/)
        * [ Build a basic chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/)
        * [ Add tools  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/)
        * Add memory  [ Add memory  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/)
          * [ 1. Create a MemorySaver checkpointer  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#1-create-a-memorysaver-checkpointer)
          * [ 2. Compile the graph  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#2-compile-the-graph)
          * [ 3. Interact with your chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#3-interact-with-your-chatbot)
          * [ 4. Ask a follow up question  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#4-ask-a-follow-up-question)
          * [ 5. Inspect the state  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#5-inspect-the-state)
          * [ Next steps  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#next-steps)
        * [ Add human-in-the-loop  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/4-human-in-the-loop/)
        * [ Customize state  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/)
        * [ Time travel  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/6-time-travel/)
      * [ Deployment  ](https://langchain-ai.github.io/langgraph/tutorials/deployment/)
    * Prebuilt agents 
      * [ Overview  ](https://langchain-ai.github.io/langgraph/agents/overview/)
      * [ Running agents  ](https://langchain-ai.github.io/langgraph/agents/run_agents/)
      * [ Streaming  ](https://langchain-ai.github.io/langgraph/agents/streaming/)
      * [ Models  ](https://langchain-ai.github.io/langgraph/agents/models/)
      * [ Tools  ](https://langchain-ai.github.io/langgraph/agents/tools/)
      * [ MCP Integration  ](https://langchain-ai.github.io/langgraph/agents/mcp/)
      * [ Context  ](https://langchain-ai.github.io/langgraph/agents/context/)
      * [ Memory  ](https://langchain-ai.github.io/langgraph/agents/memory/)
      * [ Human-in-the-loop  ](https://langchain-ai.github.io/langgraph/agents/human-in-the-loop/)
      * [ Multi-agent  ](https://langchain-ai.github.io/langgraph/agents/multi-agent/)
      * [ Evals  ](https://langchain-ai.github.io/langgraph/agents/evals/)
      * [ Deployment  ](https://langchain-ai.github.io/langgraph/agents/deployment/)
      * [ UI  ](https://langchain-ai.github.io/langgraph/agents/ui/)
    * LangGraph framework 
      * [ Agent architectures  ](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/)
      * [ Graphs  ](https://langchain-ai.github.io/langgraph/concepts/low_level/)
      * [ Streaming  ](https://langchain-ai.github.io/langgraph/concepts/streaming/)
      * [ Persistence  ](https://langchain-ai.github.io/langgraph/concepts/persistence/)
      * [ Memory  ](https://langchain-ai.github.io/langgraph/concepts/memory/)
      * [ Human-in-the-loop  ](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)
      * [ Breakpoints  ](https://langchain-ai.github.io/langgraph/concepts/breakpoints/)
      * [ Time travel  ](https://langchain-ai.github.io/langgraph/concepts/time-travel/)
      * [ Tools  ](https://langchain-ai.github.io/langgraph/concepts/tools/)
      * [ Subgraphs  ](https://langchain-ai.github.io/langgraph/concepts/subgraphs/)
      * [ Multi-agent  ](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
      * [ Functional API  ](https://langchain-ai.github.io/langgraph/concepts/functional_api/)
      * [ LangGraph's Runtime (Pregel)  ](https://langchain-ai.github.io/langgraph/concepts/pregel/)
      * [ Other  ](https://langchain-ai.github.io/langgraph/how-tos/async/)
    * LangGraph Platform 
      * [ Overview  ](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/)
      * [ Get started  ](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/)
      * [ Components  ](https://langchain-ai.github.io/langgraph/concepts/langgraph_components/)
      * [ Data management  ](https://langchain-ai.github.io/langgraph/cloud/deployment/semantic_search/)
      * [ Authentication & access control  ](https://langchain-ai.github.io/langgraph/concepts/auth/)
      * [ Assistants  ](https://langchain-ai.github.io/langgraph/concepts/assistants/)
      * [ Threads  ](https://langchain-ai.github.io/langgraph/cloud/concepts/threads/)
      * [ Runs  ](https://langchain-ai.github.io/langgraph/cloud/concepts/runs/)
      * [ Streaming  ](https://langchain-ai.github.io/langgraph/cloud/concepts/streaming/)
      * [ Human-in-the-loop  ](https://langchain-ai.github.io/langgraph/cloud/how-tos/human_in_the_loop_breakpoint/)
      * [ MCP  ](https://langchain-ai.github.io/langgraph/concepts/server-mcp/)
      * [ Double-texting  ](https://langchain-ai.github.io/langgraph/concepts/double_texting/)
      * [ Webhooks  ](https://langchain-ai.github.io/langgraph/cloud/concepts/webhooks/)
      * [ Cron Jobs  ](https://langchain-ai.github.io/langgraph/cloud/concepts/cron_jobs/)
      * [ Server Customization  ](https://langchain-ai.github.io/langgraph/how-tos/http/custom_lifespan/)
      * [ Deployment  ](https://langchain-ai.github.io/langgraph/concepts/deployment_options/)
  * [ Reference  ](https://langchain-ai.github.io/langgraph/reference/)
  * [ Examples  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
  * [ Resources  ](https://langchain-ai.github.io/langgraph/concepts/faq/)


  * [ 1. Create a MemorySaver checkpointer  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#1-create-a-memorysaver-checkpointer)
  * [ 2. Compile the graph  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#2-compile-the-graph)
  * [ 3. Interact with your chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#3-interact-with-your-chatbot)
  * [ 4. Ask a follow up question  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#4-ask-a-follow-up-question)
  * [ 5. Inspect the state  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#5-inspect-the-state)
  * [ Next steps  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#next-steps)


  1. [ Guides  ](https://langchain-ai.github.io/langgraph/)
  2. [ Get started  ](https://langchain-ai.github.io/langgraph/agents/agents/)
  3. [ LangGraph basics  ](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/)

[ ](https://github.com/langchain-ai/langgraph/edit/main/docs/docs/tutorials/get-started/3-add-memory.md "Edit this page")
# Add memory[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#add-memory "Permanent link")
The chatbot can now [use tools](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/) to answer user questions, but it does not remember the context of previous interactions. This limits its ability to have coherent, multi-turn conversations.
LangGraph solves this problem through **persistent checkpointing**. If you provide a `checkpointer` when compiling the graph and a `thread_id` when calling your graph, LangGraph automatically saves the state after each step. When you invoke the graph again using the same `thread_id`, the graph loads its saved state, allowing the chatbot to pick up where it left off. 
We will see later that **checkpointing** is _much_ more powerful than simple chat memory - it lets you save and resume complex state at any time for error recovery, human-in-the-loop workflows, time travel interactions, and more. But first, let's add checkpointing to enable multi-turn conversations.
Note
This tutorial builds on [Add tools](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/).
## 1. Create a `MemorySaver` checkpointer[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#1-create-a-memorysaver-checkpointer "Permanent link")
Create a `MemorySaver` checkpointer:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-0-1)fromlanggraph.checkpoint.memoryimport MemorySaver
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-0-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-0-3)memory = MemorySaver()

```

This is in-memory checkpointer, which is convenient for the tutorial. However, in a production application, you would likely change this to use `SqliteSaver` or `PostgresSaver` and connect a database.
## 2. Compile the graph[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#2-compile-the-graph "Permanent link")
Compile the graph with the provided checkpointer, which will checkpoint the `State` as the graph works through each node:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-1-1)graph = graph_builder.compile(checkpointer=memory)

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-2-1)fromIPython.displayimport Image, display
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-2-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-2-3)try:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-2-4)    display(Image(graph.get_graph().draw_mermaid_png()))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-2-5)except Exception:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-2-6)    # This requires some extra dependencies and is optional
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-2-7)    pass

```

## 3. Interact with your chatbot[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#3-interact-with-your-chatbot "Permanent link")
Now you can interact with your bot!
  1. Pick a thread to use as the key for this conversation.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-3-1)config = {"configurable": {"thread_id": "1"}}

```

  2. Call your chatbot:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-1)user_input = "Hi there! My name is Will."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-3)# The config is the **second positional argument** to stream() or invoke()!
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-4)events = graph.stream(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-5)    {"messages": [{"role": "user", "content": user_input}]},
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-6)    config,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-7)    stream_mode="values",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-8))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-9)for event in events:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-4-10)    event["messages"][-1].pretty_print()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-5-1)================================ Human Message =================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-5-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-5-3)Hi there! My name is Will.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-5-4)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-5-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-5-6)Hello Will! It's nice to meet you. How can I assist you today? Is there anything specific you'd like to know or discuss?

```

Note
The config was provided as the **second positional argument** when calling our graph. It importantly is _not_ nested within the graph inputs (`{'messages': []}`).


## 4. Ask a follow up question[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#4-ask-a-follow-up-question "Permanent link")
Ask a follow up question:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-1)user_input = "Remember my name?"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-3)# The config is the **second positional argument** to stream() or invoke()!
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-4)events = graph.stream(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-5)    {"messages": [{"role": "user", "content": user_input}]},
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-6)    config,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-7)    stream_mode="values",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-8))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-9)for event in events:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-6-10)    event["messages"][-1].pretty_print()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-7-1)================================ Human Message =================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-7-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-7-3)Remember my name?
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-7-4)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-7-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-7-6)Of course, I remember your name, Will. I always try to pay attention to important details that users share with me. Is there anything else you'd like to talk about or any questions you have? I'm here to help with a wide range of topics or tasks.

```

**Notice** that we aren't using an external list for memory: it's all handled by the checkpointer! You can inspect the full execution in this [LangSmith trace](https://smith.langchain.com/public/29ba22b5-6d40-4fbe-8d27-b369e3329c84/r) to see what's going on.
Don't believe me? Try this using a different config.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-8-1)# The only difference is we change the `thread_id` here to "2" instead of "1"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-8-2)events = graph.stream(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-8-3)    {"messages": [{"role": "user", "content": user_input}]},
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-8-4)    {"configurable": {"thread_id": "2"}},
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-8-5)    stream_mode="values",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-8-6))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-8-7)for event in events:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-8-8)    event["messages"][-1].pretty_print()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-9-1)================================ Human Message =================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-9-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-9-3)Remember my name?
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-9-4)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-9-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-9-6)I apologize, but I don't have any previous context or memory of your name. As an AI assistant, I don't retain information from past conversations. Each interaction starts fresh. Could you please tell me your name so I can address you properly in this conversation?

```

**Notice** that the **only** change we've made is to modify the `thread_id` in the config. See this call's [LangSmith trace](https://smith.langchain.com/public/51a62351-2f0a-4058-91cc-9996c5561428/r) for comparison.
## 5. Inspect the state[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#5-inspect-the-state "Permanent link")
By now, we have made a few checkpoints across two different threads. But what goes into a checkpoint? To inspect a graph's `state` for a given config at any time, call `get_state(config)`.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-10-1)snapshot = graph.get_state(config)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-10-2)snapshot

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-11-1)StateSnapshot(values={'messages': [HumanMessage(content='Hi there! My name is Will.', additional_kwargs={}, response_metadata={}, id='8c1ca919-c553-4ebf-95d4-b59a2d61e078'), AIMessage(content="Hello Will! It's nice to meet you. How can I assist you today? Is there anything specific you'd like to know or discuss?", additional_kwargs={}, response_metadata={'id': 'msg_01WTQebPhNwmMrmmWojJ9KXJ', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 405, 'output_tokens': 32}}, id='run-58587b77-8c82-41e6-8a90-d62c444a261d-0', usage_metadata={'input_tokens': 405, 'output_tokens': 32, 'total_tokens': 437}), HumanMessage(content='Remember my name?', additional_kwargs={}, response_metadata={}, id='daba7df6-ad75-4d6b-8057-745881cea1ca'), AIMessage(content="Of course, I remember your name, Will. I always try to pay attention to important details that users share with me. Is there anything else you'd like to talk about or any questions you have? I'm here to help with a wide range of topics or tasks.", additional_kwargs={}, response_metadata={'id': 'msg_01E41KitY74HpENRgXx94vag', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 444, 'output_tokens': 58}}, id='run-ffeaae5c-4d2d-4ddb-bd59-5d5cbf2a5af8-0', usage_metadata={'input_tokens': 444, 'output_tokens': 58, 'total_tokens': 502})]}, next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef7d06e-93e0-6acc-8004-f2ac846575d2'}}, metadata={'source': 'loop', 'writes': {'chatbot': {'messages': [AIMessage(content="Of course, I remember your name, Will. I always try to pay attention to important details that users share with me. Is there anything else you'd like to talk about or any questions you have? I'm here to help with a wide range of topics or tasks.", additional_kwargs={}, response_metadata={'id': 'msg_01E41KitY74HpENRgXx94vag', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 444, 'output_tokens': 58}}, id='run-ffeaae5c-4d2d-4ddb-bd59-5d5cbf2a5af8-0', usage_metadata={'input_tokens': 444, 'output_tokens': 58, 'total_tokens': 502})]}}, 'step': 4, 'parents': {}}, created_at='2024-09-27T19:30:10.820758+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef7d06e-859f-6206-8003-e1bd3c264b8f'}}, tasks=())

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-12-1)snapshot.next  # (since the graph ended this turn, `next` is empty. If you fetch a state from within a graph invocation, next tells which node will execute next)

```

The snapshot above contains the current state values, corresponding config, and the `next` node to process. In our case, the graph has reached an `END` state, so `next` is empty.
**Congratulations!** Your chatbot can now maintain conversation state across sessions thanks to LangGraph's checkpointing system. This opens up exciting possibilities for more natural, contextual interactions. LangGraph's checkpointing even handles **arbitrarily complex graph states** , which is much more expressive and powerful than simple chat memory.
Check out the code snippet below to review the graph from this tutorial:
[OpenAI](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__tabbed_1_1)[Anthropic](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__tabbed_1_2)[Azure](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__tabbed_1_3)[Google Gemini](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__tabbed_1_4)[AWS Bedrock](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__tabbed_1_5)
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-13-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-14-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-14-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-14-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-14-4)os.environ["OPENAI_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-14-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-14-6)llm = init_chat_model("openai:gpt-4.1")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-15-1)pip install -U "langchain[anthropic]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-16-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-16-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-16-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-16-4)os.environ["ANTHROPIC_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-16-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-16-6)llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-17-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-4)os.environ["AZURE_OPENAI_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-5)os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-6)os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-8)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-9)    "azure_openai:gpt-4.1",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-10)    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-18-11))

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-19-1)pip install -U "langchain[google-genai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-20-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-20-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-20-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-20-4)os.environ["GOOGLE_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-20-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-20-6)llm = init_chat_model("google_genai:gemini-2.0-flash")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-21-1)pip install -U "langchain[aws]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-4)# Follow the steps here to configure your credentials:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-5)# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-7)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-8)    "anthropic.claude-3-5-sonnet-20240620-v1:0",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-9)    model_provider="bedrock_converse",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-22-10))

```

_API Reference:[init_chat_model](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html) | [TavilySearch](https://python.langchain.com/api_reference/tavily/tavily_search/langchain_tavily.tavily_search.TavilySearch.html) | [BaseMessage](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.base.BaseMessage.html) | [MemorySaver](https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.memory.MemorySaver) | [StateGraph](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) | [add_messages](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.message.add_messages) | [ToolNode](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.ToolNode) | [tools_condition](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.tools_condition)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-1)fromtypingimport Annotated
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-3)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-4)fromlangchain_tavilyimport TavilySearch
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-5)fromlangchain_core.messagesimport BaseMessage
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-6)fromtyping_extensionsimport TypedDict
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-8)fromlanggraph.checkpoint.memoryimport MemorySaver
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-9)fromlanggraph.graphimport StateGraph
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-10)fromlanggraph.graph.messageimport add_messages
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-11)fromlanggraph.prebuiltimport ToolNode, tools_condition
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-12)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-13)classState(TypedDict):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-14)    messages: Annotated[list, add_messages]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-15)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-16)graph_builder = StateGraph(State)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-17)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-18)tool = TavilySearch(max_results=2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-19)tools = [tool]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-20)llm_with_tools = llm.bind_tools(tools)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-21)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-22)defchatbot(state: State):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-23)    return {"messages": [llm_with_tools.invoke(state["messages"])]}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-24)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-25)graph_builder.add_node("chatbot", chatbot)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-26)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-27)tool_node = ToolNode(tools=[tool])
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-28)graph_builder.add_node("tools", tool_node)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-29)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-30)graph_builder.add_conditional_edges(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-31)    "chatbot",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-32)    tools_condition,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-33))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-34)graph_builder.add_edge("tools", "chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-35)graph_builder.set_entry_point("chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-36)memory = MemorySaver()
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__codelineno-24-37)graph = graph_builder.compile(checkpointer=memory)

```

## Next steps[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#next-steps "Permanent link")
In the next tutorial, you will [add human-in-the-loop to the chatbot](https://langchain-ai.github.io/langgraph/tutorials/get-started/4-human-in-the-loop/) to handle situations where it may need guidance or verification before proceeding.
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! Please help us improve this page by adding to the discussion below. 
[ Previous  Add tools  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/) [ Next  Add human-in-the-loop  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/4-human-in-the-loop/)
Copyright © 2025 LangChain, Inc | [Consent Preferences](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#__consent)
Made with [ Material for MkDocs Insiders ](https://squidfunk.github.io/mkdocs-material/)
[ ](https://langchain-ai.github.io/langgraphjs/ "langchain-ai.github.io") [ ](https://github.com/langchain-ai/langgraph "github.com") [ ](https://twitter.com/LangChainAI "twitter.com")
#### Cookie consent
We use cookies to recognize your repeated visits and preferences, as well as to measure the effectiveness of our documentation and whether users find what they're searching for. **Clicking "Accept" makes our documentation better. Thank you!** ❤️
  *   * 

Accept Reject
