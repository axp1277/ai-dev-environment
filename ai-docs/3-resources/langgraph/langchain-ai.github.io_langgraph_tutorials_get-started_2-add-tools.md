[ Skip to content ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#add-tools)
**We are growing and hiring for multiple roles for LangChain, LangGraph and LangSmith.[ Join our team!](https://www.langchain.com/careers)**
[ ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg) ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_light.svg) ](https://langchain-ai.github.io/langgraph/ "LangGraph")
LangGraph 
Add tools 
[ ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/?q= "Share")
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
        * Add tools  [ Add tools  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/)
          * [ Prerequisites  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#prerequisites)
          * [ 1. Install the search engine  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#1-install-the-search-engine)
          * [ 2. Configure your environment  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#2-configure-your-environment)
          * [ 3. Define the tool  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#3-define-the-tool)
          * [ 4. Define the graph  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#4-define-the-graph)
          * [ 5. Create a function to run the tools  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#5-create-a-function-to-run-the-tools)
          * [ 6. Define the conditional_edges  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#6-define-the-conditional_edges)
          * [ 7. Visualize the graph (optional)  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#7-visualize-the-graph-optional)
          * [ 8. Ask the bot questions  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#8-ask-the-bot-questions)
          * [ 9. Use prebuilts  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#9-use-prebuilts)
          * [ Next steps  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#next-steps)
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


  * [ Prerequisites  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#prerequisites)
  * [ 1. Install the search engine  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#1-install-the-search-engine)
  * [ 2. Configure your environment  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#2-configure-your-environment)
  * [ 3. Define the tool  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#3-define-the-tool)
  * [ 4. Define the graph  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#4-define-the-graph)
  * [ 5. Create a function to run the tools  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#5-create-a-function-to-run-the-tools)
  * [ 6. Define the conditional_edges  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#6-define-the-conditional_edges)
  * [ 7. Visualize the graph (optional)  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#7-visualize-the-graph-optional)
  * [ 8. Ask the bot questions  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#8-ask-the-bot-questions)
  * [ 9. Use prebuilts  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#9-use-prebuilts)
  * [ Next steps  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#next-steps)


  1. [ Guides  ](https://langchain-ai.github.io/langgraph/)
  2. [ Get started  ](https://langchain-ai.github.io/langgraph/agents/agents/)
  3. [ LangGraph basics  ](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/)

[ ](https://github.com/langchain-ai/langgraph/edit/main/docs/docs/tutorials/get-started/2-add-tools.md "Edit this page")
# Add tools[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#add-tools "Permanent link")
To handle queries you chatbot can't answer "from memory", integrate a web search tool. The chatbot can use this tool to find relevant information and provide better responses.
Note
This tutorial builds on [Build a basic chatbot](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/).
## Prerequisites[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#prerequisites "Permanent link")
Before you start this tutorial, ensure you have the following:
  * An API key for the [Tavily Search Engine](https://python.langchain.com/docs/integrations/tools/tavily_search/).


## 1. Install the search engine[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#1-install-the-search-engine "Permanent link")
Install the requirements to use the [Tavily Search Engine](https://python.langchain.com/docs/integrations/tools/tavily_search/):
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-0-1)pip
```

## 2. Configure your environment[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#2-configure-your-environment "Permanent link")
Configure your environment with your search engine API key:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-1-1)_set_env("TAVILY_API_KEY")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-2-1)TAVILY_API_KEY:  ········

```

## 3. Define the tool[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#3-define-the-tool "Permanent link")
Define the web search tool:
_API Reference:[TavilySearch](https://python.langchain.com/api_reference/tavily/tavily_search/langchain_tavily.tavily_search.TavilySearch.html)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-3-1)fromlangchain_tavilyimport TavilySearch
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-3-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-3-3)tool = TavilySearch(max_results=2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-3-4)tools = [tool]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-3-5)tool.invoke("What's a 'node' in LangGraph?")

```

The results are page summaries our chat bot can use to answer questions:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-1){'query': "What's a 'node' in LangGraph?",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-2)'follow_up_questions': None,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-3)'answer': None,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-4)'images': [],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-5)'results': [{'title': "Introduction to LangGraph: A Beginner's Guide - Medium",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-6)'url': 'https://medium.com/@cplog/introduction-to-langgraph-a-beginners-guide-14f9be027141',
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-7)'content': 'Stateful Graph: LangGraph revolves around the concept of a stateful graph, where each node in the graph represents a step in your computation, and the graph maintains a state that is passed around and updated as the computation progresses. LangGraph supports conditional edges, allowing you to dynamically determine the next node to execute based on the current state of the graph. We define nodes for classifying the input, handling greetings, and handling search queries. def classify_input_node(state): LangGraph is a versatile tool for building complex, stateful applications with LLMs. By understanding its core concepts and working through simple examples, beginners can start to leverage its power for their projects. Remember to pay attention to state management, conditional edges, and ensuring there are no dead-end nodes in your graph.',
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-8)'score': 0.7065353,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-9)'raw_content': None},
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-10){'title': 'LangGraph Tutorial: What Is LangGraph and How to Use It?',
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-11)'url': 'https://www.datacamp.com/tutorial/langgraph-tutorial',
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-12)'content': 'LangGraph is a library within the LangChain ecosystem that provides a framework for defining, coordinating, and executing multiple LLM agents (or chains) in a structured and efficient manner. By managing the flow of data and the sequence of operations, LangGraph allows developers to focus on the high-level logic of their applications rather than the intricacies of agent coordination. Whether you need a chatbot that can handle various types of user requests or a multi-agent system that performs complex tasks, LangGraph provides the tools to build exactly what you need. LangGraph significantly simplifies the development of complex LLM applications by providing a structured framework for managing state and coordinating agent interactions.',
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-13)'score': 0.5008063,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-14)'raw_content': None}],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-4-15)'response_time': 1.38}

```

## 4. Define the graph[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#4-define-the-graph "Permanent link")
For the `StateGraph` you created in the [first tutorial](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/), add `bind_tools` on the LLM. This lets the LLM know the correct JSON format to use if it wants to use the search engine.
Let's first select our LLM:
[OpenAI](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_1_1)[Anthropic](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_1_2)[Azure](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_1_3)[Google Gemini](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_1_4)[AWS Bedrock](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_1_5)
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-5-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-6-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-6-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-6-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-6-4)os.environ["OPENAI_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-6-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-6-6)llm = init_chat_model("openai:gpt-4.1")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-7-1)pip install -U "langchain[anthropic]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-8-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-8-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-8-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-8-4)os.environ["ANTHROPIC_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-8-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-8-6)llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-9-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-4)os.environ["AZURE_OPENAI_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-5)os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-6)os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-8)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-9)    "azure_openai:gpt-4.1",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-10)    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-10-11))

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-11-1)pip install -U "langchain[google-genai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-12-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-12-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-12-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-12-4)os.environ["GOOGLE_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-12-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-12-6)llm = init_chat_model("google_genai:gemini-2.0-flash")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-13-1)pip install -U "langchain[aws]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-4)# Follow the steps here to configure your credentials:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-5)# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-7)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-8)    "anthropic.claude-3-5-sonnet-20240620-v1:0",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-9)    model_provider="bedrock_converse",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-14-10))

```

We can now incorporate it into a `StateGraph`:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-1)fromtypingimport Annotated
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-3)fromtyping_extensionsimport TypedDict
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-4)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-5)fromlanggraph.graphimport StateGraph, START, END
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-6)fromlanggraph.graph.messageimport add_messages
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-8)classState(TypedDict):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-9)    messages: Annotated[list, add_messages]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-10)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-11)graph_builder = StateGraph(State)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-12)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-13)# Modification: tell the LLM which tools it can call
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-14)# highlight-next-line
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-15)llm_with_tools = llm.bind_tools(tools)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-16)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-17)defchatbot(state: State):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-18)    return {"messages": [llm_with_tools.invoke(state["messages"])]}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-19)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-16-20)graph_builder.add_node("chatbot", chatbot)

```

## 5. Create a function to run the tools[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#5-create-a-function-to-run-the-tools "Permanent link")
Now, create a function to run the tools if they are called. Do this by adding the tools to a new node called`BasicToolNode` that checks the most recent message in the state and calls tools if the message contains `tool_calls`. It relies on the LLM's `tool_calling` support, which is available in Anthropic, OpenAI, Google Gemini, and a number of other LLM providers.
_API Reference:[ToolMessage](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.tool.ToolMessage.html)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-1)importjson
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-3)fromlangchain_core.messagesimport ToolMessage
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-4)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-6)classBasicToolNode:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-7)"""A node that runs the tools requested in the last AIMessage."""
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-8)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-9)    def__init__(self, tools: list) -> None:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-10)        self.tools_by_name = {tool.name: tool for tool in tools}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-11)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-12)    def__call__(self, inputs: dict):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-13)        if messages := inputs.get("messages", []):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-14)            message = messages[-1]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-15)        else:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-16)            raise ValueError("No message found in input")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-17)        outputs = []
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-18)        for tool_call in message.tool_calls:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-19)            tool_result = self.tools_by_name[tool_call["name"]].invoke(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-20)                tool_call["args"]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-21)            )
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-22)            outputs.append(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-23)                ToolMessage(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-24)                    content=json.dumps(tool_result),
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-25)                    name=tool_call["name"],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-26)                    tool_call_id=tool_call["id"],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-27)                )
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-28)            )
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-29)        return {"messages": outputs}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-30)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-31)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-32)tool_node = BasicToolNode(tools=[tool])
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-17-33)graph_builder.add_node("tools", tool_node)

```

Note
If you do not want to build this yourself in the future, you can use LangGraph's prebuilt [ToolNode](https://langchain-ai.github.io/langgraph/reference/prebuilt/#toolnode).
## 6. Define the `conditional_edges`[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#6-define-the-conditional_edges "Permanent link")
With the tool node added, now you can define the `conditional_edges`. 
**Edges** route the control flow from one node to the next. **Conditional edges** start from a single node and usually contain "if" statements to route to different nodes depending on the current graph state. These functions receive the current graph `state` and return a string or list of strings indicating which node(s) to call next.
Next, define a router function called `route_tools` that checks for `tool_calls` in the chatbot's output. Provide this function to the graph by calling `add_conditional_edges`, which tells the graph that whenever the `chatbot` node completes to check this function to see where to go next. 
The condition will route to `tools` if tool calls are present and `END` if not. Because the condition can return `END`, you do not need to explicitly set a `finish_point` this time.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-1)defroute_tools(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-2)    state: State,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-3)):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-4)"""
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-5)    Use in the conditional_edge to route to the ToolNode if the last message
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-6)    has tool calls. Otherwise, route to the end.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-7)    """
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-8)    if isinstance(state, list):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-9)        ai_message = state[-1]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-10)    elif messages := state.get("messages", []):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-11)        ai_message = messages[-1]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-12)    else:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-13)        raise ValueError(f"No messages found in input state to tool_edge: {state}")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-14)    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-15)        return "tools"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-16)    return END
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-17)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-18)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-19)# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-20)# it is fine directly responding. This conditional routing defines the main agent loop.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-21)graph_builder.add_conditional_edges(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-22)    "chatbot",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-23)    route_tools,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-24)    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-25)    # It defaults to the identity function, but if you
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-26)    # want to use a node named something else apart from "tools",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-27)    # You can update the value of the dictionary to something else
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-28)    # e.g., "tools": "my_tools"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-29)    {"tools": "tools", END: END},
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-30))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-31)# Any time a tool is called, we return to the chatbot to decide the next step
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-32)graph_builder.add_edge("tools", "chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-33)graph_builder.add_edge(START, "chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-18-34)graph = graph_builder.compile()

```

Note
You can replace this with the prebuilt [tools_condition](https://langchain-ai.github.io/langgraph/reference/prebuilt/#tools_condition) to be more concise. 
## 7. Visualize the graph (optional)[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#7-visualize-the-graph-optional "Permanent link")
You can visualize the graph using the `get_graph` method and one of the "draw" methods, like `draw_ascii` or `draw_png`. The `draw` methods each require additional dependencies.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-19-1)fromIPython.displayimport Image, display
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-19-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-19-3)try:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-19-4)    display(Image(graph.get_graph().draw_mermaid_png()))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-19-5)except Exception:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-19-6)    # This requires some extra dependencies and is optional
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-19-7)    pass

```

![chatbot-with-tools-diagram](https://langchain-ai.github.io/langgraph/tutorials/get-started/chatbot-with-tools.png)
## 8. Ask the bot questions[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#8-ask-the-bot-questions "Permanent link")
Now you can ask the chatbot questions outside its training data:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-1)defstream_graph_updates(user_input: str):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-2)    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-3)        for value in event.values():
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-4)            print("Assistant:", value["messages"][-1].content)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-6)while True:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-7)    try:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-8)        user_input = input("User: ")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-9)        if user_input.lower() in ["quit", "exit", "q"]:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-10)            print("Goodbye!")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-11)            break
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-12)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-13)        stream_graph_updates(user_input)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-14)    except:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-15)        # fallback if input() is not available
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-16)        user_input = "What do you know about LangGraph?"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-17)        print("User: " + user_input)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-18)        stream_graph_updates(user_input)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-20-19)        break

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-1)Assistant: [{'text': "To provide you with accurate and up-to-date information about LangGraph, I'll need to search for the latest details. Let me do that for you.", 'type': 'text'}, {'id': 'toolu_01Q588CszHaSvvP2MxRq9zRD', 'input': {'query': 'LangGraph AI tool information'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-2)Assistant: [{"url": "https://www.langchain.com/langgraph", "content": "LangGraph sets the foundation for how we can build and scale AI workloads \u2014 from conversational agents, complex task automation, to custom LLM-backed experiences that 'just work'. The next chapter in building complex production-ready features with LLMs is agentic, and with LangGraph and LangSmith, LangChain delivers an out-of-the-box solution ..."}, {"url": "https://github.com/langchain-ai/langgraph", "content": "Overview. LangGraph is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows. Compared to other LLM frameworks, it offers these core benefits: cycles, controllability, and persistence. LangGraph allows you to define flows that involve cycles, essential for most agentic architectures ..."}]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-3)Assistant: Based on the search results, I can provide you with information about LangGraph:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-4)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-5)1. Purpose:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-6)   LangGraph is a library designed for building stateful, multi-actor applications with Large Language Models (LLMs). It's particularly useful for creating agent and multi-agent workflows.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-8)2. Developer:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-9)   LangGraph is developed by LangChain, a company known for its tools and frameworks in the AI and LLM space.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-10)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-11)3. Key Features:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-12)   - Cycles: LangGraph allows the definition of flows that involve cycles, which is essential for most agentic architectures.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-13)   - Controllability: It offers enhanced control over the application flow.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-14)   - Persistence: The library provides ways to maintain state and persistence in LLM-based applications.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-15)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-16)4. Use Cases:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-17)   LangGraph can be used for various applications, including:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-18)   - Conversational agents
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-19)   - Complex task automation
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-20)   - Custom LLM-backed experiences
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-21)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-22)5. Integration:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-23)   LangGraph works in conjunction with LangSmith, another tool by LangChain, to provide an out-of-the-box solution for building complex, production-ready features with LLMs.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-24)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-25)6. Significance:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-26)...
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-27)   LangGraph is noted to offer unique benefits compared to other LLM frameworks, particularly in its ability to handle cycles, provide controllability, and maintain persistence.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-28)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-29)LangGraph appears to be a significant tool in the evolving landscape of LLM-based application development, offering developers new ways to create more complex, stateful, and interactive AI systems.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-30)Goodbye!
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-21-31)Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

```

## 9. Use prebuilts[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#9-use-prebuilts "Permanent link")
For ease of use, adjust your code to replace the following with LangGraph prebuilt components. These have built in functionality like parallel API execution.
  * `BasicToolNode` is replaced with the prebuilt [ToolNode](https://langchain-ai.github.io/langgraph/reference/prebuilt/#toolnode)
  * `route_tools` is replaced with the prebuilt [tools_condition](https://langchain-ai.github.io/langgraph/reference/prebuilt/#tools_condition)


[OpenAI](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_2_1)[Anthropic](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_2_2)[Azure](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_2_3)[Google Gemini](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_2_4)[AWS Bedrock](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__tabbed_2_5)
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-22-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-23-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-23-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-23-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-23-4)os.environ["OPENAI_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-23-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-23-6)llm = init_chat_model("openai:gpt-4.1")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-24-1)pip install -U "langchain[anthropic]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-25-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-25-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-25-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-25-4)os.environ["ANTHROPIC_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-25-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-25-6)llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-26-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-4)os.environ["AZURE_OPENAI_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-5)os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-6)os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-8)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-9)    "azure_openai:gpt-4.1",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-10)    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-27-11))

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-28-1)pip install -U "langchain[google-genai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-29-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-29-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-29-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-29-4)os.environ["GOOGLE_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-29-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-29-6)llm = init_chat_model("google_genai:gemini-2.0-flash")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-30-1)pip install -U "langchain[aws]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-4)# Follow the steps here to configure your credentials:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-5)# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-7)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-8)    "anthropic.claude-3-5-sonnet-20240620-v1:0",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-9)    model_provider="bedrock_converse",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-31-10))

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-1)fromtypingimport Annotated
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-3)fromlangchain_tavilyimport TavilySearch
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-4)fromlangchain_core.messagesimport BaseMessage
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-5)fromtyping_extensionsimport TypedDict
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-7)fromlanggraph.graphimport StateGraph, START, END
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-8)fromlanggraph.graph.messageimport add_messages
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-9)fromlanggraph.prebuiltimport ToolNode, tools_condition
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-10)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-11)classState(TypedDict):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-12)    messages: Annotated[list, add_messages]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-13)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-14)graph_builder = StateGraph(State)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-15)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-16)tool = TavilySearch(max_results=2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-17)tools = [tool]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-18)llm_with_tools = llm.bind_tools(tools)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-19)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-20)defchatbot(state: State):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-21)    return {"messages": [llm_with_tools.invoke(state["messages"])]}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-22)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-23)graph_builder.add_node("chatbot", chatbot)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-24)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-25)tool_node = ToolNode(tools=[tool])
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-26)graph_builder.add_node("tools", tool_node)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-27)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-28)graph_builder.add_conditional_edges(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-29)    "chatbot",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-30)    tools_condition,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-31))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-32)# Any time a tool is called, we return to the chatbot to decide the next step
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-33)graph_builder.add_edge("tools", "chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-34)graph_builder.add_edge(START, "chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__codelineno-32-35)graph = graph_builder.compile()

```

**Congratulations!** You've created a conversational agent in LangGraph that can use a search engine to retrieve updated information when needed. Now it can handle a wider range of user queries. To inspect all the steps your agent just took, check out this [LangSmith trace](https://smith.langchain.com/public/4fbd7636-25af-4638-9587-5a02fdbb0172/r).
## Next steps[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#next-steps "Permanent link")
The chatbot cannot remember past interactions on its own, which limits its ability to have coherent, multi-turn conversations. In the next part, you will [add **memory**](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/) to address this.
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! Please help us improve this page by adding to the discussion below. 
[ Previous  Build a basic chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/) [ Next  Add memory  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/)
Copyright © 2025 LangChain, Inc | [Consent Preferences](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/#__consent)
Made with [ Material for MkDocs Insiders ](https://squidfunk.github.io/mkdocs-material/)
[ ](https://langchain-ai.github.io/langgraphjs/ "langchain-ai.github.io") [ ](https://github.com/langchain-ai/langgraph "github.com") [ ](https://twitter.com/LangChainAI "twitter.com")
#### Cookie consent
We use cookies to recognize your repeated visits and preferences, as well as to measure the effectiveness of our documentation and whether users find what they're searching for. **Clicking "Accept" makes our documentation better. Thank you!** ❤️
  *   * 

Accept Reject
