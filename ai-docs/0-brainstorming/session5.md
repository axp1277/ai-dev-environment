“Are you ready for a new, uh, brainstorming session?”
00:03
You said:
“All righty, so, do you recall the indicator that we developed in the TradingView PineScript that barked out New York and London Session in terms of boxes like, you know, on the chart?”
00:24
You said:
“So now what I want to do is I want to create a statistical analysis and I'm going to do this using some code that I already have that is capable of generating statistics based on whether, what is the probability of a London high or a London low to get hit at any given time of the day. In the New York session, so I want to start with quantifying what that means.”
00:39
You said:
“And, uh...”
00:01
You said:
“Does that make sense?”
00:01
You said:
“Alright, so, to start, what I want to do is, I want to basically mark out where we are in a New York session, okay? Like, what time of day are we in a New York session? So, for example...”
00:23
You said:
“All right, so, suppose that we have these following time ranges, okay? So, the London session, all right, starts at 1 a.m., okay, and ends at 8 a.m., okay? At 8 a.m., we have the New York session, okay, that starts at 8 a.m., the New York a.m. session, okay? Starts at 8 a.m., and ends at 12 p.m. Then, the New York p.m. session starts at 12 p.m., and ends at 4 p.m., all right? So, now, these sessions start and ends, these are variables, okay? We could set them to anything we want, but I just want to make sure you understand so far.”
00:55
You said:
“so the next step is this now 8 a.m. right it's the end of the London session right so we're gonna know where we close at that London session close we're gonna know in which quadrant we closed okay now let's define what the quadrants are okay we're gonna split up that rectangle into 25 percentiles four tiles okay so the lowest quadrant goes from 0 to 25 percent then we have 25 percent to 50 percent 50 percent to 75 percent then 75 percent to 100 percent okay then all we do is we track where we started in the quadrant so if we started at the for example top 75th percentile quadrant when we open New York we can compute the probability of a New York session sorry the probability of the London high being rated right in the New York session we can also compute the probability of the London low being rated if we start if we open up the New York session at 8 a.m. and the bottom 25 percentile we can still compute the probability of a London low being rated or we can compute the probability of a London high being rated okay so depending on where we start in those quad the reason why I want to split it up into four different quadrants right 25th the first 25th percentile okay 25 to 50 percent 50 percent 75 percent 75 percent to 100 percent depending where we we fall in those quadrants right those probabilities of rating London highs and London lows in New York session change does that make sense”
02:12
You said:
Transcript Unavailable
01:25
You said:
“So we can treat that as a filter, right? These are basically time-based target filters where we're basically saying we're limiting our scope to only look at windows where those targets would be included or hit, right? So this is a time-based target filter. Another filter that we can add as a conditional probability is a bias. We can use VWAP. So, for example, if we are in a, what is the likelihood or what is the probability of hitting a London high during New York session if we are above VWAP? What is the probability if we are below VWAP, okay? So we wanna be able to activate these filters, turn on or off these filters. The VWAP would be anchored at the New York Midnight Open. Make sense?”
01:00
You said:
Transcript Unavailable
00:29
You said:
Transcript Unavailable
00:23
You said:
“And we're going to be using an existing tool. This is a library that I created. It's called the Statistical Frequency Engine. It's a Pinescript library. We're going to import this engine into this new Profiles London Session Profile Study. And we're going to use this London Profile Session Study to compute the statistics. I will be able to reference, once I start to plan in the code, I'll be able to reference another script that references this library. So you will know exactly how to implement from start to end in Pinescript.”
00:36
You said:
“For more information on the ChatGPT, OpenAI, DALL·E, GPT-4, and GPT-5, please visit the ChatGPT website at http://www.chatgpt.com For more information on the ChatGPT, OpenAI, DALL·E, GPT-4, and GPT-5, please visit the ChatGPT website at http://www.chatgpt.com For more information on the ChatGPT, OpenAI, DALL·E, GPT-4, and GPT-5, please visit the ChatGPT website at http://www.chatgpt.com For more information on the ChatGPT, OpenAI, DALL·E, GPT-4, and GPT-5, please visit the ChatGPT website at http://www.chatgpt.com For more information on the ChatGPT, OpenAI, DALL·E, GPT-4, and GPT-5, please visit the ChatGPT website at http://www.chatgpt.com For more information on the ChatGPT, OpenAI, DALL·E, GPT-4, and GPT-5, please visit the ChatGPT website at http://www.chatgpt.com”
03:04
You said:
“So, now that we have the entire plan pretty much completed, let's recreate the very detailed plan from start to end, split it up into tasks that are reasonable. Each task will have its own subatomic tasks that should be separable, and then what we'll do is we'll hand it off to an AI planner. The AI planner will implement our brainstorming into a more formal specification plan using certain guidelines I already provided to the AI planner. Once the specification document is ready to go, the AI planner will hand this off to an AI coder. The AI coder will implement the plan from start to end with my oversight.”
00:44
