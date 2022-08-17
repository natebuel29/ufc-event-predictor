from . import model
from sklearn.feature_selection import RFE
from ufc_predictor import util


class LogisticRegressionModel(model.ModelInterface):
    def __init__(self, clf):
        self.clf = clf
        self.fit_support = None

    def fit(self, X, y):
        # Use Recursive Feature Elimation for feature selection
        rfe = RFE(self.clf)
        fit = rfe.fit(X, y)
        self.fit_support = fit.support_
        # filter to only the significant variables
        X = X[:, fit.support_]
        X = util.add_bias(X)
        self.clf.fit(X, y)

    def predict(self, future_X):
        return self.clf.predict(future_X).tolist()
