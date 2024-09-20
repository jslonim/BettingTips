from common import utilities
from datetime import date, timedelta

class PicksWise:

    def get_matches(self): 
        matches = []
        soup = utilities.BetUtilities.get_website_html("https://www.pickswise.com/")
        results = soup.find_all("div", class_="SelectionCard_selectionCard__BYNAO")
        for result in results:
            title = result.find("span", class_="SelectionInfo_event__petE6").text
            prediction = result.find("div", class_="SelectionInfo_outcome__1i6jL").text.replace(title,"")
            odds = result.find("span", class_="SelectionInfo_line__BIWH1").text
            confidence = result.find_all("span", class_="Icon_icon__ABM02 Icon_small__soR1e Icon_icon-filled-star__yy4AO Icon_tertiary__M_Z_t ConfidenceRating_star__Zoe3z")
            sport = result.find("span", class_="CardHeader_sportName__Gey3n").text
            match_date = result.find("div", class_="TimeDate_timeDate__HSSoH").find("span").text

            if match_date == "Today":
                match_date = date.today().strftime("%B %d, %Y")
            elif match_date == "Tomorrow":
                match_date = (date.today() + timedelta(days=1)).strftime("%B %d, %Y")
            else:
                match_date = match_date + ', '+ str(date.today().year)

            if confidence:
                star_amount = len(confidence)
                if star_amount == 1:
                    confidence = 0.40
                elif star_amount == 2:
                    confidence = 0.65
                else:
                    confidence = 0.80

            decimal_odds = utilities.BetUtilities.convert_odds(odds)
            kelly_criterion = utilities.BetUtilities.kelly_criterion(confidence, decimal_odds)


            match = {
                'title': title.replace(" v ", " vs "),
                'date': utilities.BetUtilities.convert_datetime_format(match_date),
                'prediction': prediction,
                'odds': decimal_odds,
                'confidence': confidence,
                'kelly': kelly_criterion,
                'tournament' : None,
                'sport': sport,
                'source': 'Pickwise'
            }

            if kelly_criterion and kelly_criterion > 1:
                matches.append(match)

        return matches
