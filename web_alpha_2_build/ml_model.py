#function that will provide a predetermined list of possible train/test split options
def get_split():
    split_lst = [('10'),('15'),('20'),('25'),('30'),('35'),('40')]
    return split_lst

#function that will provide a list of transformation processes
def get_transform():
    transform_lst = [('None'),('Standard Scaler')]
    return transform_lst

#idk why this isn't working
def get_model():
    model_lst = [('Logistic Regression')]
    return model_lst
