import requests
import bs4
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def word(request):
    word = request.GET.get('word', '')

    res = requests.get('https://www.dictionary.com/browse/'+word)
    res2 = requests.get('https://www.thesaurus.com/browse/'+word)
    
    meaning1 = ''
    se = []
    ae = []

    if res.status_code == 200:
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        meaning = soup.find_all('div', {'value': '1'})
        if meaning:
            meaning1 = meaning[0].getText()
        else:
            word = 'Sorry, '+ word + ' Is Not Found In Our Database'

    if res2.status_code == 200:
        soup2 = bs4.BeautifulSoup(res2.text, 'lxml')

        synonyms = soup2.find_all('a', {'class': 'css-r5sw71-ItemAnchor etbu2a31'})
        se = [b.text.strip() for b in synonyms]

        antonyms = soup2.find_all('a', {'class': 'css-lqr09m-ItemAnchor etbu2a31'})
        ae = [c.text.strip() for c in antonyms]

    results = {
        'word' : word,
        'meaning' : meaning1,
    }

    return render(request, 'word.html', {'se': se, 'ae': ae, 'results': results})
