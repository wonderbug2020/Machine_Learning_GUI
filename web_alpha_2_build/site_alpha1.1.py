from flask import Flask,render_template,session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField#, FloatField
import toy_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

toy_data_lst = toy_data.get_choice()

class LoadDataForm(FlaskForm):
    selectToyData = SelectField('Pick your toy data:',choices=toy_data_lst)
    toySubmit = SubmitField('Select')

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

    return render_template('BuildModel.html')

if __name__ == '__main__':
    app.run(debug=True)
