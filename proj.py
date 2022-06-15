
from msilib.schema import Directory
from unittest import result
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import pickle
import numpy as np
import mysql.connector
from bs4 import BeautifulSoup
import requests
import json

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(
    directory="htmldirectory/")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/icon", StaticFiles(directory="icon"), name="icon")


# @app.get('/home')
# async def home():
#     return{'Data': 'Hello world'}


@app.get('/')
async def home(request: Request):
    latest_news = dict()
    treat_news = dict()

    html_text = requests.get('https://www.medicalnewstoday.com/news').text
    soup = BeautifulSoup(html_text, 'html.parser')
    new = soup.find_all('li', class_='css-kbq0t')
    for news in new:
        publish_date = news.find('div', class_='css-3be604').text
        # if(date == publish_date):
        news_title = news.find('h2', class_='css-5dw8ta').text
        news_desc = news.find('a', class_='css-2fdibo').text
        latest_news[news_title] = news_desc

    html_text = requests.get('https://www.medicalnewstoday.com/news').text
    soup = BeautifulSoup(html_text, 'html.parser')
    new = soup.find_all('li', class_='css-kbq0t')
    for news in new:
        news_title = news.find('a', class_='css-1mttucs').text
        news_desc = news.find('a', class_='css-2fdibo').text
        treat_news[news_title] = news_desc

    return templates.TemplateResponse('Home.html',
                                      context={"request": request, 'latest_news': latest_news, 'treat_news': treat_news})


@ app.get('/contact')
async def contact(request: Request):
    return templates.TemplateResponse('contact.html',
                                      context={"request": request})


@ app.get('/about')
async def about(request: Request):
    return templates.TemplateResponse('about.html',
                                      context={"request": request})


@ app.get('/consultency')
async def consultency(request: Request):
    return templates.TemplateResponse('consultency.html',
                                      context={"request": request})


@ app.post('/consultency_reasult')
async def consultency_reasult(request: Request, country: str = Form(...),
                              state: str = Form(...),
                              city: str = Form(...),
                              disease: str = Form(...)):
    reasult = ""
    print(country, state, city, disease)

    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="health_care_system")
    if myconn.is_connected():
        cur = myconn.cursor()
        sql = "SELECT * FROM doctor_tb WHERE Dcountry = '%s' AND Dstate = '%s' AND Dcity = '%s' AND Dspeciality = '%s'"

        val = (country, state, city, disease)

        try:
            cur.execute(sql % val)
            record = cur.fetchall()
            if record is not None:
                print(record)
                return json.dumps(record)
            else:
                return json.dumps([])
        except:
            print('Checking in record problem...')
        finally:
            cur.close()
            myconn.close()
    else:

        print("Connection Problem")
        reasult = 0
    return reasult


@ app.get('/diabetes')
async def diabetes(request: Request):
    latest_news = dict()
    treat_news = dict()

    html_text = requests.get('https://www.medscape.com/index/list_5458_0').text
    soup = BeautifulSoup(html_text, 'html.parser')
    new = soup.find_all('li', class_='')
    for news in new:
        news_title = news.find('a', class_='title').text
        news_desc = news.find('span', class_='teaser').text
        latest_news[news_title] = news_desc

    html_text = requests.get(
        'https://www.medscape.com/index/list_13472_0').text
    soup = BeautifulSoup(html_text, 'html.parser')
    new = soup.find_all('li', class_='')
    for news in new:
        news_title = news.find('a', class_='title').text
        news_desc = news.find('span', class_='teaser').text
        treat_news[news_title] = news_desc

    return templates.TemplateResponse('diabetes.html',
                                      context={"request": request, 'latest_news': latest_news, 'treat_news': treat_news})


# @app.get('/diabitiesf')
# async def diabities(request: Request):
#     return templates.TemplateResponse('Diabities.html',
#                                       context={"request": request})


@ app.post('/diabetes_prediction_result')
async def diabeteCheck(request: Request, userpregnancies: int = Form(...),
                       userglucose: int = Form(...),
                       userbp: int = Form(...),
                       userskin: int = Form(...),
                       userinsulin: int = Form(...),
                       userbmi: float = Form(...),
                       userdpf: float = Form(...),
                       userage: int = Form(...)):

    data = np.array([userpregnancies, userglucose, userbp, userskin,
                    userinsulin, userbmi, userdpf, userage]).reshape(1, -1)
    filename = "models/Dlr.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    output = loaded_model.predict(data)[0]

    if output == 0:
        result = "Patient is healthy and minor chance to have a Diabetes in future."
    else:
        result = "Patient will have a higher chance to have a Diabetes in near time so please follow these many instruction."

    return templates.TemplateResponse('Diapredict.html',
                                      context={"request": request, "result": result})


@app.get('/kidney')
async def kidney(request: Request):
    latest_news = dict()

    html_text = requests.get(
        'https://economictimes.indiatimes.com/topic/chronic-kidney-disease').text
    soup = BeautifulSoup(html_text, 'html.parser')
    # d = soup.find('div', class_='grid grid-8 mq875-grid-12')
    new = soup.find_all('div', class_='clr flt topicstry story_list')
    for news in new:

        news_title = news.find('h2', class_='').text
        news_desc = news.find('div', class_='syn').text
        latest_news[news_title] = news_desc

    return templates.TemplateResponse('kidney.html',
                                      context={"request": request, 'latest_news': latest_news})


# @app.get('/kidneyf')
# async def kidney(request: Request):
#     return templates.TemplateResponse('kidneydisease.html',
#                                       context={"request": request})


@app.post('/kidney_prediction')
async def kidney_check(request: Request, auserage: int = Form(...),
                       auserbp: int = Form(...),
                       ausersu: int = Form(...),
                       auserbgr: int = Form(...),
                       auserbu: int = Form(...),
                       ausersc: float = Form(...),
                       auserhtn: int = Form(...),
                       auserdm: int = Form(...),
                       auserappet: int = Form(...)):

    data2 = np.array([auserage, auserbp, ausersu, auserbgr, auserbu,
                      ausersc, auserhtn, auserdm, auserappet]).reshape(1, -1)
    filename = "models/Clr1.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    output = loaded_model.predict(data2)[0]

    if output == 0:
        result = "Kidney working properly."
    else:
        result = "Chronic kidney disease detected ...please follow the following steps"

    return templates.TemplateResponse('kidneypredict.html',
                                      context={"request": request, "result": result})


@app.get('/lung_cancer')
async def lung_cancer(request: Request):
    latest_news = dict()
    treat_news = dict()

    html_text = requests.get('https://www.medscape.com/index/list_1110_0').text
    soup = BeautifulSoup(html_text, 'html.parser')
    new = soup.find_all('li', class_='')
    for news in new:
        news_title = news.find('a', class_='title').text
        news_desc = news.find('span', class_='teaser').text
        latest_news[news_title] = news_desc

    html_text = requests.get(
        'https://www.medicalnewstoday.com/exercise-and-fitness').text
    soup = BeautifulSoup(html_text, 'html.parser')
    d = soup.find('ul', class_='css-1q1zlz3')
    new = d.find_all('li', class_='css-1ib8oek')
    for news in new:
        news_title = news.find('a', class_='css-1xlgwie').text
        news_desc = news.find('a', class_='css-onvglr').text
        treat_news[news_title] = news_desc
    return templates.TemplateResponse('lc.html', context={'request': request, 'latest_news': latest_news, 'treat_news': treat_news})


# @app.get('/lung_cancerf')
# async def lung_cancer(request: Request):
#     return templates.TemplateResponse('lungcancer.html', context={'request': request})


@app.post('/lung_prediction')
async def lung_check(request: Request, userage: int = Form(...), userapoll: int = Form(...), userdustall: int = Form(...), useroccuphaz: int = Form(...), usergr: int = Form(...), userob: int = Form(...), usersmoke: int = Form(...), userpsmoke: int = Form(...), userchestp: int = Form(...), usercob: int = Form(...)):

    data = np.array([userage, userapoll, userdustall, useroccuphaz, usergr,
                    userob, usersmoke, userpsmoke, userchestp, usercob]).reshape(1, -1)
    filename = 'models/Llr1.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    output = loaded_model.predict(data)[0]

    if output == 0:
        result = "Your lungs are still healthy"
    else:
        result = "Lung cancer detected"

    return templates.TemplateResponse('lungpredict.html',
                                      context={"request": request, "result": result})


# @app.get('/form')
# async def user_form(request: Request):
#     return templates.TemplateResponse('form.html', context={'request': request})


@app.post('/signup_form')
async def fill_form(request: Request, firstname: str = Form(...), lastname: str = Form(...), emailadd: str = Form(...), country: str = Form(...), phone: str = Form(...), streetadd: str = Form(...), city: str = Form(...), state: str = Form(...), zip: str = Form(...)):

    reasult = ""
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="health_care_system")
    if myconn.is_connected():
        cur = myconn.cursor()
        sql = "INSERT INTO user_tb (firstname, lastname, emailadd,country, phone, streetadd, city, state, zip) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)"

        val = (firstname, lastname, emailadd,
               country, phone, streetadd, city, state, zip)

        try:
            cur.execute(sql, val)

            myconn.commit()
            if cur.rowcount == 1:
                reasult = 1
            else:
                reasult = 0

            print(cur.rowcount, "record inserted!")
        except:
            print("Something wrong")
            myconn.rollback()
            reasult = 0

        myconn.close()
    else:

        print("Connection Problem")
        reasult = 0
    return reasult


@app.post('/login_form')
async def login_form(request: Request, emailadd: str = Form(...)):

    reasult = ""
    print(emailadd)
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="health_care_system")
    if myconn.is_connected():
        cur = myconn.cursor()

        sql = "SELECT * FROM user_tb WHERE emailadd = '%s'"
        val = (emailadd)

        try:
            cur.execute(sql % val)
            record = cur.fetchone()
            if record is not None:
                print(record[1])
                return record[1]

            else:
                return "Not found"
        except:
            print('Checking in record problem...')
        finally:
            cur.close()
            myconn.close()

    else:

        print("Connection Problem")
        reasult = 0
    return reasult


if __name__ == '__proj__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
