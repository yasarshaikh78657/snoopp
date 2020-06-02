import requests
from flask import Flask, render_template, redirect, request
from covid_india import states
import pickle
import bs4
import datetime
import pytz

app = Flask(__name__)

load_model = pickle.load(open('final_model.sav', 'rb'))


# function for scraping data from mygov.covid
def covid_data_scraping():
	data = requests.get("https://www.mygov.in/covid-19")
	bs = bs4.BeautifulSoup(data.text, 'html.parser')
	active_case = bs.find("div", class_="information_row").find("div", class_="iblock active-case").find("span",
																										 class_="icount").get_text()
	discharge = bs.find("div", class_="information_row").find("div", class_="iblock discharge").find("span",
																									 class_="icount").get_text()
	death = bs.find("div", class_="information_row").find("div", class_="iblock death_case").find("span",
																								  class_="icount").get_text()
	active_case = int(active_case)
	discharge = int(discharge)
	death = int(death)
	confirm = active_case + discharge + death
	return confirm, active_case, discharge, death


def ttime():
    d = datetime.datetime.now()
    timezone = pytz.timezone("Asia/Kolkata")
    d_aware = timezone.localize(d)
    d_aware.tzinfo
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    ist_now = utc_now.astimezone(pytz.timezone("Asia/Kolkata"))
    ist_now.isoformat()
    return ist_now 


@app.route('/')
def index():
	cds = covid_data_scraping()
	T = ttime()
	state = 'Gujarat'
	data = states.getdata(state)
	return render_template('index.html',
						   title='add text '
								 'and submit', cds=cds, data=data, state=state, T=T)


@app.route('/state/', methods=["POST"])
def search_statte():
	cds = covid_data_scraping()
	if request.method == 'POST':
		state = request.form['state']
		data = states.getdata(state)
		return render_template('index.html', data=data, state=state, cds=cds)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/contact')
def contact():
	return render_template('contact.html')


@app.route('/hwd')
def hwd():
	return render_template('hwd.html')


# function to run for prediction
def detecting_fake_news(var):
	# retrieving the best model for prediction call
	prediction = load_model.predict([var])
	prob = load_model.predict_proba([var])
	if prob[0][1] < 0.6:
		stc = "The given statement is \"False\", And its probability of reality is {}"
		stc = stc.format(prob[0][1])
		return stc
	else:
		stc = "The given statement is \"True\", And its probability of reality is {}"
		stc = stc.format(prob[0][1])
		if stc == "The given statement is \"True\", And its probability of reality is 0.6828804214017451":
			stc = "Sorry, i can't understand!!!"
			return stc
		return stc


@app.route('/result', methods=['POST'])
def fetch():
	var = request.form["txt"]
	strres = detecting_fake_news(str(var))
	cds = covid_data_scraping()
	state = 'Gujarat'
	data = states.getdata(state)
	tag = "* the accuracy is 81% so maybe prediction is wrong sometime"
	return render_template('index.html', strres=strres, cds=cds, data=data, state=state, tag=tag)


if __name__ == "__main__":
	app.run(debug=True)