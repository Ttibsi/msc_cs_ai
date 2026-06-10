# Week 6 - Machine Learning with Clustering

* Identify supervised, unsupervised and reinforcement learning and explain the form of their input data set or feedback
* Apply k-means clustering to perform unsupervised learning on an unlabelled data set
* Identify pitfalls of supervised learning, and apply suitable basic techniques to avoid those pitfalls.

### Week 1 - Supervised, Unsupervised, and Reinforcement Learning
Supervised learning - where the system is given examples along with the desired output for each
                        example
Unsupervised Learning - Where the AI system is given examples and has to learn patterns among them
Reinforcement Learning - Where the AI system takes actions and learns from the good or bad
                        outcomes of those actions
Factored Representation - Meaning that each example provided to the machine learning algorithm
                            is represented as a sequence of attribute/feature values


Most common form of unsupervised learning is "Clustering"

During training, a supervised learning algorithm will come up with a hypothesis about the rules of
the data it's been provided, however a good hypothesis will take multiple values from the training
data into considerations. This is something the programmer has very little control over.

### Lesson 2 - Clustering with K-Means
The most common form of unsupervised learning is clustering, detecting groups of similar examples
within a dataset.

Clustering divides a dataset into clusters where the examples in each grouping are similar 
according to some measure

A simple approach, can be too crude for some datasets

* Specify how many clusters you're trying to create (`k`)
* select K points at random as "cluster centers"
    * All instances are assigned to their closest cluster center according to the Euclidian 
    distance 
* The mean/"centroid" of the instances is calculated. This is the new center value for each
cluster
* repeat above, iterating until the same results are achieved in multiple iterations
    * At this point, the centers have stabilised and will remain the same

A bad initial choice of cluster centers can cause the algorithm to find poor/bad clusters

Finding a good value for K
* plot total distance of each sample to a selected cluster center as if k=1
* Repeat for k to a defined upper bound (ex k=5) and find the "elbow point"
* You want to find the average total distance across all nodes to see

I think what's going on here is that the whole algorithm is being run for k=1 to 5 and you just 
compare the final total distances to all the centers to see which value of K brings the nodes
closest.

### Lesson 3 - Principles and Pitfalls of Supervised Learning
hypothesis - a potential solution drawn from the "hypothesis space", such as the set of javascript
            functions or the set of 3-SAT boolean logic formula
            - represented as the function `h()` which is an approximation of the true function `f()`

Test Set - the input data that is used to test if the model will return the expected output value
Underfitting - the hypothesis can't find a pattern in the data
Variance - the amount of change in the hypothesis due to fluctuations in the training data.
         - Bigger/more variance is worse
Overfitting - The model pays too much attention to the data it was trained on and can't evaluate
                unseen data during testing

Hypothesis space - the space of hypotheses that a supervised learning method selects from. It could
                    be the polynomial functions in one variable
