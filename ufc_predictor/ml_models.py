from ufc_predictor.models.svm_model import SvmModel
from ufc_predictor.models.log_reg_model import LogisticRegressionModel
from ufc_predictor.models.neural_net_model import Model
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.preprocessing import StandardScaler

log_reg_clf = LogisticRegressionModel(LogisticRegression(random_state=2))
# parameters of kernel=rbf, c=5, and gamma=0.01 were the parameters selected by GridSearchCV
svm_clf = SvmModel(svm.SVC(kernel="rbf", C=5, gamma=0.01))
nn_clf = Model()

# StandardScaler for models
#z = (x-u)/s
# u=mean and s=std
standard_scalar = StandardScaler()
