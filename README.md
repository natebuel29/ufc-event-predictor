 # Introduction

ufc-event-predictor is a Flask web app that displays predictions for weekly UFC events. It is composed of three components: the front-end web app (this page), [ufc-scraper-lambda](https://github.com/natebuel29/ufc-scraper-lambda), and a RDS database. The app is deployed to an Elastic Beanstalk instance using a CD GitHub Actions worklflow and the AWS CDK.

# Goals

Every Saturday my friends and I hop into a discord call to watch UFC fights and play video games. Watching UFC has become my one of my favorite thing to do with my Saturday night. We often try to predict the results of an event. We usually have a couple of disagreements in our predictions and have friendly discusssions about them. One of the goals of this project was to develop a ML model that I can share with my friends and others in the UFC community for more discussion. Being able to compare the actual results with our predicted results and the models predicted results will be fascinating.

Another goal of this project is to use an outside interest (UFC) to learn various ML algorithms. Before bringing an algorithm into this project, I will research and implement the algorithm from scratch in [ufc-stats-predictor-playground](https://github.com/natebuel29/ufc-stats-predictor-playground/tree/main/predictor_playground). Only after learning the algorithm will I bring it into this project using `scikit-learn`.


# Data

The data

 # ML Algorithms
 ### Logistic Regression

 As of 7/10, the only ML algorithm used in this project is [Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression). Logistic Regression is one of the first classification ML algorithms that any course will teach you.

## PLANNED ALGORITHMS

`Support Vector Machines`

`Neural Network`