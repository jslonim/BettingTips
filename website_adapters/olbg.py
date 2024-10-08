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
        "i-sp-8": "Snooker",
        "i-sp-5": "Golf",
        "i-sp-17": "Cycling",
        "i-sp-14": "Racing",
        "i-sp-15": "Darts",
        "i-sp-9": "College Football",
        "i-sp-13": "Skating",
        "i-sp-12": "Baseball"    
    }
    
    async def get_matches(self): 
        matches = []
        soup = utilities.BetUtilities.get_website_html("https://www.olbg.com/betting-tips")

        results = soup.find_all("div", class_="tip t-grd-1")

        for result in results:
            title = result.find("div", class_= "rw evt").find("a", class_="h-rst-lnk").text.replace(" v ", " vs ")
            prediction = result.find("div", class_= "rw slct").find("a", class_="h-rst-lnk").text
            experts = getattr(result.find("div", class_= "rw slct").find("p", class_="exp"), 'text', None)
            experts = utilities.BetUtilities.extract_first_number(experts) if experts else None
            odds = result.find("div", class_= "rw odds").find("span", class_="odd ui-odds")["data-decimal"]
            confidence = determine_confidence(experts) if experts else None
            kelly_criterion = utilities.BetUtilities.kelly_criterion(confidence, float(odds)) if confidence and odds else None
            tournament  = result.find("p", class_= "league")
            tournament = getattr(tournament.find("span", class_="h-ellipsis"),'text', None) if tournament else None
            date =  utilities.BetUtilities.convert_datetime_format(result.find(class_="h-date")["datetime"])
            sport_class = result.find("div", class_= "rw sprt").find("i")["class"][0]
            sport = None
            if 'i-sp-' in sport_class:
                sport = self.SPORT_ICON_DICT.get(sport_class)
            
            reason = None
            reason_link = result.find("a", class_="h-rst-lnk")
            reason_link_url = reason_link["href"] if reason_link else None
            if reason_link_url:
                match_website = utilities.BetUtilities.get_website_html('https://www.olbg.com/' + reason_link_url)
                reason_section = match_website.find("div", class_="l-col-2 top-tips")
                if reason_section:
                    reason = reason_section.find("p", class_="rw h-readable").string

            match = {
                'title': title,
                'date': date,
                'prediction': prediction,
                'odds': odds,
                'reason': reason,
                'confidence': confidence,
                'kelly': kelly_criterion,
                'tournament' : tournament,
                'sport': sport,
                'source': 'OLBG'
            }

            if kelly_criterion and kelly_criterion > 1:
                matches.append(match)

        return matches
