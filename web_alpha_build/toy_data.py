import pandas as pd

def get_choice():
    choice_lst = [('1','Boston Housing'),('2','Classic Iris'),('3','Wine Classification'),('4','Breast Cancer')]
    return choice_lst

def get_dataset(ind):
    if ind == 1:
        from sklearn.datasets import load_boston
        data = load_boston()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['MEDV'] = data.target
        ds = df.to_html()
    elif ind == 2:
        from sklearn.datasets import load_iris
        data = load_iris()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['species'] = data.target
        ds = df.to_html()
    elif ind == 3:
        from sklearn.datasets import load_wine
        data = load_wine()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['class'] = data.target
        ds = df.to_html()
    else:
        from sklearn.datasets import load_breast_cancer
        data = load_breast_cancer()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['class'] = data.target
        ds = df.to_html()

    return ds



#load_boston()
