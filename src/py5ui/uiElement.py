class UIElement:
    def __init__(self, x, y, element_type):
        self.x = x
        self.y = y
        self.type = element_type
        self.clickable = False
        if(element_type == 10001 or 10002 or 10003 or 10004):
            self.clickable = True

        pass
    def display(self): 
        pass