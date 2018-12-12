from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt
def evaluate_svm(x_train,y_train,x_test,y_test):
    C_array = np.logspace(-3, 3, 15)
    gamma_array = np.logspace(-9, 3, 15)
    cv = StratifiedShuffleSplit(n_splits=10, test_size=0.25, random_state=22)
    tuned_parameters = [{'kernel': ['linear'], 'C': C_array.tolist(), "random_state": [22]}, {'kernel': ['rbf'], 'gamma': gamma_array.tolist(), 'C': C_array.tolist(), "random_state": [22]}, {'kernel': ['sigmoid'], 'gamma': gamma_array.tolist(), 'C': C_array.tolist(), "random_state": [22]}]

    results={}

    for params in tuned_parameters:
        score = 'f1'
        clf = GridSearchCV(SVC(), params, cv=cv, scoring='%s' % score)
        clf.fit(x_train,y_train)
        print("Best parameters for %s kernel: "%params['kernel'][0]+str(clf.best_params_))
        y_pred = clf.predict(x_test)
        scores = [f1_score(y_test,y_pred)]#, precision_score(te_y,y_pred), recall_score(te_y,y_pred), f1_score(te_y,y_pred)]
        results[params['kernel'][0]] = scores
    
    print(results)
        


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
   
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

def accuracy(y_pred,y_test):
    from sklearn.metrics import accuracy_score
    
    print(accuracy_score(y_test,y_pred))