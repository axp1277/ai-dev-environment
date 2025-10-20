[ Skip to content ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#customize-state)
**We are growing and hiring for multiple roles for LangChain, LangGraph and LangSmith.[ Join our team!](https://www.langchain.com/careers)**
[ ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg) ![logo](https://langchain-ai.github.io/langgraph/static/wordmark_light.svg) ](https://langchain-ai.github.io/langgraph/ "LangGraph")
LangGraph 
Customize state 
[ ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/?q= "Share")
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
        * [ Add memory  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/)
        * [ Add human-in-the-loop  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/4-human-in-the-loop/)
        * Customize state  [ Customize state  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/)
          * [ 1. Add keys to the state  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#1-add-keys-to-the-state)
          * [ 2. Update the state inside the tool  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#2-update-the-state-inside-the-tool)
          * [ 3. Prompt the chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#3-prompt-the-chatbot)
          * [ 4. Add human assistance  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#4-add-human-assistance)
          * [ 5. Manually update the state  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#5-manually-update-the-state)
          * [ 6. View the new value  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#6-view-the-new-value)
          * [ Next steps  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#next-steps)
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


  * [ 1. Add keys to the state  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#1-add-keys-to-the-state)
  * [ 2. Update the state inside the tool  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#2-update-the-state-inside-the-tool)
  * [ 3. Prompt the chatbot  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#3-prompt-the-chatbot)
  * [ 4. Add human assistance  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#4-add-human-assistance)
  * [ 5. Manually update the state  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#5-manually-update-the-state)
  * [ 6. View the new value  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#6-view-the-new-value)
  * [ Next steps  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#next-steps)


  1. [ Guides  ](https://langchain-ai.github.io/langgraph/)
  2. [ Get started  ](https://langchain-ai.github.io/langgraph/agents/agents/)
  3. [ LangGraph basics  ](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/)

[ ](https://github.com/langchain-ai/langgraph/edit/main/docs/docs/tutorials/get-started/5-customize-state.md "Edit this page")
# Customize state[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#customize-state "Permanent link")
In this tutorial, you will add additional fields to the state to define complex behavior without relying on the message list. The chatbot will use its search tool to find specific information and forward them to a human for review.
Note
This tutorial builds on [Add human-in-the-loop controls](https://langchain-ai.github.io/langgraph/tutorials/get-started/4-human-in-the-loop/).
## 1. Add keys to the state[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#1-add-keys-to-the-state "Permanent link")
Update the chatbot to research the birthday of an entity by adding `name` and `birthday` keys to the state:
_API Reference:[add_messages](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.message.add_messages)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-1)fromtypingimport Annotated
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-3)fromtyping_extensionsimport TypedDict
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-4)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-5)fromlanggraph.graph.messageimport add_messages
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-8)classState(TypedDict):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-9)    messages: Annotated[list, add_messages]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-10)    name: str
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-0-11)    birthday: str

```

Adding this information to the state makes it easily accessible by other graph nodes (like a downstream node that stores or processes the information), as well as the graph's persistence layer.
## 2. Update the state inside the tool[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#2-update-the-state-inside-the-tool "Permanent link")
Now, populate the state keys inside of the `human_assistance` tool. This allows a human to review the information before it is stored in the state. Use [`Command`](https://langchain-ai.github.io/langgraph/concepts/low_level/#using-inside-tools) to issue a state update from inside the tool.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-1)fromlangchain_core.messagesimport ToolMessage
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-2)fromlangchain_core.toolsimport InjectedToolCallId, tool
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-4)fromlanggraph.typesimport Command, interrupt
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-6)@tool
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-7)# Note that because we are generating a ToolMessage for a state update, we
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-8)# generally require the ID of the corresponding tool call. We can use
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-9)# LangChain's InjectedToolCallId to signal that this argument should not
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-10)# be revealed to the model in the tool's schema.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-11)defhuman_assistance(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-12)    name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-13)) -> str:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-14)"""Request assistance from a human."""
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-15)    human_response = interrupt(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-16)        {
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-17)            "question": "Is this correct?",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-18)            "name": name,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-19)            "birthday": birthday,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-20)        },
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-21)    )
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-22)    # If the information is correct, update the state as-is.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-23)    if human_response.get("correct", "").lower().startswith("y"):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-24)        verified_name = name
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-25)        verified_birthday = birthday
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-26)        response = "Correct"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-27)    # Otherwise, receive information from the human reviewer.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-28)    else:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-29)        verified_name = human_response.get("name", name)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-30)        verified_birthday = human_response.get("birthday", birthday)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-31)        response = f"Made a correction: {human_response}"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-32)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-33)    # This time we explicitly update the state with a ToolMessage inside
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-34)    # the tool.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-35)    state_update = {
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-36)        "name": verified_name,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-37)        "birthday": verified_birthday,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-38)        "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-39)    }
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-40)    # We return a Command object in the tool to update our state.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-1-41)    return Command(update=state_update)

```

The rest of the graph stays the same.
## 3. Prompt the chatbot[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#3-prompt-the-chatbot "Permanent link")
Prompt the chatbot to look up the "birthday" of the LangGraph library and direct the chatbot to reach out to the `human_assistance` tool once it has the required information. By setting `name` and `birthday` in the arguments for the tool, you force the chatbot to generate proposals for these fields.
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-1)user_input = (
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-2)    "Can you look up when LangGraph was released? "
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-3)    "When you have the answer, use the human_assistance tool for review."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-4))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-5)config = {"configurable": {"thread_id": "1"}}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-7)events = graph.stream(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-8)    {"messages": [{"role": "user", "content": user_input}]},
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-9)    config,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-10)    stream_mode="values",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-11))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-12)for event in events:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-13)    if "messages" in event:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-2-14)        event["messages"][-1].pretty_print()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-1)================================ Human Message =================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-3)Can you look up when LangGraph was released? When you have the answer, use the human_assistance tool for review.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-4)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-6)[{'text': "Certainly! I'll start by searching for information about LangGraph's release date using the Tavily search function. Then, I'll use the human_assistance tool for review.", 'type': 'text'}, {'id': 'toolu_01JoXQPgTVJXiuma8xMVwqAi', 'input': {'query': 'LangGraph release date'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-7)Tool Calls:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-8)  tavily_search_results_json (toolu_01JoXQPgTVJXiuma8xMVwqAi)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-9) Call ID: toolu_01JoXQPgTVJXiuma8xMVwqAi
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-10)  Args:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-11)    query: LangGraph release date
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-12)================================= Tool Message =================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-13)Name: tavily_search_results_json
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-14)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-15)[{"url": "https://blog.langchain.dev/langgraph-cloud/", "content": "We also have a new stable release of LangGraph. By LangChain 6 min read Jun 27, 2024 (Oct '24) Edit: Since the launch of LangGraph Cloud, we now have multiple deployment options alongside LangGraph Studio - which now fall under LangGraph Platform. LangGraph Cloud is synonymous with our Cloud SaaS deployment option."}, {"url": "https://changelog.langchain.com/announcements/langgraph-cloud-deploy-at-scale-monitor-carefully-iterate-boldly", "content": "LangChain - Changelog | ☁ 🚀 LangGraph Cloud: Deploy at scale, monitor LangChain LangSmith LangGraph LangChain LangSmith LangGraph LangChain LangSmith LangGraph LangChain Changelog Sign up for our newsletter to stay up to date DATE: The LangChain Team LangGraph LangGraph Cloud ☁ 🚀 LangGraph Cloud: Deploy at scale, monitor carefully, iterate boldly DATE: June 27, 2024 AUTHOR: The LangChain Team LangGraph Cloud is now in closed beta, offering scalable, fault-tolerant deployment for LangGraph agents. LangGraph Cloud also includes a new playground-like studio for debugging agent failure modes and quick iteration: Join the waitlist today for LangGraph Cloud. And to learn more, read our blog post announcement or check out our docs. Subscribe By clicking subscribe, you accept our privacy policy and terms and conditions."}]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-16)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-17)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-18)[{'text': "Based on the search results, it appears that LangGraph was already in existence before June 27, 2024, when LangGraph Cloud was announced. However, the search results don't provide a specific release date for the original LangGraph. \n\nGiven this information, I'll use the human_assistance tool to review and potentially provide more accurate information about LangGraph's initial release date.", 'type': 'text'}, {'id': 'toolu_01JDQAV7nPqMkHHhNs3j3XoN', 'input': {'name': 'Assistant', 'birthday': '2023-01-01'}, 'name': 'human_assistance', 'type': 'tool_use'}]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-19)Tool Calls:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-20)  human_assistance (toolu_01JDQAV7nPqMkHHhNs3j3XoN)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-21) Call ID: toolu_01JDQAV7nPqMkHHhNs3j3XoN
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-22)  Args:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-23)    name: Assistant
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-3-24)    birthday: 2023-01-01

```

We've hit the `interrupt` in the `human_assistance` tool again.
## 4. Add human assistance[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#4-add-human-assistance "Permanent link")
The chatbot failed to identify the correct date, so supply it with information:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-1)human_command = Command(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-2)    resume={
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-3)        "name": "LangGraph",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-4)        "birthday": "Jan 17, 2024",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-5)    },
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-6))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-8)events = graph.stream(human_command, config, stream_mode="values")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-9)for event in events:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-10)    if "messages" in event:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-4-11)        event["messages"][-1].pretty_print()

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-1)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-3)[{'text': "Based on the search results, it appears that LangGraph was already in existence before June 27, 2024, when LangGraph Cloud was announced. However, the search results don't provide a specific release date for the original LangGraph. \n\nGiven this information, I'll use the human_assistance tool to review and potentially provide more accurate information about LangGraph's initial release date.", 'type': 'text'}, {'id': 'toolu_01JDQAV7nPqMkHHhNs3j3XoN', 'input': {'name': 'Assistant', 'birthday': '2023-01-01'}, 'name': 'human_assistance', 'type': 'tool_use'}]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-4)Tool Calls:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-5)  human_assistance (toolu_01JDQAV7nPqMkHHhNs3j3XoN)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-6) Call ID: toolu_01JDQAV7nPqMkHHhNs3j3XoN
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-7)  Args:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-8)    name: Assistant
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-9)    birthday: 2023-01-01
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-10)================================= Tool Message =================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-11)Name: human_assistance
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-12)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-13)Made a correction: {'name': 'LangGraph', 'birthday': 'Jan 17, 2024'}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-14)================================== Ai Message ==================================
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-15)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-16)Thank you for the human assistance. I can now provide you with the correct information about LangGraph's release date.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-17)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-18)LangGraph was initially released on January 17, 2024. This information comes from the human assistance correction, which is more accurate than the search results I initially found.
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-19)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-20)To summarize:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-21)1. LangGraph's original release date: January 17, 2024
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-22)2. LangGraph Cloud announcement: June 27, 2024
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-23)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-5-24)It's worth noting that LangGraph had been in development and use for some time before the LangGraph Cloud announcement, but the official initial release of LangGraph itself was on January 17, 2024.

```

Note that these fields are now reflected in the state:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-6-1)snapshot = graph.get_state(config)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-6-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-6-3){k: v for k, v in snapshot.values.items() if k in ("name", "birthday")}

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-7-1){'name': 'LangGraph', 'birthday': 'Jan 17, 2024'}

```

This makes them easily accessible to downstream nodes (e.g., a node that further processes or stores the information).
## 5. Manually update the state[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#5-manually-update-the-state "Permanent link")
LangGraph gives a high degree of control over the application state. For instance, at any point (including when interrupted), you can manually override a key using `graph.update_state`:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-8-1)graph.update_state(config, {"name": "LangGraph (library)"})

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-9-1){'configurable': {'thread_id': '1',
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-9-2)  'checkpoint_ns': '',
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-9-3)  'checkpoint_id': '1efd4ec5-cf69-6352-8006-9278f1730162'}}

```

## 6. View the new value[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#6-view-the-new-value "Permanent link")
If you call `graph.get_state`, you can see the new value is reflected:
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-10-1)snapshot = graph.get_state(config)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-10-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-10-3){k: v for k, v in snapshot.values.items() if k in ("name", "birthday")}

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-11-1){'name': 'LangGraph (library)', 'birthday': 'Jan 17, 2024'}

```

Manual state updates will [generate a trace](https://smith.langchain.com/public/7ebb7827-378d-49fe-9f6c-5df0e90086c8/r) in LangSmith. If desired, they can also be used to [control human-in-the-loop workflows](https://langchain-ai.github.io/langgraph/tutorials/how-tos/human_in_the_loop/edit-graph-state.md). Use of the `interrupt` function is generally recommended instead, as it allows data to be transmitted in a human-in-the-loop interaction independently of state updates.
**Congratulations!** You've added custom keys to the state to facilitate a more complex workflow, and learned how to generate state updates from inside tools.
Check out the code snippet below to review the graph from this tutorial:
[OpenAI](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__tabbed_1_1)[Anthropic](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__tabbed_1_2)[Azure](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__tabbed_1_3)[Google Gemini](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__tabbed_1_4)[AWS Bedrock](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__tabbed_1_5)
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-12-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-13-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-13-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-13-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-13-4)os.environ["OPENAI_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-13-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-13-6)llm = init_chat_model("openai:gpt-4.1")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-14-1)pip install -U "langchain[anthropic]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-15-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-15-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-15-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-15-4)os.environ["ANTHROPIC_API_KEY"] = "sk-..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-15-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-15-6)llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-16-1)pip install -U "langchain[openai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-4)os.environ["AZURE_OPENAI_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-5)os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-6)os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-8)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-9)    "azure_openai:gpt-4.1",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-10)    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-17-11))

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-18-1)pip install -U "langchain[google-genai]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-19-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-19-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-19-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-19-4)os.environ["GOOGLE_API_KEY"] = "..."
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-19-5)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-19-6)llm = init_chat_model("google_genai:gemini-2.0-flash")

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-20-1)pip install -U "langchain[aws]"

```

```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-1)importos
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-2)fromlangchain.chat_modelsimport init_chat_model
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-3)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-4)# Follow the steps here to configure your credentials:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-5)# https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-6)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-7)llm = init_chat_model(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-8)    "anthropic.claude-3-5-sonnet-20240620-v1:0",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-9)    model_provider="bedrock_converse",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-21-10))

```

_API Reference:[TavilySearch](https://python.langchain.com/api_reference/tavily/tavily_search/langchain_tavily.tavily_search.TavilySearch.html) | [ToolMessage](https://python.langchain.com/api_reference/core/messages/langchain_core.messages.tool.ToolMessage.html) | [InjectedToolCallId](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.base.InjectedToolCallId.html) | [tool](https://python.langchain.com/api_reference/core/tools/langchain_core.tools.convert.tool.html) | [MemorySaver](https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.memory.MemorySaver) | [StateGraph](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph) | [START](https://langchain-ai.github.io/langgraph/reference/constants/#langgraph.constants.START) | [END](https://langchain-ai.github.io/langgraph/reference/constants/#langgraph.constants.END) | [add_messages](https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.message.add_messages) | [ToolNode](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.ToolNode) | [tools_condition](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.tools_condition) | [Command](https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Command) | [interrupt](https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt)_
```
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-1)fromtypingimport Annotated
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-3)fromlangchain_tavilyimport TavilySearch
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-4)fromlangchain_core.messagesimport ToolMessage
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-5)fromlangchain_core.toolsimport InjectedToolCallId, tool
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-6)fromtyping_extensionsimport TypedDict
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-7)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-8)fromlanggraph.checkpoint.memoryimport MemorySaver
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-9)fromlanggraph.graphimport StateGraph, START, END
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-10)fromlanggraph.graph.messageimport add_messages
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-11)fromlanggraph.prebuiltimport ToolNode, tools_condition
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-12)fromlanggraph.typesimport Command, interrupt
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-13)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-14)classState(TypedDict):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-15)    messages: Annotated[list, add_messages]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-16)    name: str
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-17)    birthday: str
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-18)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-19)@tool
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-20)defhuman_assistance(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-21)    name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-22)) -> str:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-23)"""Request assistance from a human."""
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-24)    human_response = interrupt(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-25)        {
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-26)            "question": "Is this correct?",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-27)            "name": name,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-28)            "birthday": birthday,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-29)        },
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-30)    )
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-31)    if human_response.get("correct", "").lower().startswith("y"):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-32)        verified_name = name
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-33)        verified_birthday = birthday
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-34)        response = "Correct"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-35)    else:
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-36)        verified_name = human_response.get("name", name)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-37)        verified_birthday = human_response.get("birthday", birthday)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-38)        response = f"Made a correction: {human_response}"
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-39)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-40)    state_update = {
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-41)        "name": verified_name,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-42)        "birthday": verified_birthday,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-43)        "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-44)    }
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-45)    return Command(update=state_update)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-46)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-47)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-48)tool = TavilySearch(max_results=2)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-49)tools = [tool, human_assistance]
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-50)llm_with_tools = llm.bind_tools(tools)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-51)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-52)defchatbot(state: State):
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-53)    message = llm_with_tools.invoke(state["messages"])
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-54)    assert(len(message.tool_calls) <= 1)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-55)    return {"messages": [message]}
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-56)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-57)graph_builder = StateGraph(State)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-58)graph_builder.add_node("chatbot", chatbot)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-59)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-60)tool_node = ToolNode(tools=tools)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-61)graph_builder.add_node("tools", tool_node)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-62)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-63)graph_builder.add_conditional_edges(
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-64)    "chatbot",
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-65)    tools_condition,
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-66))
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-67)graph_builder.add_edge("tools", "chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-68)graph_builder.add_edge(START, "chatbot")
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-69)
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-70)memory = MemorySaver()
[](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__codelineno-23-71)graph = graph_builder.compile(checkpointer=memory)

```

## Next steps[¶](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#next-steps "Permanent link")
There's one more concept to review before finishing the LangGraph basics tutorials: connecting `checkpointing` and `state updates` to [time travel](https://langchain-ai.github.io/langgraph/tutorials/get-started/6-time-travel/). 
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! Please help us improve this page by adding to the discussion below. 
[ Previous  Add human-in-the-loop  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/4-human-in-the-loop/) [ Next  Time travel  ](https://langchain-ai.github.io/langgraph/tutorials/get-started/6-time-travel/)
Copyright © 2025 LangChain, Inc | [Consent Preferences](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/#__consent)
Made with [ Material for MkDocs Insiders ](https://squidfunk.github.io/mkdocs-material/)
[ ](https://langchain-ai.github.io/langgraphjs/ "langchain-ai.github.io") [ ](https://github.com/langchain-ai/langgraph "github.com") [ ](https://twitter.com/LangChainAI "twitter.com")
#### Cookie consent
We use cookies to recognize your repeated visits and preferences, as well as to measure the effectiveness of our documentation and whether users find what they're searching for. **Clicking "Accept" makes our documentation better. Thank you!** ❤️
  *   * 

Accept Reject
