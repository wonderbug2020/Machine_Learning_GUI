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
    home_text_1 = 'Hello and welcome to MLGUI'
    home_text_2 = 'To get started, select some toy data below to import'

    if loadform.validate_on_submit():
        session['getsel'] = int(loadform.selectToyData.data)
        home_text_1 = 'Now that you have loaded some data you can view it by clicking on the data page'
        home_text_2 = 'You can also load in another dataset below'

    return render_template('LoadData.html',form=loadform,txt_1=home_text_1,txt_2=home_text_2)

#This page will display the data once it is loaded in
@app.route('/DataTable', methods=['GET','POST'])
def index_data():
    loadform = LoadDataForm()
    getsel = session.get('getsel',None)


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
        data_text_2 = 'You can begin building your model on the Model page'

    return render_template('DataTable.html',dataset=dataset,txt_1=data_text_1,txt_2=data_text_2)

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
        #model_selected = True
        session['model_state'] = True
    else:
        #model_selected = False
        session['model_state'] = False

    if session.get('model_state',None) == False:
        model_text_1 = 'This is the model building page'
        model_text_2 = 'Select the inputs from the choices below to start building your model'
    elif session.get('model_state',None) == True:
        model_text_1 = 'You have succesfully built your model'
        model_text_2 = 'You can see the results of the model on the results page'

    return render_template('BuildModel.html',form=buildform,txt_1=model_text_1,txt_2=model_text_2)

#This page will display the outputs of the model
@app.route('/ModelResult', methods=['GET','POST'])
def index_results():
    modsel = []
    getsel = session.get('getsel',None)
    modsel.append(session.get('Predsel',None))
    modsel.append(session.get('Splitsel',None))
    modsel.append(session.get('transformsel',None))
    modsel.append(session.get('modelsel',None))
    #metric_1=ml_model.run_model(getsel,modsel[0],modsel[1],modsel[2],modsel[3])
    if session.get('model_state',None) == False:
        result_text_1 = 'This page will display the results of your model'
        result_text_2 = "Make sure you have loaded some data and then go to the model page to build your model"
    elif session.get('model_state',None) == True:
        metric_1, met = ml_model.run_model(getsel,modsel[0],modsel[1],modsel[2],modsel[3])
        result_text_1 = 'Here are the results from your model'
        if met == 'reg':
            result_text_2 = f'Your model had an R2 score of {metric_1}'
        elif met == 'cla':
            result_text_2 = f'Your model had an accuracy of {metric_1}'

    return render_template('ModelResult.html',txt_1=result_text_1,txt_2=result_text_2)

if __name__ == '__main__':
    app.run(debug=True)
