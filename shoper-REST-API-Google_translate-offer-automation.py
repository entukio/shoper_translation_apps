#1. setup
import requests
login = 'login'
hslo = 'password?'

#https://github.com/uliontse/translators

import translators as ts
import translators.server as tss

#2. set shoper session
s = requests.Session()
response = s.post('https://shop.com/webapi/rest/auth', auth=(login, hslo))
print(response.status_code)
print(response.json())

result = response.json()
token = result['access_token']
s.headers.update({'Authorization': 'Bearer %s' % token})

#get list of categories
try:
    ps = s.get('https://mkowalska.art/webapi/rest/categories')
    categories = ps.json()
except requests.exceptions.ConnectionError:
    print('connection refused :(')


#get list of products
try:
    ps = s.get('https://mkowalska.art/webapi/rest/products',params={'page':'3'})
    products = ps.json()
except requests.exceptions.ConnectionError:
    print('connection refused :(')

#get product translations

response = s.get('https://mkowalska.art/webapi/rest/products/128')
resp_desc = response.json()
#Lista = resp_desc['translations']
#available_transl = Lista.keys()

#4. prepare texts to translate
pl_description = (resp_desc['translations']['pl_PL']['description']).replace(u'\xa0', u' ')
pl_s_description = (resp_desc['translations']['pl_PL']['short_description']).replace(u'\xa0', u' ')
pl_name = resp_desc['translations']['pl_PL']['name']

#5. translate function
def transl(text):
    return tss.google(text, from_language='pl', to_language='en')

#6. translated texts
en_description = transl(pl_description)
en_s_description = transl(pl_s_description)
en_name = transl(pl_name)
trans_arr = [en_name,en_s_description,en_description]

#7. approve translations
for i,el in enumerate(trans_arr):
    print(i,el)
    approve = input('approve? y/n')
    while approve not in ['y','n']:
        approve = input('approve? y/n')
    while approve == 'n':
        trans_arr[i] = input('paste correct translation')
        print('new translation:')
        print(trans_arr[i])
        approve = input('approve? y/n')
        while approve not in ['y','n']:
            approve = input('approve? y/n')
            

#8. prepare request body to add en_US translation
data = {'translations': {
'en_US': {
'name': trans_arr[0],
'short_description': trans_arr[1],
'description': trans_arr[2],
'active': 1,
'seo_title': trans_arr[0],
'seo_description': '',
'seo_keywords': '',
'order': 0,
'main_page': 0,
'main_page_order': 0
}
}}

#9. update translation
update = s.put('https://shop.com/webapi/rest/products/128',json=data)
print('status: ',update.status_code)
print('response: ',update.json())


