import pandas as pd
import numpy
import toy_data

#function that will provide a predetermined list of possible train/test split options
def get_split():
    split_lst = [('.10'),('.15'),('.20'),('.25'),('.30'),('.35'),('.40')]
    return split_lst

#function that will provide a list of transformation processes
def get_transform():
    transform_lst = [('None'),('Standard Scaler'),('MinMax Scaler'),('Robust Scaler'),('Normalizer')]
    return transform_lst

#function that will provide a list of different models
def get_model(model_type):
    if model_type == 'regression':
        model_lst = ['Linear Regression']
    elif model_type == 'classification':
        model_lst = ['Logistic Regression','KNN','Decision Tree','Random Forest','Support Vector Machines','Gaussian NB']
    else:
        model_lst = [('Linear Regression'),('Logistic Regression'),('KNN'),('Decision Tree'),
                    ('Random Forest'),('Support Vector Machines'),('Gaussian NB')]
    return model_lst

#This is the main function that calls all the other functions to build and run the model
def run_model(data,pred,split,trans,model):
    X,y = get_X_y(data,pred)
    X_train, X_test, y_train, y_test = get_train_test_split(X,y,float(split))
    X_train, X_test = get_scaled_data(X_train,X_test,trans)#scaler)
    y_pred,met = run_the_model(X_train, y_train, X_test, model)
    if met == 'reg':
        text = get_reg_metrics(y_test,y_pred)
    elif met == 'cla':
        text = get_cla_metrics(y_test,y_pred)
    return text,met

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
    if scalar == 'Standard Scaler':
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
    elif scalar == 'MinMax Scaler':
        from sklearn.preprocessing import MinMaxScaler
        sc = MinMaxScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
    elif scalar == 'Robust Scaler':
        from sklearn.preprocessing import RobustScaler
        sc = RobustScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
    elif scalar == 'Normalizer':
        from sklearn.preprocessing import Normalizer
        sc = Normalizer()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
    else:
        print("no scalar was choosen")
    return X_train, X_test

#This function actually runs the choosen model
def run_the_model(X_train,y_train,X_test,model):
    if model == 'Linear Regression':
        from sklearn.linear_model import LinearRegression
        lin_reg = LinearRegression()
        lin_reg.fit(X_train,y_train)
        y_pred = lin_reg.predict(X_test)
        met = "reg"
    elif model == 'Logistic Regression':
        from sklearn.linear_model import LogisticRegression
        log_cla = LogisticRegression(random_state = 0)
        log_cla.fit(X_train, y_train)
        y_pred = log_cla.predict(X_test)
        met = "cla"
    elif model == 'KNN':
        from sklearn.neighbors import KNeighborsClassifier
        knn = KNeighborsClassifier(n_neighbors=5, metric = 'minkowski', p = 2)
        knn.fit(X_train,y_train)
        y_pred = knn.predict(X_test)
        met = "cla"
    elif model == "Decision Tree":
        from sklearn.tree import DecisionTreeClassifier
        dtree = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
        dtree.fit(X_train,y_train)
        y_pred = dtree.predict(X_test)
        met = "cla"
    elif model == "Random Forest":
        from sklearn.ensemble import RandomForestClassifier
        rfc = RandomForestClassifier(n_estimators=10, criterion = 'entropy', random_state = 0)
        rfc.fit(X_train,y_train)
        y_pred = rfc.predict(X_test)
        met = "cla"
    elif model == "Support Vector Machines":
        from sklearn.svm import SVC
        svc_model = SVC(kernel = 'linear', random_state = 0)
        svc_model.fit(X_train, y_train)
        y_pred = svc_model.predict(X_test)
        met = "cla"
    elif model == "Gaussian NB":
        from sklearn.naive_bayes import GaussianNB
        nbg = GaussianNB()
        nbg.fit(X_train, y_train)
        y_pred = nbg.predict(X_test)
        met = "cla"
    return y_pred, met

#This function outputs the R2 results of the model
def get_reg_metrics(y_test,y_pred):
    from sklearn.metrics import r2_score
    Rs = r2_score(y_test,y_pred)
    rscore = round(Rs,2)
    if rscore >= .90:
        text=f"Your model performed very well with an R^2 value of {rscore}"
    elif rscore >= .70:
        text=f"Your model performed okay with an R^2 value of {rscore}"
    else:
        text=f"Your model performed poorly with an R^2 value of {rscore}"
    return text

#This function out puts the accuracy and confusion matrix results of the model
def get_cla_metrics(y_test,y_pred):
    from sklearn.metrics import confusion_matrix, accuracy_score
    #cm = confusion_matrix(y_test, y_pred)
    ac = accuracy_score(y_test, y_pred)
    acc = round(ac,2)
    if acc >= .90:
        text=f"Your model performed very well with an accuracy of {acc}"
    elif acc >= .70:
        text=f"Your model performed okay with an accuracy of {acc}"
    else:
        text=f"Your model performed poorly with an accuracy of {acc}"
    return text#, cm
