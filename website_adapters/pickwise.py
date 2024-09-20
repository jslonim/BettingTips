from common import utilities
from datetime import date, timedelta

class PicksWise:

    async def get_matches(self): 
        matches = []
        soup = utilities.BetUtilities.get_website_html("https://www.pickswise.com/")
        results = soup.find_all("div", class_="SelectionCard_selectionCard__BYNAO")
        for result in results:
            title = result.find("span", class_="SelectionInfo_event__petE6").text
            prediction = result.find("div", class_="SelectionInfo_outcome__1i6jL").text.replace(title,"")
            prediction = utilities.BetUtilities.remove_text_within_parentheses(prediction)
            odds = result.find("span", class_="SelectionInfo_line__BIWH1").text
            confidence = result.find_all("span", class_="Icon_icon__ABM02 Icon_small__soR1e Icon_icon-filled-star__yy4AO Icon_tertiary__M_Z_t ConfidenceRating_star__Zoe3z")
            sport = result.find("span", class_="CardHeader_sportName__Gey3n").text
            match_date_original = result.find("div", class_="TimeDate_timeDate__HSSoH").find("span").text

            if match_date_original == "Today":
                match_date = date.today().strftime("%B %d, %Y")
            elif match_date_original == "Tomorrow":
                match_date = (date.today() + timedelta(days=1)).strftime("%B %d, %Y")
            else:
                match_date = match_date_original + ', '+ str(date.today().year)

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

            reason = None
            reason_link = result.find("a", class_="Link_link__eOhkI SelectionInfo_selectionInfo__eQ5_8 SelectionCard_info__fEuab")
            reason_link_url = reason_link["href"] if reason_link else None
            
            if reason_link_url:
                match_website = utilities.BetUtilities.get_website_html('https://www.pickswise.com/' + reason_link_url)
                reason_matches = []
                for match in match_website.findAll("div", class_="SelectionCard_selectionCard__BYNAO"):
                    if match is None:
                        continue

                    reason_match_title = match.find("span", class_="SelectionInfo_event__petE6").text        
                    reason_match_date = match.find("div", class_="TimeDate_timeDate__HSSoH CardHeader_title__6fV7_").find("span").text
                    if reason_match_title == title and reason_match_date == match_date_original:
                        reason_matches.append(match)
                                  
                if len(reason_matches) == 1:
                    reason = reason_matches[0].find("div",class_="Html_wysiwyg__3F4LI").find_all("p")[0].text


            match_info = {
                'title': title.replace(" v ", " vs "),
                'date': utilities.BetUtilities.convert_datetime_format(match_date),
                'reason': reason,
                'prediction': prediction,
                'odds': decimal_odds,
                'confidence': confidence,
                'kelly': kelly_criterion,
                'tournament' : None,
                'sport': sport,
                'source': 'Pickwise'
            }

            if kelly_criterion and kelly_criterion > 1:
                matches.append(match_info)

        return matches
