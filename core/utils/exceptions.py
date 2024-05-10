class EmptyQuerySetError(Exception):
    def __init__(self, message="Queryset is empty"):
        self.message = message
        super().__init__(self.message)
