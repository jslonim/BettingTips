
from website_adapters.olbg import OLBG
olbg = OLBG().get_matches()

if olbg:
    for i in range(0, len(olbg)):
        print('')
        print(f'Title: {olbg[i]['title']}')
        print(f'Sport: {olbg[i]['sport']}')
        print(f'Tournament: {olbg[i]['tournament']}')
        print(f'Prediction: {olbg[i]['prediction']}')
        print(f'Experts: {olbg[i]['experts']}')
        print(f'Odds: {olbg[i]['odds']}')
        print(f'Kelly Criterion: % {olbg[i]['kelly']}')   
        print('')
else:
    print("No games worth betting on")

