from flask import Flask,render_template,session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
import toy_data

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

toy_data_lst = toy_data.get_choice()

class LoadDataForm(FlaskForm):
    selectData = SelectField('Pick your toy data:',
                             choices=toy_data_lst)
    submit = SubmitField('Select')

@app.route('/', methods=['GET','POST'])
def index():

    form = LoadDataForm()

    if form.validate_on_submit():
        #session['selectData'] = form.selectData.data
        #print(form.selectData.data)
        dataset = toy_data.get_dataset(int(form.selectData.data))

        return render_template('loadedData.html', form=form, dataset=dataset)


    return render_template('noData.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
