from flask import Flask,render_template,session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField#, FloatField
import toy_data, ml_model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

#toy_data_lst = toy_data.get_choice()

class LoadDataForm(FlaskForm):
    selectToyData = SelectField('Pick your toy data:',choices=toy_data.get_choice())#choices=toy_data_lst)
    toySubmit = SubmitField('Select')

class LoadModelForm(FlaskForm):
    selectPredictor = SelectField('Pick which variable is the predictor')
    selectSplit = SelectField('Pick a test/train split between 0 and 1',choices=ml_model.get_split())
    selectTransform = SelectField('Pick a transform if you need one, else select none: ',choices=ml_model.get_transform())
    selectModel = SelectField('Pick the model you would like to use: ',choices=ml_model.get_model())

    modelSubmit = SubmitField('Build Model')


@app.route('/', methods=['GET','POST'])
def index():
    loadform = LoadDataForm()
    session['dataset'] = 0

    if loadform.validate_on_submit():
        session['getsel'] = int(loadform.selectToyData.data)

    return render_template('LoadData.html',form=loadform)

@app.route('/DataTable', methods=['GET','POST'])
def index_data():
    loadform = LoadDataForm()
    getsel = session.get('getsel',None)

    if (getsel == 1 or getsel == 2 or getsel == 3 or getsel == 4):
        dataset= toy_data.get_dataset(getsel,"table")
    else:
        dataset = toy_data.get_empty_df()

    return render_template('DataTable.html',dataset=dataset)

@app.route('/BuildModel', methods=['GET','POST'])
def index_model():
    buildform = LoadModelForm()
    getsel = session.get('getsel',None)
    headers = toy_data.get_dataset(getsel,"headers")
    buildform.selectPredictor.choices = headers

    if buildform.validate_on_submit():
        print('button clicked')
        #print(buildform.selectSplit.data)

    return render_template('BuildModel.html',form=buildform)

@app.route('/ModelResult', methods=['GET','POST'])
def index_results():

    return render_template('ModelResult.html')

if __name__ == '__main__':
    app.run(debug=True)