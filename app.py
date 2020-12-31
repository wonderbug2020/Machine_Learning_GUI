from flask import Flask,render_template,session, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import SelectField, SubmitField#, FloatField
import toy_data, ml_model

data_loaded=False
#model_selected=False

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'mysecretkey'

#This is the form for loading in toy-data that will go on the loaddata page
class LoadDataForm(FlaskForm):
    selectToyData = SelectField('Pick your toy data:',choices=toy_data.get_choice())#choices=toy_data_lst)
    toySubmit = SubmitField('Select')

#This is the form for finding out information about the selectPredictor
class PredictorForm(FlaskForm):
    selectPredictor = SelectField('Pick which variable is the predictor')
    selectType = SelectField('Are you building a regression or classification model',choices=['regression','classification'])
    predSubmit = SubmitField('Submit Predictor')

#This is the form for choosing all the normal parameters for building a machine learning model
class LoadModelForm(FlaskForm):
    selectSplit = SelectField('Pick a test/train split between 0 and 1',choices=ml_model.get_split())
    selectTransform = SelectField('Pick a transform if you need one, else select none: ',choices=ml_model.get_transform())
    selectModel = SelectField('Pick the model you would like to use: ')#,choices=ml_model.get_model())
    modelSubmit = SubmitField('Build Model')

#This is the page that is loaded in right from the beginning that asks the User to load in some data
@app.route('/', methods=['GET','POST'])
def index():
    loadform = LoadDataForm()
    session['dataset'] = 0
    home_text_1 = 'Hello and welcome to MLGUI'
    home_text_2 = 'To get started, select some toy data below to import'

    if loadform.validate_on_submit():
        session['getsel'] = int(loadform.selectToyData.data)
        home_text_1 = 'Now that you have loaded some data you can view it by clicking on the data page'
        home_text_2 = 'You can also load in another dataset below'
        return redirect(url_for('index_data'))

    return render_template('LoadData.html',form=loadform)

#This page will display the data once it is loaded in
@app.route('/DataTable', methods=['GET','POST'])
def index_data():
    loadform = LoadDataForm()
    predform = PredictorForm()
    getsel = session.get('getsel',None)
    headers = toy_data.get_dataset(getsel,"headers")
    predform.selectPredictor.choices = headers

    if predform.validate_on_submit():
        session['Predsel'] = predform.selectPredictor.data
        session['ModType'] = predform.selectType.data
        return redirect(url_for('index_model'))

    if (getsel == 1 or getsel == 2 or getsel == 3 or getsel == 4):
        dataset= toy_data.get_dataset(getsel,"table")
        data_loaded = True
    else:
        dataset = toy_data.get_empty_df()
        data_loaded = False

    if data_loaded == False:
        data_text_1 = 'You currently do not have any data loaded'
        data_text_2 = 'You can load in data from the home page'
    elif data_loaded == True:
        data_text_1 = 'Below is your data table'
        data_text_2 = 'Before you begin building your model, provide some information about the variable you are trying to predict'

    return render_template('DataTable.html',form=predform,dataset=dataset)

#This is the page where the user will build the model using selections
@app.route('/BuildModel', methods=['GET','POST'])
def index_model():
    buildform = LoadModelForm()
    buildform.selectModel.choices = ml_model.get_model(session.get('ModType',None))

    if buildform.validate_on_submit():
        print('button clicked')
        session['Splitsel'] = float(buildform.selectSplit.data)
        session['transformsel'] = buildform.selectTransform.data
        session['modelsel'] = buildform.selectModel.data
        session['model_state'] = True
        return redirect(url_for('index_results'))
    else:
        session['model_state'] = False

    if session.get('model_state',None) == False:
        model_text_1 = 'This is the model building page'
        model_text_2 = 'Select the inputs from the choices below to start building your model'
    elif session.get('model_state',None) == True:
        model_text_1 = 'You have succesfully built your model'
        model_text_2 = 'You can see the results of the model on the results page'

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
    if session.get('model_state',None) == False:
        result_text_1 = 'This page will display the results of your model'
        result_text_2 = "Make sure you have loaded some data and then go to the model page to build your model"
    elif session.get('model_state',None) == True:
        result_text_2, met = ml_model.run_model(getsel,modsel[0],modsel[1],modsel[2],modsel[3])
        result_text_1 = 'Here are the results from your model'

    return render_template('ModelResult.html',txt_1=result_text_1,txt_2=result_text_2)

if __name__ == '__main__':
    app.run(debug=True)
