1- A medical tech startup has developed what they call a "Diagnostic Assistant" that uses generative AI to analyse patient symptoms and medical history to suggest/predict potential rare diseases that a patient could be diagnosed with in the near future. This is intended to help provide early interventions. To improve the tool, the startup has been feeding the AI anonymised patient records from several private clinics. While the records are anonymised, they include specific combinations of rare symptoms, age, and broad location data. The company’s terms of service state that “collected data is used for service improvement”, but do not specify that patient data is used to train a generative model that could potentially output similar case details to other users.
Discuss one potential ethical issue and one potential legal issue that may arise from this scenario; in each case, discuss at least one viable, real-world example to illustrate the issue.
Suggested word count: 200 to 250 words. There is no requirement to use references.

2 - Considering the legal and ethical issues you discussed in response to Question 1, suggest one potential solution for each, providing a clear and rational justification for your proposed solutions.
Suggested word count: 200 to 250 words. There is no requirement to use references.

3 - Scenario:
A financial technology (fintech) firm uses an AI model to generate personalised financial advice and investment strategies. This model was trained on thousands of proprietary financial reports and leaked internal documents from various global banks.
What primary legal issue(s) could arise? Why is this a problem for the firm, and what solution(s) could prevent this in the future?
Suggested word count: 100 to 150 words. There is no requirement to use references.

4 - An AI-driven hiring tool consistently ranks candidates from a specific postal code lower than others, despite those candidates having identical qualifications to higher-ranked applicants. Which of the following represents the most likely problem and solution?

5 - Consider the statement: "If the sensor detects smoke (s), then the alarm must sound (a)."
Which of the following are correct? Select all that apply.
(1 mark for each correct answer, -1 for each incorrect answer; to a minimum of 0 mark).

6 - Consider the following statement:
"A smartphone is a communication device that has a touchscreen, but not all communication devices with touchscreens are smartphones."
Task:

    Present the statement in the form of a Horn clause (or clauses).
    Briefly explain what a Horn clause is in the context of propositional logic.
    Identify the premises, conclusions, and logical operations (conjunctions/disjunctions).

You can copy and paste any logic symbols needed from here: ∧, ∨, ¬, ⇒, ⇔, ⊢, ⊨

7 - Given the following statements describing the operation of a smart home system:

    A light turns on if motion is detected and it is sunset.
    A light turns on if motion is detected, but the battery is not low.
    A light is off (not on) if it is not sunset and no motion is detected.
    If the battery is low, the light does not turn on even if motion is detected.

With the following variables:

    L: Light is on
    M: Motion is detected
    S: It is sunset
    B: Battery is low

Present propositional logic statements in conjunctive normal form for each of the four statements above (one per line).

8 - The following specifications have been provided for the design of a logic system for an automated irrigation controller:

    If the soil moisture is low and it is not raining, turn on the water.
    If the user manually overrides, turn on the water regardless of moisture.
    If the water is on, send a log to the cloud.
    If the tank is empty, do not turn on the water and send an alert.

Task: Define and present the minimal set of propositional logic variables (using only positive states) needed to represent these conditions.

(1 mark for each correct variable, -1 for each incorrect variable; to a minimum of 0 mark)

9 - Which of the following statements represents a key difference between Depth First Search (DFS) and Depth-limited Search (DLS)?

// NOTE: for Qs 10-12, a graph was provided with the following heuristic table:
Town h(n)
A 3
B 2
C 5
D 4
E 7
F 3
G 4
H 2
I 5
J 0
10 - With a starting point at A and a goal state of J, carry out a Breadth First Search and present your result as a single string of capital letters (without spaces or commas), comprised of the nodes visited during the search process (i.e. ‘ABCDEFGHIJ’). Where a set of nodes can be visited in any order, visit them in alphabetical order in your answer. Do not show any additional working out.
11 - With a starting point at A and a goal state of J, presenting only those paths which lead to the goal state without backtracking and without revisiting nodes, carry out a Depth First Search and present each result as a single string of capital letters  (without spaces or commas), comprised of the nodes visited during the search process (i.e. ‘ABCDEFGHIJ’). You should present a pair of results; one for a search path through node B and the other for a search path through node C. Do not show any additional working out.
12 - Determine the optimal route from town A to town J by applying the graph version of A* Search to solve this problem. One step of the algorithm consists of identifying the frontier, then selecting one node from this to move to. The start node is A. Show the first five steps you take, specifying the frontier (open list, i.e. show only nodes that have not yet been explored/expanded) as a series of states listed in alphabetical order, followed by the node that is selected at each step. Each node in the frontier must be followed by its f(n) value in parentheses. For example, your frontier might be ‘[D(15), G(18)]’ and the selected node, D, and you must write the step in an appropriate format, such as  “Step n: [D(15), G(18)], D” with each step on a separate line. The first step is the one with only the start node in the frontier, that is [A(0)], A. Do not show any additional workings.


13- You are using a decision tree for classification. The tree is growing very deep and performs perfectly on training data but poorly on new data. What is the most likely problem and corresponding potential solution?

14 - Which of the following are common practices to prevent overfitting?

15 - A retail company wants to group its customers into segments based on purchasing behaviour to design better marketing campaigns.
Present an argument for using supervised or unsupervised learning. State what is needed for each, which is more suitable for the task and why.
Suggested word count: 200 to 250 words. There is no requirement to use references.

16 - For each of the following scenarios, state the most suitable approach, whether Supervised, Unsupervised, or Reinforcement. Justify your answer in one short sentence for each scenario.
    A drone learning to balance and fly in gusty winds via trial and error.
    Categorising a library of 1 million untagged photos into potential classes such as "landscapes" or "portraits."
    Predicting house prices based on historical sales data of similar homes.
    A recommendation engine finding hidden similarities between users who have not bought the same items.
    Detecting fraudulent credit card transactions based on a dataset of known "fraud" and "legitimate" cases.


17 - Suppose you have a neural network with 3 nodes in the input layer, one hidden layer with 5 nodes, and an output layer with 2 nodes. How many trainable parameters (weights and biases) are in this network?

18 - Which of the following statements are true about neural networks?
    An epoch is one full pass of the training dataset through the network.
    Softmax is often used in the output layer for multi-class classification.
    Neural networks can only process numerical data and cannot handle images.
    Weights in a neural network are usually initialised to zero.
    Gradient Descent is used to update weights to minimise the loss function.
    Hidden layers are called "hidden" because they are encrypted for security.
    A bias term allows the activation function to be shifted.

19 - While building a CNN for a basic digit recognition task, you are trying out different sizes for the convolution filter for a 20x20 input dimension. First, you tried a 3x3 convolution filter with a stride of 1 and no padding, then you tried the same filter size with no padding, but with a stride of 2. Present the formula for calculating the output dimensions from these filters, then calculate the output dimensions for the two convolution filters using the formula you have presented. You must show your calculations.

20 - A city council decides to use a deep neural network to predict which infrastructure (roads, bridges, etc.) will need repair next based on sensor data and historical maintenance logs. Present a critical analysis of two essential needs for this development, two potential problems and two suggested solutions with relevant justification.
