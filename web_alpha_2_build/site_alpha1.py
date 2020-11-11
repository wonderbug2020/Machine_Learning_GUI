from flask import Flask,render_template,session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField#, SubmitField, FloatField
#from wtforms.form import Form
#from wtforms.validators import DataRequired, NumberRange
import toy_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

toy_data_lst = toy_data.get_choice()

class LoadDataForm(FlaskForm):
    selectData = SelectField('Pick your toy data:',choices=toy_data_lst)

@app.route('/', methods=['GET','POST'])
def index():
    form = LoadDataForm()

    return render_template('LoadData.html',form=form)

@app.route('/DataTable', methods=['GET','POST'])
def index_data():
    dataset = toy_data.get_empty_df()

    return render_template('DataTable.html',dataset=dataset)

@app.route('/BuildModel', methods=['GET','POST'])
def index_model():

    return render_template('BuildModel.html')

@app.route('/ModelResult', methods=['GET','POST'])
def index_results():

    return render_template('ModelResult.html')

@app.route('/test', methods=['GET','POST'])
def test():
    form = LoadDataForm()
    print("this button was clicked")
    print(form.selectData)#.data)
    #dataset, headers = toy_data.get_dataset(int(form.selectData.data))
    return ""# render_template('DataTable.html',dataset=dataset)

if __name__ == '__main__':
    app.run(debug=True)
