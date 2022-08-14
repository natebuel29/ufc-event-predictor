
class ML_Model_Service:
    def __init__(self, clf):
        self.clf = clf

    def predict(self, X, y, future_X):
        self.clf.fit(X, y)
        clf_predictions = self.clf.predict(future_X).tolist()

        return clf_predictions
