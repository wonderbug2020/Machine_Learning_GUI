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

    if loadform.validate_on_submit():
        dataset, headers = toy_data.get_dataset(int(loadform.selectToyData.data))
        return render_template('DataTable.html',dataset=dataset)

    return render_template('LoadData.html',form=loadform)

@app.route('/DataTable', methods=['GET','POST'])
def index_data():
    dataset = toy_data.get_empty_df()

    return render_template('DataTable.html',dataset=dataset)

if __name__ == '__main__':
    app.run(debug=True)
