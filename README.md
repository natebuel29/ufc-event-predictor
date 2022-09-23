 # Introduction

ufc-event-predictor is a Flask web app that displays predictions for weekly UFC events. It is composed of three components: the front-end web app (this project), [ufc-scraper-lambda](https://github.com/natebuel29/ufc-scraper-lambda), and a RDS database. The app is deployed to an Elastic Beanstalk instance using a CD GitHub Actions worklflow and the AWS CDK.

# Goals

Every Saturday my friends and I hop into a discord call to watch UFC fights and play video games. Watching UFC has become my one of my favorite thing to do with my Saturday nights. We often try to predict the results of an event and compare our predictions with eachother. It always feels good to be the one who correctly predicts a fight so I decided to make this project. One of the goals of this project is to develop a ML model that predicts UFC events that I can share with my friends and others in the UFC community. Being able to compare the actual results with our predicted results and the models predicted results will be fascinating.

Another goal of this project is to use an outside interest (UFC) to learn various ML algorithms. Before bringing an algorithm into this project, I will research and implement the algorithm from scratch in [ufc-stats-predictor-playground](https://github.com/natebuel29/ufc-stats-predictor-playground/tree/main/predictor_playground). Only after learning the algorithm will I bring it into this project using `scikit-learn`.


# Data

All fighter and event data used is scraped from [ufcstats.com](http://ufcstats.com/statistics/events/completed). The following fighter attributes are used by the model to predict fights:

- Wins

- Loses

- SLpM - Significant Strikes Landed per Minute

- Str. Acc. - Significant Striking Accuracy

- SApM - Significant Strikes Absorbed per Minute

- Str. Def. - Significant Strike Defence (the % of opponents strikes that did not land)

- TD Avg. - Average Takedowns Landed per 15 minutes

- TD Acc. - Takedown Accuracy

- TD Def. - Takedown Defense (the % of opponents TD attempts that did not land)

- Sub. Avg. - Average Submissions Attempted per 15 minutes

 # ML Algorithms

 ## Logistic Regression

Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression) is one of the first classification ML algorithms that any course will teach you. LR makes a prediction (the dependent variable) based off of the relationship between independent variables. In this project, the model will predict the winner of the fight (either blue corner or red corner) and the independent variables are all of the attributes documented in the `Data` section.

 ## Support Vector Machines

[Support Vector Machines](https://en.wikipedia.org/wiki/Support-vector_machine) is a classification ML algorithm that determines a decision boundary between two categories of data and maximizes the width of the gap between the two categories. After the decision boundary has been found through optimization and training, predictions are made by mapping data into the space and determining what side of the decision boundary the point lies on.

SVM has some important hyperparameters. Firstly, the kernel parameter determines what kernel function should be used in the algorithm. A [kernel function](https://en.wikipedia.org/wiki/Kernel_method) is a method used to convert linearly inseparable data to linearly separable by transforming the data into higher dimensions. A few kernel methods are linear, polynomial, and radial basis function. Next, the C parameter tells the optimization how much you want to avoid misclassifying the training examples. Large values of C will choose a smaller margin with fewer misclassifications and large values of C will choose a more significant margin with more misclassifications. The last parameter I will talk about is the gamma parameter. Gamma defines how far the influence of a single training example reaches. A low value means 'far' and a high value means 'close'.

For our data, the following parameters were selected using [sklearn.GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html):

- `Kernel = rbf`
- `C = 5`
- `gamma = .001`

## Neural Networks

A [Neural Network](https://en.wikipedia.org/wiki/Neural_network) is a ML algorithm that processes data in way that is heavily inspired by the human brain. Neural networks involve interconnected nodes (neurons) structured in a layer. These connected nodes represent the neurons and synapses of a biological brain. Neural networks are the heart of deep learning algorithms.

![Neural Network Image](https://www.tibco.com/sites/tibco/files/media_entity/2021-05/neutral-network-diagram.svg)

Neural networks have a lot of hyperparameters. Below are the hyperparameters that recieved the best results during testing:

- `neural network structure = input -> 256 -> 256 -> 256 -> 1 (prediction)`
- `activation functions for hidden layers = relu`
- `activation functions for output layers = sigmoid`
- `optimizer = adam with a learning rate of 1e-3 and decay of 1e-9`
- `regularizer = l2`
