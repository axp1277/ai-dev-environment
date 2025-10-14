“Are you ready for a new brainstorming session?”
00:02
You said:
“Okay, so I want to enhance my AI coding workflow that I use across all my projects. And just to kind of give you some context, I use Cloud Code to do all my AI coding. And I leverage a subdirectory called AI-Docs. And I also leverage another subdirectory called .cloud forward slash commands, which are all the cloud commands that are possible within the – that I can use. And so what I want to do is I want to actually create a workflow. And I have a – there should be a – there is a workflow subdirectory that contains markdown files. So this AI-Docs is literally a subdirectory that contains other subdirectories. And all these subdirectories have markdown files, okay? So the markdown files pretty much provide us with prompts that we can reuse in order to execute some specific workflow in our development plan when we develop code. So far, does everything make sense?”
01:23
You said:
Transcript Unavailable
00:01
You said:
“Please, you want to bring it.”
00:01
You said:
“Smoother and more stream.”
00:01
You said:
“Okay, so I think what I want to do is, the way I want to basically implement this workflow at this point is Cloud Code allows you to spool up these sub-agents, okay? And so, I think what we need is, we need a Cloud Command, okay? We need to create a new Cloud Command that will do, that will basically call two separate Cloud Commands. So, basically, we can create a Cloud Command that calls other Cloud Command files. Does that make sense?”
00:44
You said:
“Yes, so the two commands that I want to change right now, chain right now, are there's one command that basically takes a brainstorming session and converts it into a PRD, and then another command that takes a brainstorming session and converts it into a specification document. Okay, so I already have, I have a brain2specs, and I have a brain2prd, um, cloud commands. I have two cloud commands, one is brain2specs, and one is brain2prd, right? So I think what I need is I need a new command, and I don't know what the best wording for this command would be, but I think plan would be the way to go, like, if I just hit, if I just, um, create a command called plan, right, um, or maybe there's a better word for it, is basically, you know, I need a workflow that will create all of the, um, markdown files that will help me with the implementation of the code. So I'm going to, from this specific workflow, it's going to create a product requirement document and also a, um, specification document with atomic and subatomic tasks. Does that make sense?”
01:25
You said:
“So I guess my question to you is, from a software perspective, do you think that a PRD and a specification file are all we need in order to drive development, or do you think there is any other files that we should be also including?”
00:22
You said:
“Thanks.”
00:00
You said:
“So, I do actually, I kind of like the user story document. Can you explain to me what the difference between a user story document is and a PRD and a spec plan?”
00:11
You said:
“And you had also added another document too, what was that again, the validation document?”
00:08
You said:
“Okay, got it. So, and how would you, if you were to, like, sort these documents from highest level to lowest level, how would you, like, sort them?”
00:10
You said:
“Okay, perfect. So, if we were to create this plan, the master command, ideally I would want to create this plan command that would literally take a brainstorming session and create all these documents in sequence. But I think it would be even more powerful if we did this. So like the first document that we created is the PRD, right? So, for that particular agent, we would just provide the brainstorming session, and from the brainstorming session, we would get a PRD out of it. The next document, I believe, is the user stories, right? So the user stories would get the brainstorming session, but it would also get the PRD document from the previous agent. Then, after that, we have the specification document, right? The specification document would get the original brainstorming session, but it would also get the PRD session and the user story output. Okay? And then, finally, the validation would basically get everything. It would get the session, it would get the PRD, it would get the user story and the specification document. What do you think of this workflow?”
01:22
You said:
“Okay, perfect. So now, let's talk about the plan markdown files, the CloudCommand plan markdown file that will call these subcommands in sequence, right? I wanna be able to get provided two inputs. The first input is the brainstorming session number, and you can reference my other specification commands like brain2specs is a markdown file command that accepts one input. That one input is the session number in the brainstorming folder. So for example, if I say plan space one, it knows that it needs to go and take the brainstorming session number one markdown file and then extract the PRD from it, extract the user stories, extract the specification document, and extract the acceptance criteria document or the validation document, right? But it would be really cool to also be able to provide a second argument, which would be an optional argument. The second argument, if it's not specified, it would basically just create all the documents, right? If the second document, if the second argument, actually, you know what, let's not overcomplicate this. Let's just have one argument for this, which is the session number in the brainstorming conversation, the brainstorming session markdown file.”
01:45
You said:
“Generating the PRT.”
00:01
You said:
“Keep going.”
00:00
You said:
“or use the PLD.”
00:01
You said:
“Okay, so can you just summarize in detail everything we've talked about so far and provide a kind of a plan on how to implement this from start to end?”
00:10
You said:
“Perfect. So I think we are good to go for this specific one. Let's tack on this additional requirement that we want to – it's a little bit different from what we just talked about. It's a new implementation. So this new implementation is we want to be able to – so one of the challenges is sometimes when we stop AI coding and we're in the middle of a project and we have to close out our AI and then come back to it on a later day, we need a command that will kind of understand where it left off and so it can kind of start taking over and being able to resume the work that it left off. So I want to have a command called prime. So what prime does is it will have one input and the input will be – actually, the input will be an optional input. So if there is no input, it will literally just list all the files in the current directory, look for any readme files, and kind of start really – kind of thoroughly understand the current layout of the directories and everything and kind of understand what it's working with. So that's the first step. The second option is if we want to prime and we only want to work with a specific module, we can prime and then we would basically add a forward slash and then the relative path to the module. So then this instructs the AI to kind of understand what that specific module – how that specific module works in order to provide a context to move forward on any future requests by the human. And then finally, the last command would be if there is a forward slash prime and then a number, that means that the AI is instructed to go into the AI docs and look at the AI docs subdirectories and look for the session number in the brainstorming conversation with that specific number. So it kind of gets a sense of, okay, well, this is what the session was about. And then it's going to go to the specs subdirectory, which is 2-specs. And that will tell it what the current specification is for that. And then it's going to go to the PRD subdirectory, right? And there's going to be a PRD2.md if 2 was the session number. And it's going to understand that and then so on. So prime kind of gives the ability for the AI to kind of pick up where it left off on the previous session where it was implementing and iterating through code.”
03:23
You said:
“I think we're ready to hand this off to the AI Planner. So the AI Planner will have its own guideline to create a very detailed specification plan in order to implement this plan from start to end. But I want you to kind of provide it with your own recommendation on how the tasks should be subdivided in order to create these new prompts. So remember, right, we need to have an initial task that kind of surveys the current AI Docs folder and just make sure that, and also the Doc Cloud Commands folder, and to make sure that we have all of the prompts that we need in order to implement this. Okay, so we're looking for a Brain2Specs prompt. We're looking for a Brain2PRD prompt. We don't have a Brain2UserStories prompt or a Brain2Story prompt, and we don't have a Brain2Validation or Acceptance Criteria prompt. So those two, we'll have to actually implement those Cloud Commands, okay, in detail. So to kind of close up this conversation, create a very detailed layout of what you think the spec plan should look like, and then this will then get handed to the AI Planner. The AI Planner will actually take your recommendation and then implement it in more detail, following a very specific guideline.”
01:35
You said:
“Keep going, please.”
00:01
You said:
“Yes, so I like this entire plan, but I just came up with a new command that I think would be super useful. This command is going to be called the graph command, and the graph command will be responsible for taking all of the documents that we've just generated and create two mermaid diagrams. One mermaid diagram is going to be kind of like a general, very concise, very clear workflow chart of trying to basically map out how the app is going to work in a very clear, concise workflow. And then the second diagram is going to be a system architecture diagram. It may be an overkill, but I think it would be interesting to see how these two diagrams are created by leveraging all of the documents that were created, including the brainstorming session.”
01:02
You said:
“So I have an idea. So for the prime command, what we can do is we can actually initiate or ask Cloud Code to spool up a code-based researcher sub-agent. And this code-based researcher sub-agent will have the ability to go into the code to the existing implementation of the code, if there is one, and research what we currently have, and provide kind of a detailed summary and overview of what the current code does. Kind of like an onboarding agent, where it's trying to basically onboard the AI coding assistants to make sure it understands what the current implementation is. The reason why we want to use a sub-agent is because it doesn't pollute the current context of the primary agent. We can just use the sub-agent, which uses its own context, to go and perform the research. Does that make sense?”
01:08
You said:
“Keep going, please.”
00:02
You said:
“This transcript may not be true.”
00:01
You said:
“Yeah, so this is actually, this has to come before invoking the Code Researcher sub-agent. We have to invoke the Agent Architect, okay, which is another sub-agent that actually creates sub-agents. So the Agent Architect is already implemented in my codebase, and the Agent Architect, we have to provide a description of how we want to implement, of how do we create the Code Agent Researcher, like what are the role, what is the role, what are the instructions of this codebase researcher, and then the codebase researcher will be implemented.”
00:44
You said:
“No, no, no. Sorry, sorry. The prime command does not do that. This is just to, basically, in our specification document, when we're creating this entire set of work, prime, like, markdown files and instructions, we're going to need a code reviewer, or a code researcher sub-agent, right? So in order to, we need to just create this code researcher sub-agent once, right? When we develop this entire new workflow. Okay?”
00:33
You said:
Transcript Unavailable
00:00
You said:
“will be defined as part of.”
00:01
You said:
“Yeah, so then I think right now we want to do a final, detailed, recommended implementation plan to hand off to the AI planner because we've kind of added these additional enhancements after we had created that initial plan. So just finalize everything one more time and then we'll hand it off to the AI planner.”
00:27
You said:
Transcript Unavailable
00:01
You said:
Transcript Unavailable
00:02
You said:
“Find the graph command.”
00:01
