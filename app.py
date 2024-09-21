from common import utilities
from website_adapters.olbg import OLBG
from website_adapters.pickwise import PicksWise 
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    website_adapters = [PicksWise(), OLBG()]  # Add more adapters as needed

    coroutines = [adapter.get_matches() for adapter in website_adapters]
    results = await asyncio.gather(*coroutines)

    # Flatten the list of lists
    matches = [match for sublist in results for match in sublist]

    matches = utilities.BetUtilities.get_unique_objects_by_title(matches)
    return matches

matches = asyncio.run(main())

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
