# Week 7 - Deep Learning

* Explain what deep learning is, why there's a need for it, and why this field has seen a resurgence. [MLO 1, 2, 3 & 4]
* Articulate the basic concepts of a Convolutional Neural Network (CNN) and some of its use cases, such as object detection and computer vision (facial recognition, etc). [MLO 4]
* Define the concept of Generative Artificial Intelligence and its applications. [MLO4]
* Identify and critically evaluate the potential threats to society posed by recent developments in AI. [MLO 4]

### Lesson 1 - Intro to Deep Learning
* The basis of many recent intelligent applications
    - virtual assistants
    - cancer diagnosis
    - natural language processing
* A subset of ML, which is a subset of AI
* More appropriate for larger datasets than traditional ML
* Neural networks are the core of deep learning

Forward Propagation
- also known as feed-forward architecture
- data flows left to right through the network

Back Propagation
- At the output layer, a model error is calculated based on the obtained output and the
actual output and that error is propagated backwards to adjust weights.
- responsible for the learning in the network and used the minimise the loss function

Loss Function
- Most commonly used loss function: sum of the squared error
    - error is calculated as aggregating the squared differences between the actual output and
    the model/expected output

Steps of the learning algorithm:
- network weights are initialised to random values
- data is fed into the network (forward prop)
- actual output is compared to obtained output using loss function
- Error (loss value) is propagated backwards to adjust weights
- repeat

Cost of a neuron =
    * weights of all the edges
    * input values of a training sample
    * output of the training sample

( The above are all multiplied together to get the cost)
The goal is to minimise the cost - as the cost decreases, accuracy increases
We can use gradient descent instead of a brute-force approach

Back prop algorithm:
- until convergence is reached, perform the following
- present a training data instance
- calculate the error at the output layer
- calcupate the error at the hidden layer (all nodes) based on the error of the output nodes
- continue back through the model

Overfitting
- When the network tries to learn too many details from the training data
- results in poor performance on unseen data
- network fails to generalise.

- The key is to drop random units with their connections from the network

Drop out algorithm
- sample each node in each hidden layer with a probability value
- only keep edges that have both ends in the network

