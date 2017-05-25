from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect,render_to_response
from .forms import RegistrationForm, LoginForm, SearchForm
from django.utils import timezone
from textblob import TextBlob
import requests
import urllib
import json
from aylienapiclient import textapi
import base64

url = 'http://sentiment.vivekn.com/api/text/'
client = textapi.Client(" 356dbb8a" , " 0c4b4df8ea8140894f63d390ccc2ff1d")

# Create your views here.

"""def main_page(request):
    return render(request , 'WebApp/main_page.html' , {})"""

@csrf_exempt
def main_page(request):
    if request.method == 'POST':
        val = SearchForm(request.POST)
        if val.is_valid():
            sp = {}
            get_sentiment =  val.cleaned_data['search_query']
            #print ("Anish" + get_sentiment)
            post_data = {'txt' : get_sentiment}
            newList = []
            newList.append(get_sentiment)
            data = {}
            data['texts'] = newList
            json_data = json.dumps(data)
            response = requests.post('https://api.uclassify.com/v1/uclassify/topics/classify', \
            data = json_data, \
            headers = {'Authorization': 'Token ' + "1nw5OWHEDx06"})
            json_data = response.json()
            #print(json_data)
            categories = json_data[0]['classification']

            myList = []
            for c in categories:
                name = c['className']
                conf = c['p']
                myList.append([name , conf])

            myList.sort(key=lambda x: x[1],reverse=True)

            t = 0
            for c in myList:
                sp[t] = c[0]
                t = t + 1
                sp[t] = c[1]
                t = t + 1
                if t == 9:
                    break

            payload = {'text': get_sentiment,
                       'token': '04eea67c6ea64ac6917ffd639995ad6d', 'model': '54cf2e1c-e48a-4c14-bb96-31dc11f84eac'}
            responseD = requests.post('https://api.dandelion.eu/datatxt/cl/v1', data=payload)
            DTrespone = responseD.json()
            DTcategories = DTrespone['categories']

            myListDT = []
            for c in DTcategories:
                name = c['name']
                conf = c['score']
                myListDT.append([name , conf])

            myListDT.sort(key=lambda x: x[1],reverse=True)

            t = t + 1
            for c in myListDT:
                sp[t] = c[0]
                t = t + 1
                sp[t] = c[1]
                t = t + 1
                if t == 18:
                    break

            classifications = client.ClassifyByTaxonomy({"text": get_sentiment, "taxonomy": "iab-qag"})

            curr = t

            for category in classifications['categories']:
                sp[t] = category['label']
                t = t + 1
                sp[t] = category['score']
                t = t + 1

            now = t - curr

            return render_to_response('WebApp/main_page.html' , {'result' : sp})

    else:
        val = SearchForm()

    return render(request , 'WebApp/main_page.html' , {'value' : val})


def signup_btn(request):
    form = RegistrationForm()
    return render(request , 'WebApp/signup.html' , {'form' : form})

def login_btn(request):
    form = LoginForm()
    return render(request , 'WebApp/login.html' , {'form' : form})

def login(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            post = form.save(commit = False)
            post.username = request.user
            post.email = request.user
            post.password = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('main_page.html' , pk = post.pk)


    else:
        form = RegistrationForm()

    return render(request , 'WebApp/logout.html' , {})

def logout(request):
    return render(request , 'WebApp/logout.html' , {})