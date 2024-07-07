from scripts.item.objets import Circulation
from scripts.item.objets import Gares_parcoures


def etl_rer(data):
    dic_circulations = {}
    gares = Gares_parcoures()

    # Traiter les données pour créer les objets Circulation, Trajet et Stop
    for route_schedule in data["route_schedules"]:
        display_info = route_schedule["display_informations"]
        circulation_type = display_info["commercial_mode"]
        quai = display_info["label"]

        for circulations in route_schedule["table"]["headers"]:
            id_circulation = circulations["links"][0]["id"]
            name_train = circulations["display_informations"]["headsign"]

            if id_circulation not in circulations:
                dic_circulations[id_circulation] = Circulation(
                    id_circulation, circulation_type, quai, name_train
                )

            for row in route_schedule["table"]["rows"]:
                name_gare = row["stop_point"]["name"]
                gares.add_gare(name_gare)

                for dt in row["date_times"]:
                    if (
                        dt["links"] != [] and dt["links"][0]["id"] == id_circulation
                    ):  # Vérifier que l'arrêt correspond à la circulation en cours
                        h_stop = dt["date_time"]

                        if h_stop != "":
                            dic_circulations[id_circulation].trajet.append(
                                id_circulation, name_gare, h_stop, quai
                            )
                            # dic_circulations[id_circulation].trajet.display()  # DEBUG
                            # print("---------------\n")

    return dic_circulations, gares
