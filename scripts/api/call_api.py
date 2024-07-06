import requests

from datetime import datetime, timedelta
from scripts.str.formatage import format_hour, format_date


def get_today_route(ligne: str,
                    url: str,
                    user: str,
                    pwd: str):
    """
    Récupèrer toutes les circulations déjà disponibles, pour une ligne donnée, dans les prochaines 24 heures.
    :param url: URL de l'API
    :param user: User de connexion
    :param pwd: Mot de passe de connexion
    :param ligne: Nom de la ligne à récupérer (ex : "C" pour le RER C)
    :return: Contenu de l'API
    """
    ligne = ligne.upper()

    query = f"coverage/sncf/lines/line:SNCF:{ligne}/route_schedules"
    api_content = requests.get(url + query,
                               auth=(user, pwd))

    if api_content.status_code == 200:
        api_content.encoding = 'utf-8'
        return api_content.text

    print("Erreur : connexion API")
    return None



def get_monthly_route(ligne: str,
                      url: str,
                      user: str,
                      pwd: str,
                      start_datetime,
                      end_datetime):
    #/!\ NE MARCHE PAS ENCORE ! PROBLEME AVEC LE FILTRE DE DATE
    ligne = ligne.upper()

    today_date = datetime.now()
    today_year = str(today_date.year)
    today_month = format_date(today_date.month)
    today_day = format_date(today_date.day)
    today_str = today_year + today_month + today_day

    tomorrow_date = today_date + timedelta(1)
    tomorow_year = str(tomorrow_date.year)
    tomorow_month = format_date(tomorrow_date.month)
    tomorow_day = format_date(tomorrow_date.day)
    tomorow_str = tomorow_year + tomorow_month + tomorow_day

    start_h = format_hour(start_datetime)
    end_h = format_hour(end_datetime)

    # TODO : corriger les heures limites
    query = f"coverage/sncf/lines/line:SNCF:{ligne}/route_schedules//?since%3D={today_str}T{start_h}&until={tomorow_str}T{end_h}&"
    api_content = requests.get(url + query,
                               auth=(user, pwd))

    if api_content.status_code == 200:
        return api_content.text

    print("Erreur : connexion API")
    return None
