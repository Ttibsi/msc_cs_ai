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
