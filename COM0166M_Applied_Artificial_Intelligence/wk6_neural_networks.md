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
