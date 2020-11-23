from flask import Flask,render_template,session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField#, FloatField
import toy_data, ml_model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

#This is the form for loading in toy-data that will go on the loaddata page
class LoadDataForm(FlaskForm):
    selectToyData = SelectField('Pick your toy data:',choices=toy_data.get_choice())#choices=toy_data_lst)
    toySubmit = SubmitField('Select')

#This is the form for choosing all the normal parameters for building a machine learning model
class LoadModelForm(FlaskForm):
    selectPredictor = SelectField('Pick which variable is the predictor')
    selectSplit = SelectField('Pick a test/train split between 0 and 1',choices=ml_model.get_split())
    selectTransform = SelectField('Pick a transform if you need one, else select none: ',choices=ml_model.get_transform())
    selectModel = SelectField('Pick the model you would like to use: ',choices=ml_model.get_model())
    modelSubmit = SubmitField('Build Model')

#This is the page that is loaded in right from the beginning that asks the User to load in some data
@app.route('/', methods=['GET','POST'])
def index():
    loadform = LoadDataForm()
    session['dataset'] = 0

    if loadform.validate_on_submit():
        session['getsel'] = int(loadform.selectToyData.data)

    return render_template('LoadData.html',form=loadform)

#This page will display the data once it is loaded in
@app.route('/DataTable', methods=['GET','POST'])
def index_data():
    loadform = LoadDataForm()
    getsel = session.get('getsel',None)

    if (getsel == 1 or getsel == 2 or getsel == 3 or getsel == 4):
        dataset= toy_data.get_dataset(getsel,"table")
    else:
        dataset = toy_data.get_empty_df()

    return render_template('DataTable.html',dataset=dataset)

#This is the page where the user will build the model using selections
@app.route('/BuildModel', methods=['GET','POST'])
def index_model():
    buildform = LoadModelForm()
    getsel = session.get('getsel',None)
    headers = toy_data.get_dataset(getsel,"headers")
    buildform.selectPredictor.choices = headers

    if buildform.validate_on_submit():
        print('button clicked')
        session['Predsel'] = buildform.selectPredictor.data
        session['Splitsel'] = float(buildform.selectSplit.data)
        session['transformsel'] = buildform.selectTransform.data
        session['modelsel'] = buildform.selectModel.data

    return render_template('BuildModel.html',form=buildform)

#This page will display the outputs of the model
@app.route('/ModelResult', methods=['GET','POST'])
def index_results():
    modsel = []
    getsel = session.get('getsel',None)
    modsel.append(session.get('Predsel',None))
    modsel.append(session.get('Splitsel',None))
    modsel.append(session.get('transformsel',None))
    modsel.append(session.get('modelsel',None))
    metric_1=ml_model.run_model(getsel,modsel[0],modsel[1],modsel[2],modsel[3])
    #print(modsel[0])

    return render_template('ModelResult.html',metric_1=metric_1)#var=modsel[0])

if __name__ == '__main__':
    app.run(debug=True)
