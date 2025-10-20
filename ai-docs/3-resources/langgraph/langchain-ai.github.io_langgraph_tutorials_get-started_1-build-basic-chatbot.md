[ Skip to content ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#build-a-basic-chatbot)
**We are growing and hiring for multiple roles for LangChain, LangGraph and LangSmith.[ Join our team!](https://www.langchain.com/careers)**
[ ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg) ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_light.svg) ](https://langchain-ai.github.io/langgraph/ "LangGraph")
LangGraph 
Build a basic chatbot 
[ ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/?q= "Share")
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
        * Build a basic chatbot  [ Build a basic chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/)
          * [ Prerequisites  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#prerequisites)
          * [ 1. Install packages  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#1-install-packages)
          * [ 2. Create a StateGraph  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#2-create-a-stategraph)
          * [ 3. Add a node  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#3-add-a-node)
          * [ 4. Add an entry point  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#4-add-an-entry-point)
          * [ 5. Compile the graph  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#5-compile-the-graph)
          * [ 6. Visualize the graph (optional)  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#6-visualize-the-graph-optional)
          * [ 7. Run the chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#7-run-the-chatbot)
          * [ Next steps  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#next-steps)
        * [ Add tools  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/)
        * [ Add memory  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/)
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


  * [ Prerequisites  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#prerequisites)
  * [ 1. Install packages  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#1-install-packages)
  * [ 2. Create a StateGraph  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#2-create-a-stategraph)
  * [ 3. Add a node  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#3-add-a-node)
  * [ 4. Add an entry point  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#4-add-an-entry-point)
  * [ 5. Compile the graph  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#5-compile-the-graph)
  * [ 6. Visualize the graph (optional)  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#6-visualize-the-graph-optional)
  * [ 7. Run the chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#7-run-the-chatbot)
  * [ Next steps  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#next-steps)


  1. [ Guides  ](https://langchain-ai.github.io/langgraph/)
  2. [ Get started  ](https://langchain-ai.github.io/langgraph/agents/agents/)
  3. [ LangGraph basics  ](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/)

[ ](https://github.com/langchain-ai/langgraph/edit/main/docs/docs/tutorials/get-started/1-build-basic-chatbot.md "Edit this page")
# Build a basic chatbot[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#build-a-basic-chatbot "Permanent link")
In this tutorial, you will build a basic chatbot. This chatbot is the basis for the following series of tutorials where you will progressively add more sophisticated capabilities, and be introduced to key LangGraph concepts along the way. Let’s dive in! 🌟
## Prerequisites[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#prerequisites "Permanent link")
Before you start this tutorial, ensure you have access to a LLM that supports tool-calling features, such as [OpenAI](https://platform.openai.com/api-keys), [Anthropic](https://console.anthropic.com/settings/admin-keys), or [Google Gemini](https://ai.google.dev/gemini-api/docs/api-key).
## 1. Install packages[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#1-install-packages "Permanent link")
Install the required packages:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-0-1)pip
```

Tip
Sign up for LangSmith to quickly spot issues and improve the performance of your LangGraph projects. LangSmith lets you use trace data to debug, test, and monitor your LLM apps built with LangGraph. For more information on how to get started, see [LangSmith docs](https://docs.smith.langchain.com). 
## 2. Create a `StateGraph`[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#2-create-a-stategraph "Permanent link")
Now you can create a basic chatbot using LangGraph. This chatbot will respond directly to user messages.
Start by creating a `StateGraph`. A `StateGraph` object defines the structure of our chatbot as a "state machine". We'll add `nodes` to represent the llm and functions our chatbot can call and `edges` to specify how the bot should transition between these functions.
_API Reference:[StateGraph](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) | [START](https://langchain-ai.github.io/langgraph/reference/constants/#langgraph.constants.START) | [add_messages](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.message.add_messages)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-1)fromtypingimport Annotated
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-3)fromtyping_extensionsimport TypedDict
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-4)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-5)fromlanggraph.graphimport StateGraph, START
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-6)fromlanggraph.graph.messageimport add_messages
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-8)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-9)classState(TypedDict):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-10)    # Messages have the type "list". The `add_messages` function
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-11)    # in the annotation defines how this state key should be updated
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-12)    # (in this case, it appends messages to the list, rather than overwriting them)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-13)    messages: Annotated[list, add_messages]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-14)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-15)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-1-16)graph_builder = StateGraph(State)

```

Our graph can now handle two key tasks:
  1. Each `node` can receive the current `State` as input and output an update to the state.
  2. Updates to `messages` will be appended to the existing list rather than overwriting it, thanks to the prebuilt [`add_messages`](https://langchain-ai.github.io/langgraph/reference/graphs/?h=add+messages#add_messages) function used with the `Annotated` syntax.


* * *
Concept
When defining a graph, the first step is to define its `State`. The `State` includes the graph's schema and [reducer functions](https://langchain-ai.github.io/langgraph/concepts/low_level/#reducers) that handle state updates. In our example, `State` is a `TypedDict` with one key: `messages`. The [`add_messages`](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.message.add_messages) reducer function is used to append new messages to the list instead of overwriting it. Keys without a reducer annotation will overwrite previous values. To learn more about state, reducers, and related concepts, see [LangGraph reference docs](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.message.add_messages).
## 3. Add a node[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#3-add-a-node "Permanent link")
Next, add a "`chatbot`" node. **Nodes** represent units of work and are typically regular Python functions.
Let's first select a chat model:
[OpenAI](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__tabbed_1_1)[Anthropic](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__tabbed_1_2)[Azure](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__tabbed_1_3)[Google Gemini](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__tabbed_1_4)[AWS Bedrock](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__tabbed_1_5)
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-2-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-3-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-3-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-3-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-3-4)os.environ["OPENAI_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-3-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-3-6)llm = init_chat_model("openai:gpt-4.1")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-4-1)pip install -U "langchain[anthropic]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-5-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-5-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-5-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-5-4)os.environ["ANTHROPIC_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-5-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-5-6)llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-6-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-4)os.environ["AZURE_OPENAI_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-5)os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-6)os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-8)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-9)    "azure_openai:gpt-4.1",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-10)    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-7-11))

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-8-1)pip install -U "langchain[google-genai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-9-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-9-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-9-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-9-4)os.environ["GOOGLE_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-9-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-9-6)llm = init_chat_model("google_genai:gemini-2.0-flash")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-10-1)pip install -U "langchain[aws]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-4)# Follow the steps here to configure your credentials:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-5)# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-7)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-8)    "anthropic.claude-3-5-sonnet-20240620-v1:0",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-9)    model_provider="bedrock_converse",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-11-10))

```

We can now incorporate the chat model into a simple node:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-13-1)defchatbot(state: State):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-13-2)    return {"messages": [llm.invoke(state["messages"])]}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-13-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-13-4)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-13-5)# The first argument is the unique node name
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-13-6)# The second argument is the function or object that will be called whenever
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-13-7)# the node is used.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-13-8)graph_builder.add_node("chatbot", chatbot)

```

**Notice** how the `chatbot` node function takes the current `State` as input and returns a dictionary containing an updated `messages` list under the key "messages". This is the basic pattern for all LangGraph node functions.
The `add_messages` function in our `State` will append the LLM's response messages to whatever messages are already in the state.
## 4. Add an `entry` point[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#4-add-an-entry-point "Permanent link")
Add an `entry` point to tell the graph **where to start its work** each time it is run:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-14-1)graph_builder.add_edge(START, "chatbot")

```

## 5. Compile the graph[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#5-compile-the-graph "Permanent link")
Before running the graph, we'll need to compile it. We can do so by calling `compile()` on the graph builder. This creates a `CompiledGraph` we can invoke on our state.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-15-1)graph = graph_builder.compile()

```

## 6. Visualize the graph (optional)[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#6-visualize-the-graph-optional "Permanent link")
You can visualize the graph using the `get_graph` method and one of the "draw" methods, like `draw_ascii` or `draw_png`. The `draw` methods each require additional dependencies.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-16-1)fromIPython.displayimport Image, display
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-16-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-16-3)try:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-16-4)    display(Image(graph.get_graph().draw_mermaid_png()))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-16-5)except Exception:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-16-6)    # This requires some extra dependencies and is optional
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-16-7)    pass

```

![basic chatbot diagram](https://langchain-ai.github.io/langgraph/tutorials/get-started/basic-chatbot.png)
## 7. Run the chatbot[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#7-run-the-chatbot "Permanent link")
Now run the chatbot! 
Tip
You can exit the chat loop at any time by typing `quit`, `exit`, or `q`.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-1)defstream_graph_updates(user_input: str):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-2)    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-3)        for value in event.values():
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-4)            print("Assistant:", value["messages"][-1].content)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-7)while True:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-8)    try:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-9)        user_input = input("User: ")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-10)        if user_input.lower() in ["quit", "exit", "q"]:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-11)            print("Goodbye!")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-12)            break
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-13)        stream_graph_updates(user_input)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-14)    except:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-15)        # fallback if input() is not available
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-16)        user_input = "What do you know about LangGraph?"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-17)        print("User: " + user_input)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-18)        stream_graph_updates(user_input)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-17-19)        break

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-18-1)Assistant: LangGraph is a library designed to help build stateful multi-agent applications using language models. It provides tools for creating workflows and state machines to coordinate multiple AI agents or language model interactions. LangGraph is built on top of LangChain, leveraging its components while adding graph-based coordination capabilities. It's particularly useful for developing more complex, stateful AI applications that go beyond simple query-response interactions.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-18-2)Goodbye!

```

**Congratulations!** You've built your first chatbot using LangGraph. This bot can engage in basic conversation by taking user input and generating responses using an LLM. You can inspect a [LangSmith Trace](https://smith.langchain.com/public/7527e308-9502-4894-b347-f34385740d5a/r) for the call above.
Below is the full code for this tutorial:
_API Reference:[init_chat_model](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html) | [StateGraph](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) | [START](https://langchain-ai.github.io/langgraph/reference/constants/#langgraph.constants.START) | [add_messages](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.message.add_messages)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-1)fromtypingimport Annotated
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-3)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-4)fromtyping_extensionsimport TypedDict
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-6)fromlanggraph.graphimport StateGraph, START
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-7)fromlanggraph.graph.messageimport add_messages
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-8)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-9)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-10)classState(TypedDict):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-11)    messages: Annotated[list, add_messages]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-12)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-13)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-14)graph_builder = StateGraph(State)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-15)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-16)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-17)llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-18)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-19)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-20)defchatbot(state: State):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-21)    return {"messages": [llm.invoke(state["messages"])]}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-22)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-23)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-24)# The first argument is the unique node name
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-25)# The second argument is the function or object that will be called whenever
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-26)# the node is used.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-27)graph_builder.add_node("chatbot", chatbot)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-28)graph_builder.add_edge(START, "chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__codelineno-19-29)graph = graph_builder.compile()

```

## Next steps[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#next-steps "Permanent link")
You may have noticed that the bot's knowledge is limited to what's in its training data. In the next part, we'll [add a web search tool](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/) to expand the bot's knowledge and make it more capable.
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! Please help us improve this page by adding to the discussion below. 
[ Previous  Overview  ](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/) [ Next  Add tools  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/)
Copyright © 2025 LangChain, Inc | [Consent Preferences](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/#__consent)
Made with [ Material for MkDocs Insiders ](https://squidfunk.github.io/mkdocs-material/)
[ ](https://langchain-ai.github.io/langgraphjs/ "langchain-ai.github.io") [ ](https://github.com/langchain-ai/langgraph "github.com") [ ](https://twitter.com/LangChainAI "twitter.com")
#### Cookie consent
We use cookies to recognize your repeated visits and preferences, as well as to measure the effectiveness of our documentation and whether users find what they're searching for. **Clicking "Accept" makes our documentation better. Thank you!** ❤️
  *   * 

Accept Reject
