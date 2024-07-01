from str.formatage import datetime_to_date_hour


class Stop:
    # Node de linked list Trajet
    def __init__(self, id_circulation, name_gare, h_stop, ligne, next_gare=None):
        self.id_circulation = id_circulation
        self.name_gare = name_gare
        self.h_stop = h_stop
        self.ligne = ligne
        self.next_gare = next_gare

    def display(self):
        formated_date = datetime_to_date_hour(self.h_stop)
        print(f"Arrêt à {self.name_gare}: {formated_date} sur la ligne {self.ligne}")

    def display_all(self):
        self.display()
        if self.next_gare is not None:
            self.next_gare.display_all()


class Trajet:
     # Linked List de Stops (= quais)
    def __init__(self):
        self.head = None

    def append(self, id_circulation, name_gare, h_stop, ligne):
        new_stop = Stop(id_circulation, name_gare, h_stop, ligne)
        if not self.head:
            self.head = new_stop
        else:
            current = self.head
            while current.next_gare:
                current = current.next_gare
            current.next_gare = new_stop

    def display(self):
        self.head.display_all()


class Circulation:
    def __init__(self, id_circulation, circulation_type, quai, name_train):
        self.id_circulation = id_circulation
        self.circulation_type = circulation_type
        self.quai = quai
        self.name_train = name_train
        self.trajet = Trajet()


class Gares_parcoures:
    def __init__(self):
        self.set_gares = set()

    def add_gare(self, name_gare):
        self.set_gares.add(name_gare)

    def display(self):
        for gare_name in self.set_gares:
            print(gare_name)
