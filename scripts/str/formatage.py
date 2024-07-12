from typing import Union


def format_date(nb: int) -> str:
    return str(nb) if nb > 9 else ("0" + str(nb))


def format_hour(nb: int) -> str:
    nb *= 10_000
    nb = str(nb)
    if len(nb) < 6:
        nb = "0" + nb

    return nb


def datetime_to_date_hour(
    str_date: str, RETURN_VALUES: bool = False
) -> Union[tuple[int, int, int, int, int], str]:
    """
    formate les dates "20240629T180400" en "29/06/2024 18:04"
    :param str_date:
    :return:
    """
    date_half, time_half = str_date.split("T")

    year = date_half[:4]
    month = date_half[4:6]
    day = date_half[6:]

    hour = time_half[:2]
    minute = time_half[2:4]

    formated_date = f"{day}/{month}/{year} {hour}:{minute}"

    if RETURN_VALUES:
        return int(year), int(month), int(day), int(hour), int(minute)

    return formated_date


def date_rer_to_date_sql(date_str: str) -> str:
    # 20240629T180500 -> 2024-06-29 18:05:00
    d = date_str.split("T")
    date_part = d[0]
    year = date_part[:4]
    month = date_part[4:6]
    day = date_part[6:]

    hour_part = d[1]
    hour = hour_part[:2]
    minute = hour_part[2:4]
    second = '00'

    return f"{year}-{month}-{day} {hour}:{minute}:{second}"




"""
def format_json(json_data: str) -> pd.DataFrame:
    rows = []
    for route_schedule in json_data['route_schedules']:
        direction = route_schedule['display_informations']['direction']
        code = route_schedule['display_informations']['code']
        network = route_schedule['display_informations']['network']
        color = route_schedule['display_informations']['color']
        name = route_schedule['display_informations']['name']
        label = route_schedule['display_informations']['label']
        text_color = route_schedule['display_informations']['text_color']
        commercial_mode = route_schedule['display_informations']['commercial_mode']

        for header in route_schedule['table']['headers']:
            headsign = header['display_informations']['headsign']
            trip_short_name = header['display_informations']['trip_short_name']
            header_direction = header['display_informations']['direction']

            for row in route_schedule['table']['rows']:
                for date_time in row['date_times']:
                    departure_time = date_time['base_date_time']
                    arrival_time = date_time['date_time']

                    row_data = {
                        "gare_depart": direction,
                        "gare_arrivee": header_direction,
                        "heure_depart": departure_time,
                        "heure_arrivee": arrival_time
                    }
                    rows.append(row_data)

    return pd.DataFrame(rows)
"""
