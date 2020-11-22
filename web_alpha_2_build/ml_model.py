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

#function that will provide a list of different models
def get_model():
    model_lst = [('Logistic Regression')]
    return model_lst

#This is the main function that calls all the other functions to build and run the model
def run_model(data,pred,split,trans,model):
    X,y = get_X_y(data,pred)
    X_train, X_test, y_train, y_test = get_train_test_split(X,y,float(split))
    X_train, X_test = get_scaled_data(X_train,X_test,trans)#scaler)
    y_pred = run_the_model(X_train, y_train, X_test, model)
    cm,ac = get_metrics(y_test,y_pred)
    return cm,ac

#This function seperates the data into X and y components
def get_X_y(data_in,predictor):
    data_ = toy_data.get_dataset(data_in,"dframe")
    y = data_[predictor].to_numpy()
    X = data_.drop(labels=[predictor],axis=1).to_numpy()
    return X, y

#This function takes a user input and creates the train-test split
def get_train_test_split(X,y,split):
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=101)
    return X_train, X_test, y_train, y_test

#This function takes te user input and transforms thet data is they want that
def get_scaled_data(X_train,X_test,scalar):
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test

#This function actually runs the choosen model
def run_the_model(X_train,y_train,X_test,model):
    from sklearn.linear_model import LogisticRegression
    log_cla = LogisticRegression(random_state = 0)
    log_cla.fit(X_train, y_train)
    y_pred = log_cla.predict(X_test)
    return y_pred

#This function out puts the accuracy and confusion matrix results of the model
def get_metrics(y_test,y_pred):
    from sklearn.metrics import confusion_matrix, accuracy_score
    cm = confusion_matrix(y_test, y_pred)
    ac = accuracy_score(y_test, y_pred)
    return cm, ac
