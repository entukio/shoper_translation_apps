from flask import Flask, render_template, request, url_for, flash, redirect
import requests

login = 'login'
hslo = 'haslo?'

#https://github.com/uliontse/translators
import translators as ts
import translators.server as tss

# translate function
def transl(text):
    return tss.google(text, from_language='pl', to_language='en')

translate_to = 'en_US'

#2. set shoper session
s = requests.Session()
response = s.post('https://shop.com/webapi/rest/auth', auth=(login, hslo))
result = response.json()
token = result['access_token']
s.headers.update({'Authorization': 'Bearer %s' % token})

#IMPORTANT!!! PROD ID > IT GETS ADDED +1 AFTER EVERY POST REQUEST to /submit

prod_id=124

#declaring translation variables to pass to Flask


def getProductTranslations(prod_id):
    #3a. get product translations
    response = s.get('https://shop.com/webapi/rest/products/'+str(prod_id))
    resp_desc = response.json()
    try:
        Lista = resp_desc['translations']
        available_transl = Lista.keys()
        if translate_to not in available_transl:
            #4. prepare texts to translate
            pl_description = (resp_desc['translations']['pl_PL']['description']).replace(u'\xa0', u' ')
            pl_s_description = (resp_desc['translations']['pl_PL']['short_description']).replace(u'\xa0', u' ')
            pl_name = resp_desc['translations']['pl_PL']['name']


            #5. translated texts
            en_description = transl(pl_description)
            en_s_description = transl(pl_s_description)
            en_name = transl(pl_name)

            return [0,(pl_name,pl_s_description,pl_description,en_name,en_s_description,en_description),prod_id]

        else:
            return [1,'Translation available',prod_id]
        
    except:
        return [1,'No product',prod_id]


def getTranslationResult(prod_id):
    result = getProductTranslations(prod_id)
    return result

def updateTrans(id,name,s_desc,desc):
    data = {'translations': {
        'en_US': {
        'name': name,
        'short_description': s_desc,
        'description': desc,
        'active': 1,
        'seo_title': name,
        'seo_description': '',
        'seo_keywords': '',
        'order': 0,
        'main_page': 0,
        'main_page_order': 0
        }
        }}

    #9. update translation
    update = s.put('https://shop.com/webapi/rest/products/'+str(id),json=data)
    return update.status_code

def double_check(id):
    #10. double-check
    response = s.get('https://shop.com/webapi/rest/products/'+str(id))
    resp_desc = response.json()
    Lista = resp_desc['translations']['en_US']
    return Lista



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html',translation=getTranslationResult(prod_id))

@app.route('/submit', methods = ['GET','POST'])
def submit():
    if request.method =='POST':
        name = request.form.get('name')
        s_desc = request.form.get('s_desc')
        desc = request.form.get('desc')
        global prod_id
        id = prod_id
        update_status = updateTrans(id,name,s_desc,desc)
        doubleres = double_check(id)
        flash(update_status)
        flash(doubleres)
        prod_id += 1

    return render_template('index.html',translation=getTranslationResult(prod_id))

@app.route('/skip', methods = ['GET'])
def skip():
    global prod_id
    prod_id += 1
    return render_template('index.html',translation=getTranslationResult(prod_id))

app.run(debug=True)
