from . import model
from ufc_predictor import util


class SvmModel(model.ModelInterface):
    def __init__(self, clf):
        self.clf = clf

    def fit(self, X, y):
        util.add_bias(X)
        self.clf.fit(X, y)

    def predict(self, future_X):
        return self.clf.predict(future_X).tolist()
