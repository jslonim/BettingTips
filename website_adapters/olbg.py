
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
    
class OLBG:
    
    SPORT_ICON_DICT = {
        "i-sp-4": "Basketball",
        "i-sp-1": "Soccer",
        "i-sp-3": "Tennis",
        "i-sp-7": "Cricket",
        "i-sp-16": "Boxing",
        "i-sp-11": "Football",
        "i-sp-21": "Volleyball",
        "i-sp-8": "Snooker"
    }
    
    def get_matches(self): 
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
            tournament  = result.find("p", class_= "league")
            tournament = getattr(tournament.find("span", class_="h-ellipsis"),'text', None) if tournament else None
            sport_class = result.find("div", class_= "rw sprt").find("i")["class"][0]
            sport = None
            if 'i-sp-' in sport_class:
                sport = self.SPORT_ICON_DICT.get(sport_class)

            match = {
                'title': title,
                'prediction': prediction,
                'experts': experts,
                'odds': odds,
                'confidence': confidence,
                'kelly': kelly,
                'tournament' : tournament,
                'sport': sport
            }

            if kelly and kelly > 1:
                matches.append(match)

        return matches
