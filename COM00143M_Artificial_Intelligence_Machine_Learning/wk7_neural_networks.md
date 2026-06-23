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
    * also called logistic function
`relu(x) = max(0, x)`
    * Also called the Rectifier
`softplus(x) = log(1 + e^x)`
`tanh(x) = (e^2x - 1) / (e^2x + 1)`
`hard_threshold(x) = x >= 0 ? 1 : 0`

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

* Training consists of tuning parameters (weights) to minimise the loss on the training set
    * Usually done through some variant of Stochastic Gradient Descent (SGD)
* Real world NNs will be very large, so during SGD, it's common to use small minibatches to 
aid in escaping local minima and reduce the computational cost.
* Minibatches can be calculated independantly, so are often sized to the take advantage of 
GPU and TPU parallelism
* Batch Normalisation - technique used to improve the rate of convergence during SGD
    * rescales values in internal layers of the network from examples within each minibatch

---
A neuron is a linear function of it's inputs.
A neuron with n inputs has n+1 weights
The linear function is followed by the activation function, which is deliberately not a linear 
function

logistic regression uses gradient ascent, starting with an arbitrary assignment for weights
and iteratively improving them.

The logistic regression function is equivalent to a neuron as the logistic function as its
activation function.

Convolutions
* Some neurons act as a filter. Ex you may have a 3x3x1 filter, meaning that for each 3x3 space
in the input layer, 1 output node is populated. 
* The purpose of this is to reduce the amount of weights needed to calculate.
* Every copy in the output layer uses the same weights

Calculating output volume sizes:
* If Input volume is AxBxC, and filters have size PxQxC
* (A-P+1) x (B-Q+1) x n
* n is the number of filters in the layer

When calculating, the numbers in the multiplier (ex 10x10x1) are the number of neurons, not the 
number of weights. THERE IS ALWAYS ONE MORE WEIGHT FOR THE NEURON ITSELF, AS WELL AS A WEIGHT FOR
EVERY INPUT. In a 10x10x1 layer, we'd have 11 weights for every node on the second layer

Example:
Input layer: 15x15x1
First convolutional layer: 5 filters of 3x3x1
How many _weights_ are there?

3x3x1 size = 9 inputs = 10 weights per filter. 10 * 5 filters = 50 weights total
Layer size (output volume) = 13x13x5
    This is calculated as (15 - 3 + 1) x (15 - 3 + 1) * 5 filters
    See line 111 above

Second convolutional layer: 5 filters of 2x2x5

Each filter has 2x2x5 inputs = 20 inputs = 21 weights per filter. 21 * 5 filters = 105 weights
Layer size is calculated to be 12x12x5 using the same pattern as above

Output layer - fully connected layer with 10 neurons

Each neuron has 12x12x5 inputs, 12*12*5 = 721 * 10 neurons = 7210 weights

Total weights in the network = 50 + 105 + 7210 = 7365

---
Amount of neurons in current layer
* Follow formula on line 111
* AxB is prev layer
* PxQ is current layer
* Ignore filters

Amount of weights in current layer:
* Multiply out the layer size and filters
* See line 123

### Lesson 3 - Perils of Machine Learning in the Real World
* Used widely in machine autonomy - most commonly NNs in places such as autonomous vehicles
* use of RL to learn how to drive or react in specific scenarios
* Biggest problem is "interpretability". We dont know how NNs identify specific things 
(weights and values)
* NNs running into new things they can't identify - not included in the training data
* Overfitting might not recognise things such as traffic lights that are in different designs
or use different bulbs, for example
