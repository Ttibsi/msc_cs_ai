# Week 6 - Neural Networks

* Define the basic concepts: unsupervised, supervised and reinforcement learning, discrete and continuous data, classification and regression, and overfitting. [MLO 2 & MLO 4]
* Apply basic principles of Neural Networks. [MLO 1]
* Define, train and use multilayer Neural Networks. [MLO 1, MLO 3 & MLO 4]
* Identify methods of current AI research and give examples of their application in state-of-the-art AI systems. [MLO 4]

### Lesson 1 - Machine Learning
Machine learning - no longer based purely on algorithm design
    - machines are also trained using large data sets
    - The aim is for the machine to be able to exceed what it's programmed to do

Common steps:
* train - run training data through the model
* Validate - part of the data should be keps aside for validation purposes
* test - test using "new" data
* deploy - if the model performs well enough, it can be deployed

Type of learning:
* supervised
    - complete and fully labelled data used in training
    - should be able to identify patterns or rules within previously unseen data
* semi-supervised
* unsupervised
    - complete but unlabelled data used
    - often when it's not possible to acquire completely labelled data
    - unsupervised models will reveal segmentation or clustering of data
    - useful for anomaly detection
* reinforcement
    - learns by repeatedly attempting a task
    - each attempt is subtly different from the last
    - better attempts are rewarded, less successful attempts are penalised
    - continues until it reaches an optimal strategy
    - useful for applications such as game playing or robotics automation

The study of agents that learn from their world
ML is a field within AI which enables computers to seek goals independantly using algorithms

Deep learning - may include both supervised and unsupervised techniques

Classification
* one example is K-nearest neighbor
* binary classifcation uses two classes - ex spam and not spam
    * naive Bayes classifier algorithm is an example
* One method = logistic regression
    * outputs the probability of a value belonging to a class

K-means - popular clustering algorithm
    - randomly select elements to be the "centers" of each cluster (centroids)
    - assign each sample to the nearest centroid
    - move the centroids to the center of the samples that were assigned to it
    - loop 2 and 3 until the clusters do not change, a max number of iterations is hit,
    or until point tolerance is reached

Decision trees
    - Build up a tree by associating data splitting on the features of the
    root data that shows the largest information gain
    - iterative process
    - overfitting - too many elements in the tree
        - usually there is a depth limit
    - an algorithm is requires to optimise the data at each split

Linear Regression
    - model the relationship between multiple features and a continuous target data
    - y = w0 + w1x where y is the contiuous value, x is a single "core" value
        and w0 is the weight of the y axi and w1 is the coefficient of x

Reinforcement Learning
* Behavioural learning model
* trained via feedback from data analysis via trial and error
* "Markov's decision processes in systems theory"
* common use cases - robotics, game-playing, self-driving cars

### Lesson 2 - Neural Networks

Neurons in nature
* recieve signals through "dendrites"
* signals are processed in the cell body
* signals pass down the axon electro-chemically
* passed through electrical signals and chemicals
* Connections between neurons are synapses

Perceptron - simulating neurons
- can take inputs that are assigned weights
- calculate the weighted sum of inputs via matrix multiplication
- result gets passed into an "activation" function that decides if the value
is passed on
- A bias value may be added to the weighted sum in a node to increase/decrease
likelyhood of activation

Applications of neural networks
- computer vision
- natural language processing
- AV recognition and processing
- autonomous navigation
- discovery in research
- statistical forecasting

NNs use a function which in classification tasks (ex spam filtering) must have
must have a condition to be triggered, ex if the value is over 1 so that the
state changes between 1 and 0. One example is the sigmoid function:
```
S(x) = 1 / 1+e^-x
```
This returns either 1 or -1 for any real number passed in

```py
import math
def sigmoid(x):
    return 1 / (1 + math.exp(-x))
```

Deep learning - "deep" because the logic is organised into multiple layers
feedforward network - directed acyclic graph with designated Input and output nodes.

Typically inputs are "continuous" between 0 and 1

### Lesson 3 - Applications of Neural Networks 
Expressive Artificial Intelligence -- AI + art
    - Commonly found in gaming

### Discussion - Ethics in AI
As discussed in week 1, there are four ways to classify artificial intelligence 
-- thinking or acting "humanly", or thinking or acting rationally. If we are to 
take creative AI to be just acting humanly, instead of actually thinking, then 
any artwork generated is purely of the "just keep stirring" variety[1] and in 
my opinion is taking away from artists that have honed their craft in the same 
way that we currently see Large Language Models spitting out "AI Slop" code 
compared to the masters of software engineering.

From what I've observed, this comes down to questioning the value of art. If 
the medium is generatlly considered of value by society - for example, cimena 
or video games -- then it appears that there is more push back from society when 
AI is generated. This has come to a head in both industries, such as with the 
backlash toward the AI character of Tilly Norwood in Hollywood[2], or the 
repealing of the Game of the Year award from video game Expedition 33 due to 
it's use of AI generated art.[3]

However, on the other hand, we're seeing more and more static AI-generated 
artwork used across social media, looking at recent trends such as the action 
figure-like mini me's[4], and AI characatures of people's offices[5]. This 
shows that people are happier to both waiver their privacy by sharing personal 
information and use these image generators without any thought about how these 
work without any major backlash.

My personal opinion is that this is something we should move away from, as 
generated artwork will only cause long-term harm to an industry that already 
struggles. After the Covid-19 closed thousands of locations involved in film, 
TV, performing art, and then the SAG-AFTRA and WGA strikes of 2023, there were 
thousands of people throughout the film, video game, VFX, and live art 
industries who lost their jobs, and those industries are still trying to recover 
without the looming threat of AI as some see it as a financial shortcut -- an 
issue that I've observed that our own industrty is wmoving towards as well.
---
references:
[1] “Machine Learning,” xkcd. https://xkcd.com/1838/
[2] Wikipedia Contributors, “Tilly Norwood,” Wikipedia, Oct. 08, 2025.
[f] J. Peckham, “Clair Obscur: Expedition 33 Stripped of a Game of the Year Award Because of AI,” PCMAG, Dec. 22, 2025. https://www.pcmag.com/news/clair-obscur-expedition-33-stripped-of-a-game-of-the-year-award-because (accessed Feb. 18, 2026).
[4] Liv, “ChatGPT AI action dolls: Concerns around the Barbie-like viral social trend,” BBC News, Apr. 11, 2025. Available: https://www.bbc.co.uk/news/articles/c5yg690e9eno
[5] K. O'Flaherty, “The New ChatGPT Caricature Trend Comes With A Privacy Warning,” Forbes, Feb. 09, 2026. Available: https://www.forbes.com/sites/kateoflahertyuk/2026/02/09/the-new-chatgpt-caricature-trend-comes-with-a-privacy-warning/

### Quiz notes
- Linear regression is for discrete values, not continuous
- activation functions introduce non-linearity to the model
- K-means is best for grouping data into clusters
- regression trees are a form of decision tree
