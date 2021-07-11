from flask import Flask, render_template, request
import os
import requests
from bs4 import BeautifulSoup as bs


#request url + parses
url = "https://ncov2019.live/"
r = requests.get(url)
page = r.text
page_soup = bs(page, "html.parser")


#create container using worldwide table
containers = page_soup.findAll("div", {"class": "container--wrap bg-navy-4 table-container col hide-mobile"})
container = containers[1]


#create functions for scraping country, deceased, active cases, and vaccination delattr
def country_scraper():
  global container
  country_container = container.findAll('td', {"class": "text--gray"})
  return_list = []

  return_list.append(country_container[0].text.strip())
  for i in range(1, len(country_container)):
    country_container_2 = country_container[i].findAll('span')
    return_list.append(country_container_2[1].text.strip())
  
  return return_list

def deceased_scraper():
  global container
  deceased_container = container.findAll('td', {"class": "text--red"})
  return_list = []

  for i in range(len(deceased_container)):
    if i % 2 == 0:
      deceased_container_2 = deceased_container[i].findAll('span')
      return_list.append(deceased_container_2[0].text.strip())
  
  return return_list

def active_scraper():
  global container
  active_cases_container = container.findAll('td', {"class": "text--yellow"})
  return_list = []

  for i in range(len(active_cases_container)):
    return_list.append(active_cases_container[i].text.strip())
  
  return return_list

def vaccination_scraper():
  global container
  vaccination_container = container.findAll('td', {"class": "text--blue"})
  return_list = []

  for i in range(len(vaccination_container)):
    if i % 4 == 2:
      return_list.append(vaccination_container[i].text.strip())
  
  return return_list

def population_scraper():
  global container
  population_counter = container.findAll('td', {"class": "text--blue"})
  return_list = []

  for i in range(len(population_counter)):
    if i % 4 == 3:
      return_list.append(population_counter[i].text.strip())
    
  return return_list

#secret key practice https://stackoverflow.com/questions/30873189/where-should-i-place-the-secret-key-in-flask
#create app function
def create_app(test_config=None):
  # create and configure the app - taken from https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
      SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
      DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  if test_config is None:
      # load the instance config, if it exists, when not testing
      app.config.from_pyfile('config.py', silent=True)
  else:
      # load the test config if passed in
      app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
      os.makedirs(app.instance_path)
  except OSError:
      pass

  #create lists for storing scraped values
  countries, deceased, activecases, vaccinations, population, percent_active, percent_vax = [], [], [], [], [], [], []
  
  #route handling
  @app.errorhandler(404)
  def pageNotFound(error):
    return render_template('other/404.html')

  @app.route('/')
  def home():
    return render_template('other/home.html')

  @app.route('/data', methods=['get', 'post'])
  def data():
    countries = country_scraper()
    deceased = deceased_scraper()
    activecases = active_scraper()
    vaccinations = vaccination_scraper()
    population = population_scraper()
    for i in range(len(population)):
      try:
        percent_active.append(str(100*(float(activecases[i].replace(",", "")))/(float(population[i].replace(",", "")))))
      except:
        percent_active.append("Unknown")
      try:
        percent_vax.append(str(100*(float(vaccinations[i].replace(",", "")))/(float(population[i].replace(",", "")))))
      except:
        percent_vax.append("Unknown")
    
    return render_template('other/data.html', countries = countries, population=population, deceased = deceased, activecases = activecases, vaccinations = vaccinations, percent_active=percent_active, percent_vax=percent_vax, length=len(countries))
    #how to group table (by column, by continent)
    #background colors based on % of vaccinations/active cases (based on sort?)

  from . import db
  db.init_app(app)

  from . import auth
  app.register_blueprint(auth.bp)
  
  return app

"""if __name__ == '__main__':
  create_app().run(debug=True, host='0.0.0.0')"""
#https://hack-the-cloud-20.ryanlee35.repl.co/