import time
import json
import pandas as pd
from typing import Union
import requests
from bs4 import BeautifulSoup, Comment
LEAGUES_IDS = {
    #'9': 'Premier-League',
    #'12': 'La-Liga',
    '11': 'Serie-A',
    #'20': 'Bundesliga',
    '13': 'Ligue-1',
    #'10': 'Championship',
    #'22': 'Major-League-Soccer',
    #'23': 'Eredivisie',
    #'31': 'Liga-MX',
    #'32': 'Primeira-Liga',
    #'17': 'Segunda-Division',
    #'33': '2-Bundesliga',
    #'37': 'Belgian-Pro-League',
    #'60': 'Ligue-2',
    #'21': 'Primera-Division',
    #'18': 'Serie-B'
}

METRICS_GROUPS = [
    'shooting',
    'passing',
 #  'passing_types',
 #  'gca',
 #  'defense',
 #  'possession',
]   

SEASONS = [
  #  '2017-2018',
  #  '2018-2019',
  #  '2019-2020',
  #  '2020-2021',
    '2021-2022',
  #  '2022-2023',
  #  '2023-2024'
]
def get_soup(link, headers):
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None
def get_table(soup):
    dataframes = []

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if any(f'div_stats_{metrics_group}' in comment for metrics_group in METRICS_GROUPS):
            soup_chart = BeautifulSoup(comment.string, "html.parser")
            table = soup_chart.find('table')

            if table is not None:
                df = pd.read_html(str(table))[0]
                

                player_ids = []
                for row in table.find_all('tr')[2:10]:
                    td = row.find('td', {'data-append-csv': True})
                    player_ids.append(td['data-append-csv'] if td else None)

                player_id_df = pd.DataFrame({'PlayerID': player_ids})
                df = pd.concat([df, player_id_df], axis=1)
                
                df.columns = [col[1] if isinstance(col, tuple) and len(col) >= 2 else col for col in df.columns]

                dataframes.append(df)

    if not dataframes:
        print("No data found for the specified metrics group.")
        return None

    return pd.concat(dataframes, ignore_index=True)
