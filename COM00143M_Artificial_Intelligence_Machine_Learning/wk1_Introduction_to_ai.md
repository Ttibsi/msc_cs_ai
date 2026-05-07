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

