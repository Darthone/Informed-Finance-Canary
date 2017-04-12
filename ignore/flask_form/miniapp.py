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
	sma2 = TextField('Simple Moving Average 2 (SMA) (eg 30):', validators=[validators.required()])
	dateRange = TextField('Length of Process: ', validators=[validators.required()])
	nslow = TextField('Slow EMA (eg 26): ', validators=[validators.required()])
	nfast = TextField('Fast EMA (eg 12): ', validators=[validators.required()])
	nema = TextField('EMA Signal Line (eg 9): ', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
	form = ReusableForm(request.form)

	print form.errors
	if request.method == 'POST':
		tickerName = request.form['tickerName']
		sma1 = request.form['sma1']
		sma2 = request.form['sma2']
		dateRange = request.form['dateRange']
		nslow = request.form['nslow']
		nfast = request.form['nfast']
		nema = request.form['nema']
		print tickerName, sma1, sma2, dateRange, nslow, nfast, nema
		
		if form.validate():
			flash('Ticker Name: ' + tickerName)
			flash('Simple Moving Average 1 (SMA) (eg 10): ' + sma1)
			flash('Simple Moving Average 2 (SMA) (eg 30): ' + sma2)
			flash('Length of Process: ' + dateRange)
			flash('Slow EMA (eg 26): ' + nslow)
			flash('Fast EMA (eg 12): ' + nfast)
			flash('EMA Signal Line (eg 9): ' + nema)
		else:
			flash('Error: All the form fields are required. ')

	return render_template('index.html', form=form)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)
