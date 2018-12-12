from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout

def svm(x_train,y_train,x_test):
    #Train SVM
    from sklearn.svm import LinearSVC, SVC

    svm = LinearSVC(C = 0.25, loss = 'hinge',penalty = 'l2')
    svm.fit(x_train,y_train)
    y_pred = svm.predict(x_test)
    return y_pred

def decision_tree(x_train,y_train,x_test):
    from sklearn.tree import DecisionTreeClassifier

    dt = DecisionTreeClassifier(criterion = 'gini', max_depth = 4)

    dt.fit(x_train,y_train)
    y_pred = dt.predict(x_test)
    return y_pred

def keras_1(x_train,y_train,x_test):
    """ Creates a Sequential model made out of Densely connected Neural Network layers. All parameters are configured as per specification for Q4"""

    model = Sequential()
    model.add(Dense(10,input_dim = x_train.shape[1], activation = 'relu'))
    model.add(Dense(100,activation = 'relu'))
    model.add(Dense(700,activation = 'relu'))
    model.add(Dense(123,activation = 'sigmoid'))
    model.add(Dense(y_train.shape[1],activation = 'softmax'))
    
    model.compile(loss = 'mse', optimizer ='adam',metrics = ['accuracy'])

    model.fit(x_train,y_train,epochs = 10, batch_size = 100)

    return model.predict(x_test)
   
def keras_2(x_train,y_train,x_test):
    """ Creates a Sequential model made out of Densely connected Neural Network layers. All parameters are configured as per specification for Q4"""

    model = Sequential()
    #Input Layer with 61 inputs corresponding to 61 features 
    model.add(Dense(10,input_dim = x_train.shape[1], activation = 'relu'))

    model.add(Dense(100,activation = 'relu'))
    model.add(Dense(700,activation = 'relu'))
    model.add(Dense(123,activation = 'sigmoid'))
    model.add(Dense(y_train.shape[1],activation = 'softmax'))
    
    #Compiling the model with appropriate parameters
    model.compile(loss = 'mse', optimizer ='adam',metrics = ['accuracy'])
    model.fit(x_train,y_train,epochs = 10, batch_size = 100)

    return model.predict(x_test)

 # z =accuracy_score(y_test,y_pred)
    # print(z)
    # mc = misclassification_report(full_data,y_pred,y_test)