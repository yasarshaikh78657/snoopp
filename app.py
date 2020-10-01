#import modules
import requests
from flask import Flask,render_template, redirect, request
import pickle
import bs4
import time
from time import gmtime, strftime
from datetime import datetime
from pytz import timezone


app = Flask(__name__)

#load the trained model
load_model = pickle.load(open('final_model.sav', 'rb'))

#function for scraping data from mygov.covid
def covid_data_scraping():
    data = requests.get("https://www.mygov.in/covid-19")
    bs = bs4.BeautifulSoup(data.text, 'html.parser')
    active_case= bs.find("div" , class_="information_row").find("div" , class_="iblock active-case").find("div" , class_="iblock_text").find("span", class_="icount").get_text()
    discharge= bs.find("div" , class_="information_row").find("div" , class_="iblock discharge").find("div" , class_="iblock_text").find("span", class_="icount").get_text()
    death= bs.find("div" , class_="information_row").find("div" , class_="iblock death_case").find("div" , class_="iblock_text").find("span", class_="icount").get_text()
    confirm= bs.find("div" , class_="information_row").find("div" , class_="iblock t_case").find("div" , class_="iblock_text").find("span", class_="icount").get_text()
    return confirm,active_case,discharge,death

#function for indian standerd time show
def ttime():
    now_utc = datetime.now(timezone('UTC'))
    now_india = now_utc.astimezone(timezone('Asia/Kolkata'))
    T = now_india.strftime("%d %B, %I:%M %p IST")
    return T
    

#index page    
@app.route('/')
def index():
    cds = covid_data_scraping()
    T = ttime()
    return  render_template('index.html',
                                   title='add text '
                                         'and submit',cds = cds,T = T)
										
#about page
@app.route('/about')
def about():
	return render_template('about.html')
#contact page	
@app.route('/contact')
def contact():
	return render_template('contact.html')
#how its work page	
@app.route('/hwd')
def hwd():
	return render_template('hwd.html')

    
#function to run for prediction
def detecting_fake_news(var):    
  #retrieving the best model for prediction call
  prediction = load_model.predict([var])
  prob = load_model.predict_proba([var])
  if prob[0][1] < 0.6:
      stc = "The given statement is \"False\", And its probability of reality is {}"
      stc = stc.format(prob[0][1])
      return stc
  else:
      stc = "The given statement is \"True\", And its probability of reality is {}"
      stc = stc.format(prob[0][1])
      if stc=="The given statement is \"True\", And its probability of reality is 0.6828804214017451":
          stc="Sorry, i can't understand!!!"
          return stc
      return stc
#result of model 
@app.route('/result', methods=['POST'])
def fetch():
    var = request.form["txt"]
    strres = detecting_fake_news(str(var))
    cds = covid_data_scraping()
    T = ttime()
    tag = "* the accuracy is 81% so maybe prediction is wrong sometime"
    return render_template('index.html', strres= strres,cds=cds,tag = tag,T = T)





if __name__ == "__main__":
    app.run(debug=True)


