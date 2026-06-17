# Week 7 - Machine Learning with Neural Networks

* Identify the strengths and weaknesses of linear regression, logistic regression, and neural networks for supervised learning tasks
* Train and evaluate linear regression, logistic regression, and neural network models using a machine learning toolkit
* Identify safety issues when machine learning systems are deployed in the real world, in particular in autonomous vehicles.

### Week 1 - Regression and Classification with Linear Models
* linear regression - used in regression
* logistic regression - used to classify data

Linear models 
- output is just the sum of the attribute values with weights applied
- Coming up with weights is the challenge
`(A*1.2) + (B*0.7) * (C*1) = X` is an example, where the float literals are weights applied
to each input parameter A,B,C

* On the first iteration, you estimate a weight using the `least squares linear regression` method.
    * Another option is `Least Absolute Deviation`
* weights are chosen to minimise the sum of the square of the errors

Logistic regression is very closely related to linear regression, but instead of predicting a
number, it predicts a probability of 0-1.
This works by taking the result of a linear function and passing it through a logistic function

Often, test data will go through the calculations and the value closest to the result will be 
selected. (EX if you get the result 0.7, the binary result of 1 will be selected). This is 
called "Multiresponse linear regression"

### Lesson 2- Neural Networks and Deep Learning
* A logistic regression function can be thought of as a form of neuron
* NNs are supervised learning.
* Deep learning - neural networks with many layers
    * Deep learning refers to the fact that "circuits" have many layers
    * Originated with work that tried to replicate how neurons worked in the brain, hence the name.
    However this is no longer the case

FeedForward Networks
* Only calculates in one direction
* Is made of a DAG with designated input/output nodes

* Recurrent network - feeds intermediate values back to its own inputs.

Each node in a network is a "Unit"
A node has inputs and the edges have weights
The value of every node is put through an "activation function" such as sigmoid or relu as part 
of the calculation

activation functions:
`sigmoid(x) = 1 / (1 + e^-x)`
`relu(x) = max(0, x)`
`softplus(x) = log(1 + e^x)`
`tanh(x) = (e^2x - 1) / (e^2x + 1)`

Gradient Descent learning - calculate the gradient of the loss function with respect to the weights
                            and adjust the weights along the gradient to reduce the loss

`Squared Loss function` - used to calculate the gradient

When representing adjacency, ie when the inputs are images and nodes represent specific pixels, 
the first hidden layer can be constructed to only recieve inputs from a localised region of the
inputs. This is usually one part fo the Convolutional Neural Network

Pooling layer - "pools together" a set of presceeding values in previous layers into a single value.
This doesn't usually use an activation function.
    * Average pooling - calculates the average of the input values
    * max pooling - finds the maximum value from the inputs, useful for downsampling.

CNNs use tensors and tensor calculations instead of vector mathematics. These are often 
represented as 2D arrays. 

Residual networks
* an approach to building very deep networks that avoid the problem of vanishing gradients
* Conceptually, a layer will "perturb" the representation from the previous layer instead
of replacing it wholesale.
    * If this perturbation is small, the next layer is very similar to the previous
* This are often used with CNNs in vision applications, but are a general-purpose tool
* Not uncommon to see hundreds of layers in a residual CNN.
