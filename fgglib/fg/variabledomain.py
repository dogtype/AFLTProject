class VariableDomain:

    def __init__(self, infinite):
        self.infinite = infinite
        self.content = set()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Domain: "+str(self.infinite)+", "+str(self.content)

    def set_content(self, content):
        if(self.infinite):
            raise Exception("Cannot set content, domain is infinite!")
        self.content = content

    def enumerate(self) -> set:
        for c in self.content:
            yield c
