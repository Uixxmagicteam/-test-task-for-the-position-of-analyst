class Car():

    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.metr = 0

    def desc(self):
        desc = str(self.year) + self.model + self.brand
        return desc.title()

    def upd(self):
        if self.brand == "bmx":
            self.metr = 30

newcar = Car("bmx", "x6", 1994)

newcar.upd()
print(newcar.desc())
print(newcar.metr)

