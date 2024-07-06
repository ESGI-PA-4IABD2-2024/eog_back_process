import json
import pandas as pd

from api.call_api import get_today_route
from local.config import load_config, return_config
from transform.etl import etl_rer

pd.set_option('display.max_columns', None)      # Afficher toutes les colonnes d'un dataframe



if __name__ == '__main__':
    DEBUG = False

    config = load_config()
    rer_url, rer_user, rer_pwd, metro_url, metro_user, metro_pwd = return_config(config)

    rer = "A"   # TODO : Définir ce paramètre dans un fichier ou en appel du code
    if not DEBUG:
        api_result = get_today_route(ligne=rer,
                                     url=rer_url,
                                     user=rer_user,
                                     pwd=rer_pwd)
    else:
        f = open("test_dataset/rer_a.txt", "r")
        api_result = f.read()
        f.close()
    # print(api_result) # DEBUG

    data = json.loads(api_result)

    dic_circulations, gares = etl_rer(data)

    # Afficher les données
    gares.display()
    # print(f"Nombre de circulations récupérées : {len(dic_circulations)}")     # DEBUG
    for circulation in dic_circulations:
        print("\n\n")
        dic_circulations[circulation].trajet.display()

    print("DEBUG")
