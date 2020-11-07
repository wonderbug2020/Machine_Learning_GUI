from flask import Flask,render_template,session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange

#import toy_data

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/', methods=['GET','POST'])
def index():

    return render_template('LoadData.html')

@app.route('/DataTable', methods=['GET','POST'])
def index_data():

    return render_template('DataTable.html')

@app.route('/BuildModel', methods=['GET','POST'])
def index_model():

    return render_template('BuildModel.html')

@app.route('/ModelResult', methods=['GET','POST'])
def index_results():

    return render_template('ModelResult.html')

if __name__ == '__main__':
    app.run(debug=True)
