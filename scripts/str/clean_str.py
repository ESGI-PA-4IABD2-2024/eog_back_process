CORRECTION = {
    # RER A
    "La Grande Arche de la Défense": "La Défense",
    "Neuilly-Plaisance - Noctilien": "Neuilly-Plaisance",
    "Noisy-le-Grand Champs": "Noisi-Champs",
    "La Varenne Saint-Hilaire - Chennevières-sur-Marne": "La Varenne Chennevières",
    "Sucy-en-Brie - Bonneuil-sur-Marne": "Sucy-Bonneuil",
    "Saint-Maur-des-Fossés - Créteil": "Saint-Maur - Créteil",
}


def clean_gareName(set_gares: set):
    for gare in set_gares:
        if gare in CORRECTION:
            set_gares.remove(gare)
            set_gares.add(CORRECTION[gare])

    return set_gares
