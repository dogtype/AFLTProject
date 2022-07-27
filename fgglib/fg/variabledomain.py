class VariableDomain:

    def __init__(self,infinite):
        self.infinite = infinite

    def set_content():
        if self.infinite:
            raise Exception("Cannot set content, domain is infinite!")

    def enumerate() -> set:
        for c in self.content:
            yield c
