#!/usr/bin/env python
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# app config
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
	tickerName = TextField('Ticker Name:', validators=[validators.required()])
	sma1 = TextField('Simple Moving Average 1 (SMA) (eg 10):', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
	form = ReusableForm(request.form)

	print form.errors
	if request.method == 'POST':
		tickerName = request.form['tickerName']
		sma1 = request.form['sma1']
		print tickerName, sma1
		
		if form.validate():
			flash('Ticker Name: ' + tickerName)
			flash('Simple Moving Average 1 (SMA) (eg 10): ' + sma1)
		else:
			flash('Error: All the form fields are required. ')

	return render_template('index.html', form=form)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)
