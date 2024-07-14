import json
from datetime import datetime
from datetime import timedelta
from typing import Any

import requests
from str.formatage import format_date
from str.formatage import format_hour


def get_today_route(ligne: str, url: str, user: str):
    """
    Récupèrer toutes les circulations déjà disponibles, pour une ligne donnée,
    dans les prochaines 24 heures.
    :param url: URL de l'API
    :param user: User de connexion
    :param pwd: Mot de passe de connexion
    :param ligne: Nom de la ligne à récupérer (ex : "C" pour le RER C)
    :return: Contenu de l'API
    """
    ligne = ligne.upper()

    query = f"coverage/sncf/lines/line:SNCF:{ligne}/route_schedules"
    try:
        api_content = requests.get(url + query, auth=(user, ""))

        if api_content.status_code == 200:
            api_content.encoding = "utf-8"
            return api_content.text

        print(
            f"Erreur : une erreur est renvoyée par l'API ; code erreur : {api_content.status_code}"
        )

    except KeyError:
        print("Erreur : impossible de joindre l'API ")
        return None


def get_monthly_route(ligne: str, url: str, user: str, start_datetime, end_datetime):
    # /!\ NE MARCHE PAS ENCORE ! PROBLEME AVEC LE FILTRE DE DATE
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
    query = (
        f"coverage/sncf/lines/line:SNCF:{ligne}/route_schedules//?since%3D={today_str}T{start_h}"
        f"&until={tomorow_str}T{end_h}&"
    )
    api_content = requests.get(url + query, auth=user)

    if api_content.status_code == 200:
        return api_content.text

    print("Erreur : connexion API")
    return None


def get_hourly_route(ligne: str, token: str) -> Any | None:
    with open("./api/correspondances_lignes.json", "r") as f:
        correspondance_dict = json.load(f)

    line = correspondance_dict[ligne]
    query = f"https://prim.iledefrance-mobilites.fr/marketplace/estimated-timetable?LineRef={line}"
    headers = {"Accept": "application/json", "apikey": token}
    api_content = requests.get(query, headers=headers)
    print("Status:", api_content)
    if api_content.status_code == 200:
        api_content.encoding = "utf-8"
        return api_content.text
    print("Erreur : connexion API")
    print(f"{query}")
    return None


def get_stop_point_name(stop_point_id: str) -> Any | None:
    with open("./api/correspondances_arrets.json", "r") as f:
        correspondance_dict = json.load(f)
    try:
        nom_arret = correspondance_dict[stop_point_id]
        return nom_arret
    except KeyError:
        raise ValueError(
            f"L'identifiant '{stop_point_id}' n'est pas présent dans correspondances_arrets.json"
        )


def get_departure_from_arrival(arrival: str, direction: str) -> Any | None:
    with open("./api/lines_order.json", "r") as f:
        lines_dict = json.load(f)
    try:
        departure = "Unknown"
        for line in lines_dict:
            if arrival == line["arrival_id"] and direction == line["destination_name"]:
                departure = line["depart_id"]
        return departure
    except KeyError:
        raise ValueError(f"L'identifiant '{arrival}' n'est pas présent dans lines_order.json")


def get_line_short_name(stop_point_id: str) -> Any | None:
    with open("./api/lines_short_name.json", "r") as f:
        correspondance_dict = json.load(f)
    try:
        nom_arret = correspondance_dict[stop_point_id]
        return nom_arret
    except KeyError:
        raise ValueError(
            f"L'identifiant '{stop_point_id}' n'est pas présent dans lines_short_name.json"
        )
