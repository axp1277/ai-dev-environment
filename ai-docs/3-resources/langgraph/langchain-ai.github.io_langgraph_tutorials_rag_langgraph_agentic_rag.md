[ Skip to content ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#agentic-rag)
**We are growing and hiring for multiple roles for LangChain, LangGraph and LangSmith.[ Join our team!](https://www.langchain.com/careers)**
[ ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg) ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_light.svg) ](https://langchain-ai.github.io/langgraph/ "LangGraph")
LangGraph 
Agentic RAG 
[ ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/?q= "Share")
Initializing search 
[ GitHub  ](https://github.com/langchain-ai/langgraph "Go to repository")
  * [ Guides ](https://langchain-ai.github.io/langgraph/)
  * [ Reference ](https://langchain-ai.github.io/langgraph/reference/)
  * [ Examples ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
  * [ Resources ](https://langchain-ai.github.io/langgraph/concepts/faq/)


[ ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg) ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_light.svg) ](https://langchain-ai.github.io/langgraph/ "LangGraph") LangGraph 
[ GitHub  ](https://github.com/langchain-ai/langgraph "Go to repository")
  * [ Guides  ](https://langchain-ai.github.io/langgraph/)
  * [ Reference  ](https://langchain-ai.github.io/langgraph/reference/)
  * Examples 
    * Agentic RAG  [ Agentic RAG  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
      * [ Setup  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#setup)
      * [ 1. Preprocess documents  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#1-preprocess-documents)
      * [ 2. Create a retriever tool  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#2-create-a-retriever-tool)
      * [ 3. Generate query  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#3-generate-query)
      * [ 4. Grade documents  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#4-grade-documents)
      * [ 5. Rewrite question  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#5-rewrite-question)
      * [ 6. Generate an answer  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#6-generate-an-answer)
      * [ 7. Assemble the graph  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#7-assemble-the-graph)
      * [ 8. Run the agentic RAG  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#8-run-the-agentic-rag)
    * [ Agent Supervisor  ](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)
    * [ SQL agent  ](https://langchain-ai.github.io/langgraph/tutorials/sql-agent/)
    * LangGraph Platform 
      * [ Authentication  ](https://langchain-ai.github.io/langgraph/tutorials/auth/getting_started/)
      * [ Rebuild graph at runtime  ](https://langchain-ai.github.io/langgraph/cloud/deployment/graph_rebuild/)
      * [ How to interact with the deployment using RemoteGraph  ](https://langchain-ai.github.io/langgraph/how-tos/use-remote-graph/)
      * [ How to use LangGraph Platform to deploy CrewAI, AutoGen, and other frameworks  ](https://langchain-ai.github.io/langgraph/how-tos/autogen-langgraph-platform/)
      * [ Front-end and generative UI  ](https://langchain-ai.github.io/langgraph/cloud/how-tos/use_stream_react/)
  * [ Resources  ](https://langchain-ai.github.io/langgraph/concepts/faq/)


  * [ Setup  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#setup)
  * [ 1. Preprocess documents  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#1-preprocess-documents)
  * [ 2. Create a retriever tool  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#2-create-a-retriever-tool)
  * [ 3. Generate query  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#3-generate-query)
  * [ 4. Grade documents  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#4-grade-documents)
  * [ 5. Rewrite question  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#5-rewrite-question)
  * [ 6. Generate an answer  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#6-generate-an-answer)
  * [ 7. Assemble the graph  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#7-assemble-the-graph)
  * [ 8. Run the agentic RAG  ](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#8-run-the-agentic-rag)


[ ](https://github.com/langchain-ai/langgraph/edit/main/docs/docs/tutorials/rag/langgraph_agentic_rag.ipynb "Edit this page")
# Agentic RAG[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#agentic-rag "Permanent link")
In this tutorial we will build a [retrieval agent](https://python.langchain.com/docs/tutorials/qa_chat_history). Retrieval agents are useful when you want an LLM to make a decision about whether to retrieve context from a vectorstore or respond to the user directly.
By the end of the tutorial we will have done the following:
  1. Fetch and preprocess documents that will be used for retrieval.
  2. Index those documents for semantic search and create a retriever tool for the agent.
  3. Build an agentic RAG system that can decide when to use the retriever tool.


![Screenshot 2024-02-14 at 3.43.58 PM.png](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
## Setup[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#setup "Permanent link")
Let's download the required packages and set our API keys:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-0-1)pip"langchain[openai]"
```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-1)importgetpass
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-2)importos
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-3)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-4)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-5)def_set_env(key: str):
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-6)    if key not in os.environ:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-7)        os.environ[key] = getpass.getpass(f"{key}:")
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-8)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-9)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-1-10)_set_env("OPENAI_API_KEY")

```

Set up [LangSmith](https://smith.langchain.com) for LangGraph development
Sign up for LangSmith to quickly spot issues and improve the performance of your LangGraph projects. LangSmith lets you use trace data to debug, test, and monitor your LLM apps built with LangGraph — read more about how to get started [here](https://docs.smith.langchain.com). 
## 1. Preprocess documents[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#1-preprocess-documents "Permanent link")
1. Fetch documents to use in our RAG system. We will use three of the most recent pages from [Lilian Weng's excellent blog](https://lilianweng.github.io/). We'll start by fetching the content of the pages using `WebBaseLoader` utility:
_API Reference:[WebBaseLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.web_base.WebBaseLoader.html)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-1)fromlangchain_community.document_loadersimport WebBaseLoader
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-2)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-3)urls = [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-4)    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-5)    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-6)    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-7)]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-8)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-2-9)docs = [WebBaseLoader(url).load() for url in urls]

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-3-1)docs[0][0].page_content.strip()[:1000]

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-4-1)"Reward Hacking in Reinforcement Learning | Lil'Log\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nLil'Log\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n|\n\n\n\n\n\n\nPosts\n\n\n\n\nArchive\n\n\n\n\nSearch\n\n\n\n\nTags\n\n\n\n\nFAQ\n\n\n\n\n\n\n\n\n\n      Reward Hacking in Reinforcement Learning\n    \nDate: November 28, 2024  |  Estimated Reading Time: 37 min  |  Author: Lilian Weng\n\n\n \n\n\nTable of Contents\n\n\n\nBackground\n\nReward Function in RL\n\nSpurious Correlation\n\n\nLet’s Define Reward Hacking\n\nList of Examples\n\nReward hacking examples in RL tasks\n\nReward hacking examples in LLM tasks\n\nReward hacking examples in real life\n\n\nWhy does Reward Hacking Exist?\n\n\nHacking RL Environment\n\nHacking RLHF of LLMs\n\nHacking the Training Process\n\nHacking the Evaluator\n\nIn-Context Reward Hacking\n\n\nGeneralization of Hacking Skills\n\nPeek into Mitigations\n\nRL Algorithm Improvement\n\nDetecting Reward Hacking\n\nData Analysis of RLHF\n\n\nCitation\n\nReferences\n\n\n\n\n\nReward hacking occurs when a reinforcement learning (RL) agent exploits flaws or ambiguities in the reward function to ac"

```

2. Split the fetched documents into smaller chunks for indexing into our vectorstore:
_API Reference:[RecursiveCharacterTextSplitter](https://python.langchain.com/api_reference/text_splitters/character/langchain_text_splitters.character.RecursiveCharacterTextSplitter.html)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-5-1)fromlangchain_text_splittersimport RecursiveCharacterTextSplitter
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-5-2)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-5-3)docs_list = [item for sublist in docs for item in sublist]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-5-4)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-5-5)text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-5-6)    chunk_size=100, chunk_overlap=50
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-5-7))
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-5-8)doc_splits = text_splitter.split_documents(docs_list)

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-6-1)doc_splits[0].page_content.strip()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-7-1)"Reward Hacking in Reinforcement Learning | Lil'Log\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nLil'Log\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n|\n\n\n\n\n\n\nPosts\n\n\n\n\nArchive\n\n\n\n\nSearch\n\n\n\n\nTags\n\n\n\n\nFAQ"

```

## 2. Create a retriever tool[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#2-create-a-retriever-tool "Permanent link")
Now that we have our split documents, we can index them into a vector store that we'll use for semantic search. 
1. Use an in-memory vector store and OpenAI embeddings:
_API Reference:[InMemoryVectorStore](https://python.langchain.com/api_reference/core/vectorstores/langchain_core.vectorstores.in_memory.InMemoryVectorStore.html) | [OpenAIEmbeddings](https://python.langchain.com/api_reference/openai/embeddings/langchain_openai.embeddings.base.OpenAIEmbeddings.html)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-8-1)fromlangchain_core.vectorstoresimport InMemoryVectorStore
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-8-2)fromlangchain_openaiimport OpenAIEmbeddings
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-8-3)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-8-4)vectorstore = InMemoryVectorStore.from_documents(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-8-5)    documents=doc_splits, embedding=OpenAIEmbeddings()
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-8-6))
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-8-7)retriever = vectorstore.as_retriever()

```

2. Create a retriever tool using LangChain's prebuilt `create_retriever_tool`:
_API Reference:[create_retriever_tool](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.retriever.create_retriever_tool.html)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-9-1)fromlangchain.tools.retrieverimport create_retriever_tool
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-9-2)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-9-3)retriever_tool = create_retriever_tool(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-9-4)    retriever,
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-9-5)    "retrieve_blog_posts",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-9-6)    "Search and return information about Lilian Weng blog posts.",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-9-7))

```

3. Test the tool:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-10-1)retriever_tool.invoke({"query": "types of reward hacking"})

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-11-1)'(Note: Some work defines reward tampering as a distinct category of misalignment behavior from reward hacking. But I consider reward hacking as a broader concept here.)\nAt a high level, reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering.\n\nWhy does Reward Hacking Exist?#\n\nPan et al. (2022) investigated reward hacking as a function of agent capabilities, including (1) model size, (2) action space resolution, (3) observation space noise, and (4) training time. They also proposed a taxonomy of three types of misspecified proxy rewards:\n\nLet’s Define Reward Hacking#\nReward shaping in RL is challenging. Reward hacking occurs when an RL agent exploits flaws or ambiguities in the reward function to obtain high rewards without genuinely learning the intended behaviors or completing the task as designed. In recent years, several related concepts have been proposed, all referring to some form of reward hacking:'

```

## 3. Generate query[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#3-generate-query "Permanent link")
Now we will start building components ([nodes](https://langchain-ai.github.io/langgraph/concepts/low_level#nodes) and [edges](https://langchain-ai.github.io/langgraph/concepts/low_level#edges)) for our agentic RAG graph. Note that the components will operate on the [`MessagesState`](https://langchain-ai.github.io/langgraph/concepts/low_level#messagesstate) — graph state that contains a `messages` key with a list of [chat messages](https://python.langchain.com/docs/concepts/messages/).
1. Build a `generate_query_or_respond` node. It will call an LLM to generate a response based on the current graph state (list of messages). Given the input messages, it will decide to retrieve using the retriever tool, or respond directly to the user. Note that we're giving the chat model access to the `retriever_tool` we created earlier via `.bind_tools`:
_API Reference:[init_chat_model](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-1)fromlanggraph.graphimport MessagesState
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-3)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-4)response_model = init_chat_model("openai:gpt-4.1", temperature=0)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-5)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-6)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-7)defgenerate_query_or_respond(state: MessagesState):
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-8)"""Call the model to generate a response based on the current state. Given
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-9)    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-10)    """
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-11)    response = (
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-12)        response_model
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-13)        .bind_tools([retriever_tool]).invoke(state["messages"])
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-14)    )
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-12-15)    return {"messages": [response]}

```

2. Try it on a random input:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-13-1)input = {"messages": [{"role": "user", "content": "hello!"}]}
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-13-2)generate_query_or_respond(input)["messages"][-1].pretty_print()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-14-1)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-14-2)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-14-3)Hello! How can I help you today?

```

3. Ask a question that requires semantic search:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-1)input = {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-2)    "messages": [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-3)        {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-4)            "role": "user",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-5)            "content": "What does Lilian Weng say about types of reward hacking?",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-6)        }
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-7)    ]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-8)}
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-15-9)generate_query_or_respond(input)["messages"][-1].pretty_print()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-16-1)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-16-2)Tool Calls:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-16-3)  retrieve_blog_posts (call_tYQxgfIlnQUDMdtAhdbXNwIM)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-16-4) Call ID: call_tYQxgfIlnQUDMdtAhdbXNwIM
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-16-5)  Args:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-16-6)    query: types of reward hacking

```

## 4. Grade documents[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#4-grade-documents "Permanent link")
1. Add a [conditional edge](https://langchain-ai.github.io/langgraph/concepts/low_level#conditional-edges) — `grade_documents` — to determine whether the retrieved documents are relevant to the question. We will use a model with a structured output schema `GradeDocuments` for document grading. The `grade_documents` function will return the name of the node to go to based on the grading decision (`generate_answer` or `rewrite_question`):
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-1)frompydanticimport BaseModel, Field
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-2)fromtypingimport Literal
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-3)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-4)GRADE_PROMPT = (
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-5)    "You are a grader assessing relevance of a retrieved document to a user question. \n "
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-6)    "Here is the retrieved document: \n\n{context}\n\n"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-7)    "Here is the user question: {question}\n"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-8)    "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-9)    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-10))
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-11)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-12)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-13)classGradeDocuments(BaseModel):
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-14)"""Grade documents using a binary score for relevance check."""
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-15)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-16)    binary_score: str = Field(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-17)        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-18)    )
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-19)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-20)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-21)grader_model = init_chat_model("openai:gpt-4.1", temperature=0)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-22)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-23)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-24)defgrade_documents(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-25)    state: MessagesState,
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-26)) -> Literal["generate_answer", "rewrite_question"]:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-27)"""Determine whether the retrieved documents are relevant to the question."""
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-28)    question = state["messages"][0].content
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-29)    context = state["messages"][-1].content
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-30)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-31)    prompt = GRADE_PROMPT.format(question=question, context=context)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-32)    response = (
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-33)        grader_model
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-34)        .with_structured_output(GradeDocuments).invoke(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-35)            [{"role": "user", "content": prompt}]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-36)        )
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-37)    )
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-38)    score = response.binary_score
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-39)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-40)    if score == "yes":
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-41)        return "generate_answer"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-42)    else:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-17-43)        return "rewrite_question"

```

2. Run this with irrelevant documents in the tool response:
_API Reference:[convert_to_messages](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.utils.convert_to_messages.html)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-1)fromlangchain_core.messagesimport convert_to_messages
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-2)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-3)input = {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-4)    "messages": convert_to_messages(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-5)        [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-6)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-7)                "role": "user",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-8)                "content": "What does Lilian Weng say about types of reward hacking?",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-9)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-10)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-11)                "role": "assistant",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-12)                "content": "",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-13)                "tool_calls": [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-14)                    {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-15)                        "id": "1",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-16)                        "name": "retrieve_blog_posts",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-17)                        "args": {"query": "types of reward hacking"},
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-18)                    }
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-19)                ],
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-20)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-21)            {"role": "tool", "content": "meow", "tool_call_id": "1"},
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-22)        ]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-23)    )
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-24)}
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-18-25)grade_documents(input)

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-19-1)'rewrite_question'

```

3. Confirm that the relevant documents are classified as such:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-1)input = {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-2)    "messages": convert_to_messages(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-3)        [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-4)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-5)                "role": "user",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-6)                "content": "What does Lilian Weng say about types of reward hacking?",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-7)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-8)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-9)                "role": "assistant",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-10)                "content": "",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-11)                "tool_calls": [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-12)                    {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-13)                        "id": "1",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-14)                        "name": "retrieve_blog_posts",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-15)                        "args": {"query": "types of reward hacking"},
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-16)                    }
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-17)                ],
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-18)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-19)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-20)                "role": "tool",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-21)                "content": "reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-22)                "tool_call_id": "1",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-23)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-24)        ]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-25)    )
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-26)}
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-20-27)grade_documents(input)

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-21-1)'generate_answer'

```

## 5. Rewrite question[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#5-rewrite-question "Permanent link")
1. Build the `rewrite_question` node. The retriever tool can return potentially irrelevant documents, which indicates a need to improve the original user question. To do so, we will call the `rewrite_question` node:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-1)REWRITE_PROMPT = (
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-2)    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-3)    "Here is the initial question:"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-4)    "\n ------- \n"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-5)    "{question}"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-6)    "\n ------- \n"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-7)    "Formulate an improved question:"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-8))
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-9)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-10)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-11)defrewrite_question(state: MessagesState):
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-12)"""Rewrite the original user question."""
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-13)    messages = state["messages"]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-14)    question = messages[0].content
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-15)    prompt = REWRITE_PROMPT.format(question=question)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-16)    response = response_model.invoke([{"role": "user", "content": prompt}])
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-22-17)    return {"messages": [{"role": "user", "content": response.content}]}

```

2. Try it out:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-1)input = {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-2)    "messages": convert_to_messages(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-3)        [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-4)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-5)                "role": "user",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-6)                "content": "What does Lilian Weng say about types of reward hacking?",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-7)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-8)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-9)                "role": "assistant",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-10)                "content": "",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-11)                "tool_calls": [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-12)                    {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-13)                        "id": "1",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-14)                        "name": "retrieve_blog_posts",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-15)                        "args": {"query": "types of reward hacking"},
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-16)                    }
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-17)                ],
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-18)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-19)            {"role": "tool", "content": "meow", "tool_call_id": "1"},
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-20)        ]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-21)    )
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-22)}
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-23)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-24)response = rewrite_question(input)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-23-25)print(response["messages"][-1]["content"])

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-24-1)What are the different types of reward hacking described by Lilian Weng, and how does she explain them?

```

## 6. Generate an answer[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#6-generate-an-answer "Permanent link")
1. Build `generate_answer` node: if we pass the grader checks, we can generate the final answer based on the original question and the retrieved context:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-1)GENERATE_PROMPT = (
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-2)    "You are an assistant for question-answering tasks. "
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-3)    "Use the following pieces of retrieved context to answer the question. "
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-4)    "If you don't know the answer, just say that you don't know. "
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-5)    "Use three sentences maximum and keep the answer concise.\n"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-6)    "Question: {question}\n"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-7)    "Context: {context}"
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-8))
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-9)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-10)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-11)defgenerate_answer(state: MessagesState):
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-12)"""Generate an answer."""
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-13)    question = state["messages"][0].content
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-14)    context = state["messages"][-1].content
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-15)    prompt = GENERATE_PROMPT.format(question=question, context=context)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-16)    response = response_model.invoke([{"role": "user", "content": prompt}])
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-25-17)    return {"messages": [response]}

```

2. Try it:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-1)input = {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-2)    "messages": convert_to_messages(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-3)        [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-4)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-5)                "role": "user",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-6)                "content": "What does Lilian Weng say about types of reward hacking?",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-7)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-8)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-9)                "role": "assistant",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-10)                "content": "",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-11)                "tool_calls": [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-12)                    {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-13)                        "id": "1",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-14)                        "name": "retrieve_blog_posts",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-15)                        "args": {"query": "types of reward hacking"},
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-16)                    }
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-17)                ],
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-18)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-19)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-20)                "role": "tool",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-21)                "content": "reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-22)                "tool_call_id": "1",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-23)            },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-24)        ]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-25)    )
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-26)}
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-27)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-28)response = generate_answer(input)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-26-29)response["messages"][-1].pretty_print()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-27-1)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-27-2)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-27-3)Lilian Weng says that reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering. These categories describe different ways in which an agent might exploit flaws in the reward system. Environment or goal misspecification involves unintended behaviors due to poorly specified objectives, while reward tampering involves directly manipulating the reward signal.

```

## 7. Assemble the graph[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#7-assemble-the-graph "Permanent link")
  * Start with a `generate_query_or_respond` and determine if we need to call `retriever_tool`
  * Route to next step using `tools_condition`:
    * If `generate_query_or_respond` returned `tool_calls`, call `retriever_tool` to retrieve context 
    * Otherwise, respond directly to the user
  * Grade retrieved document content for relevance to the question (`grade_documents`) and route to next step:
    * If not relevant, rewrite the question using `rewrite_question` and then call `generate_query_or_respond` again
    * If relevant, proceed to `generate_answer` and generate final response using the `ToolMessage` with the retrieved document context


_API Reference:[StateGraph](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) | [START](https://langchain-ai.github.io/langgraph/reference/constants/#langgraph.constants.START) | [END](https://langchain-ai.github.io/langgraph/reference/constants/#langgraph.constants.END) | [ToolNode](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.ToolNode) | [tools_condition](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.tools_condition)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-1)fromlanggraph.graphimport StateGraph, START, END
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-2)fromlanggraph.prebuiltimport ToolNode
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-3)fromlanggraph.prebuiltimport tools_condition
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-4)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-5)workflow = StateGraph(MessagesState)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-6)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-7)# Define the nodes we will cycle between
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-8)workflow.add_node(generate_query_or_respond)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-9)workflow.add_node("retrieve", ToolNode([retriever_tool]))
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-10)workflow.add_node(rewrite_question)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-11)workflow.add_node(generate_answer)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-12)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-13)workflow.add_edge(START, "generate_query_or_respond")
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-14)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-15)# Decide whether to retrieve
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-16)workflow.add_conditional_edges(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-17)    "generate_query_or_respond",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-18)    # Assess LLM decision (call `retriever_tool` tool or respond to the user)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-19)    tools_condition,
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-20)    {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-21)        # Translate the condition outputs to nodes in our graph
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-22)        "tools": "retrieve",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-23)        END: END,
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-24)    },
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-25))
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-26)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-27)# Edges taken after the `action` node is called.
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-28)workflow.add_conditional_edges(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-29)    "retrieve",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-30)    # Assess agent decision
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-31)    grade_documents,
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-32))
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-33)workflow.add_edge("generate_answer", END)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-34)workflow.add_edge("rewrite_question", "generate_query_or_respond")
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-35)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-36)# Compile
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-28-37)graph = workflow.compile()

```

Visualize the graph:
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-29-1)fromIPython.displayimport Image, display
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-29-2)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-29-3)display(Image(graph.get_graph().draw_mermaid_png()))

```

![](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)
## 8. Run the agentic RAG[¶](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#8-run-the-agentic-rag "Permanent link")
```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-1)for chunk in graph.stream(
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-2)    {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-3)        "messages": [
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-4)            {
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-5)                "role": "user",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-6)                "content": "What does Lilian Weng say about types of reward hacking?",
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-7)            }
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-8)        ]
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-9)    }
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-10)):
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-11)    for node, update in chunk.items():
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-12)        print("Update from node", node)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-13)        update["messages"][-1].pretty_print()
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-30-14)        print("\n\n")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-1)Update from node generate_query_or_respond
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-2)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-3)Tool Calls:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-4)  retrieve_blog_posts (call_NYu2vq4km9nNNEFqJwefWKu1)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-5) Call ID: call_NYu2vq4km9nNNEFqJwefWKu1
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-6)  Args:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-7)    query: types of reward hacking
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-8)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-9)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-10)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-11)Update from node retrieve
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-12)================================= Tool Message =================================
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-13)Name: retrieve_blog_posts
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-14)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-15)(Note: Some work defines reward tampering as a distinct category of misalignment behavior from reward hacking. But I consider reward hacking as a broader concept here.)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-16)At a high level, reward hacking can be categorized into two types: environment or goal misspecification, and reward tampering.
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-17)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-18)Why does Reward Hacking Exist?#
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-19)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-20)Pan et al. (2022) investigated reward hacking as a function of agent capabilities, including (1) model size, (2) action space resolution, (3) observation space noise, and (4) training time. They also proposed a taxonomy of three types of misspecified proxy rewards:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-21)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-22)Let’s Define Reward Hacking#
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-23)Reward shaping in RL is challenging. Reward hacking occurs when an RL agent exploits flaws or ambiguities in the reward function to obtain high rewards without genuinely learning the intended behaviors or completing the task as designed. In recent years, several related concepts have been proposed, all referring to some form of reward hacking:
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-24)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-25)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-26)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-27)Update from node generate_answer
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-28)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-29)
[](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__codelineno-31-30)Lilian Weng categorizes reward hacking into two types: environment or goal misspecification, and reward tampering. She considers reward hacking as a broad concept that includes both of these categories. Reward hacking occurs when an agent exploits flaws or ambiguities in the reward function to achieve high rewards without performing the intended behaviors.

```

Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! Please help us improve this page by adding to the discussion below. 
[ Previous  Environment variables  ](https://langchain-ai.github.io/langgraph/cloud/reference/env_var/) [ Next  Agent Supervisor  ](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)
Copyright © 2025 LangChain, Inc | [Consent Preferences](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#__consent)
Made with [ Material for MkDocs Insiders ](https://squidfunk.github.io/mkdocs-material/)
[ ](https://langchain-ai.github.io/langgraphjs/ "langchain-ai.github.io") [ ](https://github.com/langchain-ai/langgraph "github.com") [ ](https://twitter.com/LangChainAI "twitter.com")
#### Cookie consent
We use cookies to recognize your repeated visits and preferences, as well as to measure the effectiveness of our documentation and whether users find what they're searching for. **Clicking "Accept" makes our documentation better. Thank you!** ❤️
  *   * 

Accept Reject
