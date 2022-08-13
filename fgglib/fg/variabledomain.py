class VariableDomain:
    '''
    Class that represents the domain of possible values that a
    variable in a factor graph can assume.
    '''
    

    def __init__(self, infinite):
        '''
        Creates a new domain object.
        
        Args:
            infinite (bool): specifies if the domain is infinite or not
            
        Returns:
            VariableDomain: the created VariableDomain object
        '''
        
        self.infinite = infinite
        self.content = set()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Domain: "+str(self.infinite)+", "+str(self.content)

    def set_content(self, content):
        '''
        Sets the content of the domain, i.e. the values contained in it.
        
        Args:
            content (set): set containing the values
        
        Returns:
            None
            
        Raises:
            Exception: if the domain is infinite, because infinite domains
                do not have the content explicitly represented
        '''
        
        if(self.infinite):
            raise Exception("Cannot set content, domain is infinite!")
        self.content = content

    def enumerate(self) -> set:
        '''
        Enumerates the values contained in the domain.
        
        Returns:
            set: a set containing the values
            
        Raises:
            Exception: if the domain is infinite, because infinite domains
                do not have the content explicitly represented
        '''
        
        if(self.infinite):
            raise Exception("Cannot enumerate content, domain is infinite!")
        for c in self.content:
            yield c
