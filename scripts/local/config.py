import json


def load_config():
    with open("./local/config.json") as config_file:
        file_content = json.load(config_file)

        return file_content


def return_config(config):
    rer_config = config["RER"]
    rer_url = rer_config["URL"]
    rer_user = rer_config["TOKEN"]
    rer_pwd = rer_config["PWD"]

    metro_config = config["METRO"]
    metro_url = metro_config["URL"]
    metro_user = metro_config["TOKEN"]
    metro_pwd = metro_config["PWD"]

    # TODO : rajouter config de la BDD

    return rer_url, rer_user, rer_pwd, metro_url, metro_user, metro_pwd
