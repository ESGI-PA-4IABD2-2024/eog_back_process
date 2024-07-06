import os
import json
import pandas as pd
from dotenv import load_dotenv
from api.call_api import get_today_route
from local.config import load_config, return_config
from transform.etl import etl_rer

load_dotenv()
pd.set_option('display.max_columns', None)  # Afficher toutes les colonnes d'un dataframe

if __name__ == '__main__':

    navitia_token = os.environ.get('NAVITIA_TOKEN')

    DEBUG = False

    config = load_config()
    rer_url = 'https://api.navitia.io/v1/'

    rer = "A"
    if not DEBUG:
        api_result = get_today_route(ligne=rer,
                                     url=rer_url,
                                     user=navitia_token)
    else:
        f = open("test_dataset/rer_a.txt", "r")
        api_result = f.read()
        f.close()
    # print(api_result) # DEBUGx

    data = json.loads(api_result)

    dic_circulations, gares = etl_rer(data)

    # Afficher les données
    gares.display()
    # print(f"Nombre de circulations récupérées : {len(dic_circulations)}")     # DEBUG
    for circulation in dic_circulations:
        print("\n\n")
        dic_circulations[circulation].trajet.display()

    print("DEBUG")
