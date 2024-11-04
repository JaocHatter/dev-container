class Perro:
    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return "Nombre del Perro: %r" % self.name
    
dog = Perro("pancho")
print(dog)