def get_pred_sug(selection):
    if selection == 1:
        text = f'You have choosen the Boston Housing dataset where the MEDV variable is typically used as the predictor which requires a regression model'
    elif selection == 2:
        text = f'You have choosen the Classic Iris dataset where the species variable is typically used as the predictor which requires a classification model'
    elif selection == 3:
        text = f'You have choosen the Wine Classification dataset where the class variable is typically used as the predictor which requires a classification model'
    elif selection == 4:
        text = f'You have choosen the Breast Cancer dataset where the class variable is typically used as the predictor which requires a classification model'
    else:
        text = f'You have not made a selection yet'

    return text
