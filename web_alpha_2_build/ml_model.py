import pandas as pd
import numpy
import toy_data

#function that will provide a predetermined list of possible train/test split options
def get_split():
    split_lst = [('.10'),('.15'),('.20'),('.25'),('.30'),('.35'),('.40')]
    return split_lst

#function that will provide a list of transformation processes
def get_transform():
    transform_lst = [('None'),('Standard Scaler')]
    return transform_lst

#idk why this isn't working
def get_model():
    model_lst = [('Logistic Regression')]
    return model_lst

def run_model(data,pred,split,trans,model):
    #print(f"your data is {data}")
    X,y = get_X_y(data,pred)
    #print(f"your Pred is {pred}")
    X_train, X_test, y_train, y_test = get_train_test_split(X,y,float(split))
    #print(f"your trans is {trans}")
    X_train, X_test = get_scaled_data(X_train,X_test,trans)#scaler)
    #print(f"your split is {split}")
    y_pred = run_the_model(X_train, y_train, X_test, model)
    #print(f"your model is {model}")
    cm,ac = get_metrics(y_test,y_pred)
    #print(f"The accuracy of the model is {ac}")
    return cm,ac


def get_X_y(data_in,predictor):
    data_ = toy_data.get_dataset(data_in,"dframe")
    y = data_[predictor].to_numpy()
    X = data_.drop(labels=[predictor],axis=1).to_numpy()
    return X, y

def get_train_test_split(X,y,split):
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=101)
    return X_train, X_test, y_train, y_test

def get_scaled_data(X_train,X_test,scalar):
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test

def run_the_model(X_train,y_train,X_test,model):
    from sklearn.linear_model import LogisticRegression
    log_cla = LogisticRegression(random_state = 0)
    log_cla.fit(X_train, y_train)
    y_pred = log_cla.predict(X_test)
    return y_pred

def get_metrics(y_test,y_pred):
    from sklearn.metrics import confusion_matrix, accuracy_score
    cm = confusion_matrix(y_test, y_pred)
    #print(cm)
    ac = accuracy_score(y_test, y_pred)
    #print(ac)
    return cm, ac
