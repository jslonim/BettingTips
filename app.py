import requests
from bs4 import BeautifulSoup

from common import utilities

def determine_confidence(expert_number):
    if expert_number == 1:
        return 0.65
    elif expert_number == 2:
        return 0.80
    elif expert_number > 2:
        return 1
    else:
        return None

matches = []
URL = "https://www.olbg.com/betting-tips"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div", class_="tip t-grd-1")

for result in results:
    title = result.find("div", class_= "rw evt").find("a", class_="h-rst-lnk").text
    prediction = result.find("div", class_= "rw slct").find("a", class_="h-rst-lnk").text
    experts = getattr(result.find("div", class_= "rw slct").find("p", class_="exp"), 'text', None)
    experts = utilities.BetUtilities.extract_first_number(experts) if experts else None
    odds = result.find("div", class_= "rw odds").find("span", class_="odd ui-odds")["data-decimal"]
    confidence = determine_confidence(experts) if experts else None
    kelly = utilities.BetUtilities.kelly_criterion(confidence, float(odds)) if confidence and odds else None

    match = {
        'title': title,
        'prediction': prediction,
        'experts': experts,
        'odds': odds,
        'confidence': confidence,
        'kelly': kelly
    }

    if kelly and kelly > 1:
        matches.append(match)

if matches:
    for i in range(0, len(matches)):
        print('')
        print(f'Title: {matches[i]['title']}')
        print(f'Prediction: {matches[i]['prediction']}')
        print(f'Experts: {matches[i]['experts']}')
        print(f'Odds: {matches[i]['odds']}')
        print(f'Kelly Criterion: % {matches[i]['kelly']}')   
        print('')
else:
    print("No games worth betting on")

