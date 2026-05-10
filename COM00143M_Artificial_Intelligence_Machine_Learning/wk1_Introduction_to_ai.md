# Week 1 - Introduction to AI - Goals, Methods, Controversies

* Explain the goals and purpose of artificial intelligence, and distinctions between approaches such as acting rationally and simulating human behaviour
* Articulate the distinctions between and purpose of AI Search, Logic and Machine Learning
* Identify some of the methods of current AI research and be able to give examples of their application in state-of-the-art AI systems
* Critically evaluate ethical and legal issues that may arise from recent developments in AI.

### Lesson 1 - What is AI

Four broad definitions of AI
* Thinking humanly - AI algorithms should be as close as possible to human thought processs
    - Introspection, psycological experiments, brain imaging
* Thinking rationally - AI algorithms should model and ideal standard of human thought
    - "laws of thought" approach
    - Building on the concepts of logic and probability
* Acting humanly - AI systems should act in a way that is as similar to humans as possible
    - This is the Turing Test
    - Most researchers don't chase this
* Acting rationally - AI systems should make the best possible actions, compared to an ideal standard
    - Rationality is well defined.
    - This approach has been the primary focus of the field's history - rational agents
 
AI capabilities needed for the turing test
* natural language processing
* knowledge representation
* automated reasoning
* machine learning

Interaction with the real world will also require:
* computer vision
* robotics

### Lesson 2 - State of the Art in AI
1956 - Logic Theorist wrote a proof for a theorem shorter than the one in the a known paper
    - a paper on this subject was rejected
General Problem Solver - the first program to use the "thinking humanly" approach
1958 - lisp language created, dominant AI programming language for the late 1900s

dangers of AI:
* Lethal autonomous weapons
* surveillance and persuasion
* biased decision making
* impact on employment
* safety-critical applications - and the fatal injuries that may come with it 
* cybersecurity

Competitions in AI
* SAT Competition
    - Multiple tracks
    - Goal is to solve the boolean satisfiability problem fastewr than others
* robocup
    - robots learning to play football against each other
    - been running since 1997, over 40 teams take part
    - different leagues for different shaped robots, including humanoid and roomba-like

### Lesson 3 - Intro to AI Search
AI search is a powerful technique for solving problems when we need a sequence of actions to
achieve a goal. Key concepts include: states, actions, goals.

Search problem examples:
* rubiks cube
* robot that delivers packages

Given a current state, the valid actions to take are a finite set (mathematical set)
ex `ACTIONS(Liverpool) = {ToManchester, ToBirmingham, ToCardff}`
in the problem of getting from london to liverpool

In short, this is some form of search problem, such as Breath-First search

Agent - anything that cn be viewed as percieving its environment through sensors and acting
upon that environment through actuators
Percept - any content the agent's sensors are perceiving

### Lesson 4 - Introduction to Logic
Logic in AI:
- used to find errors
- used for scheduling
- used for designing scientific experiments

AI can derive new knowledge from an existing body of knowledge using inferrence algorithms
These AI agents rely on their Knowledge Base (KB)
    - a set of sentences that contains everything they know)
    - expressed in a "knowledge representation language"

TELL - an instruction to add a new sentence to the knowledge base
ASK - an instruction to query what is known

A knowledge base agent goes through three steps
    - TELL the kb what it percieves
    - ASK what action should be performed
    - the agent TELLs which action was chosen
This is the whole agent algorithm

### Lesson 5 - Introduction to Machine Learning
Machine learning is one of the most important areas within AI
- Unsupervised learning - AI is given examples, has to learn patterns (ex clustering)
- supervised learning - given examples along with the desired output
- reinforcement learning - AI takes action and learns from the results

An agent is learning if it improves it's performance after making observations of the real world

When an output is a finite set of values (ex sunny/cloudy/rainy), it's a classification problem
If the output is a number, it's called regression

Underfitting - when a hypothesis fails to find a pattern in the data. This usually means there 
isn't enough data to train the model on

Overfitting - when a model pays too much attention to the particular data it was trained on and 
can't handle unseen data correctly

### Lesson 6 - Contemporary AI

