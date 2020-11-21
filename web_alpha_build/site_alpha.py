from flask import Flask,render_template,session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange

import toy_data

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

toy_data_lst = toy_data.get_choice()

class LoadDataForm(FlaskForm):
    selectData = SelectField('Pick your toy data:',choices=toy_data_lst)
    submit = SubmitField('Select')

class BuildModelForm(FlaskForm):
    selectPredict = SelectField('Pick which variable is the predictor:')
    selectSplit = FloatField('Pick a test/train split between 0 and 1')#,validators=[DataRequired(), NumberRange(0,1)])
    selectTransform = SelectField('Pick a transform if you need one, else select none',choices=[('1','none'),('2','Standard Scaler')])
    selectModel = SelectField('Pick the model you would like to use: ',choices=[('1','Logistic Regression')])
    modelSubmit = SubmitField('Select 1')

@app.route('/', methods=['GET','POST'])
def index():

    form_1 = LoadDataForm()
    form_2 = BuildModelForm()

    if form_1.validate_on_submit():
        dataset, headers = toy_data.get_dataset(int(form_1.selectData.data))
        print(type(headers))
        form_2.selectPredict.choices = headers
        print("This was executed")
        return render_template('loadedData.html', form_1=form_1, form_2=form_2, dataset=dataset)

    return render_template('noData.html', form_1=form_1)

def modelBuilt():

    form_1 = LoadDataForm()
    form_2 = BuildModelForm()

    #if form_2.validate_on_submit():
    if form_2.modelSubmit.data and form_2.validate():
        print(form_2.selectPredict.data)
        print("this was also executed")
        return render_template('builtModel.html', form_1=form_1, form_2=form_2, dataset=dataset)


if __name__ == '__main__':
    app.run(debug=True)
