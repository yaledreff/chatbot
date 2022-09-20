class BookingDetails:
    def __init__(
        self,
        origine: str = None,
        destination: str = None,
        aller: str = None,
        retour: str = None,
        budget: str = None
    ):

        self.destination = destination
        self.origine = origine
        self.aller = aller
        self.retour = retour
        self.budget = budget