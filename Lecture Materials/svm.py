from sklearn import datasets
# print iris
iris = datasets.load_iris()
X, y = iris.data, iris.target
#print(X)
#print(y)

from sklearn import svm
classifier = svm.SVC(gamma='auto', probability=True)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
#print(y_pred)
#print(classifier.predict_proba(X_test))

"""
# MLP
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
mlp.fit(X_train, y_train)
y_pred = mlp.predict(X_test)
print(y_pred)
print(mlp.predict_proba(X_test))
"""

from sklearn.metrics import accuracy_score
print(accuracy_score(y_pred, y_test))
print(accuracy_score(y_pred, y_test, normalize=False))

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

"""
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier
classifier = SklearnClassifier(LinearSVC())
"""
"""
import cPickle
s = cPickle.dumps(classifier)
clf2 = cPickle.loads(s)
print(clf2.predict(X[0:1]))
print(y[0])
"""
