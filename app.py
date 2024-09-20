
from common import utilities
from website_adapters.olbg import OLBG
from website_adapters.pickwise import PicksWise 

matches = []
matches.extend(OLBG().get_matches())
#matches.extend(PicksWise().get_matches())
matches = utilities.BetUtilities.get_unique_objects_by_title(matches)

for match in matches:
    print('')
    print(f'Title: {match['title']}')
    print(f'Date: {match['date']}')
    print(f'Sport: {match['sport']}')
    print(f'Tournament: {match['tournament']}')
    print(f'Prediction: {match['prediction']}')
    print(f'Reason: {match['reason']}')
    print(f'Odds: {match['odds']}')
    print(f'Kelly Criterion: % {match['kelly']}')   
    print(f'Source: {match['source']}')
    print('')
