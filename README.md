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

 As of 7/10, the only ML algorithm used in this project is [Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression). Logistic Regression is one of the first classification ML algorithms that any course will teach you. LR makes a prediction (the dependent variable) based off of the relationship between independent variables. In this project, the model will predict the winner of the fight (either blue corner or red corner) and the independent variables are all of the attributes documented in the `Data` section.

## PLANNED ALGORITHMS

`Support Vector Machines`

`Neural Network`
