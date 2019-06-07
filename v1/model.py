import random
from v1 import cnx
from pymongo import MongoClient


class Car:
    def __init__(self, *args,**kwargs):

        if len(args) > 0:
            kwargs=args[0]

        for key in kwargs:
            self.__setattr__(key,kwargs[key])

        if 'price' in kwargs.keys():
            self.price = kwargs['price']
            self.price_1 = kwargs['price']
            self.price_2 = kwargs['price']
            self.price_3 = kwargs['price']
            self.price_4 = kwargs['price']
            self.price_5 = kwargs['price']
            self.price_6 = kwargs['price']
            self.price_7 = kwargs['price']
            self.price_8 = kwargs['price']
            self.price_9 = kwargs['price']
            self.price_10 = kwargs['price']
            self.price_11 = kwargs['price']
            self.price_12 = kwargs['price']
            self.price_13 = kwargs['price']
            self.price_14 = kwargs['price']
            self.price_15 = kwargs['price']
            self.price_16 = kwargs['price']
            self.price_17 = kwargs['price']
            self.price_18 = kwargs['price']
            self.price_19 = kwargs['price']
            self.price_20 = kwargs['price']


    def to_dict(self):
        return {"index":self.index,"make": self.make, "model": self.model,
                "price": self.price,
                "price_1": self.price,
                "price_2": self.price,
                "price_3": self.price,
                "price_4": self.price,
                "price_5": self.price,
                "price_6": self.price,
                "price_7": self.price,
                "price_8": self.price,
                "price_9": self.price,
                "price_10": self.price,
                "price_11": self.price,
                "price_12": self.price,
                "price_13": self.price,
                "price_14": self.price,
                "price_15": self.price,
                "price_16": self.price,
                "price_17": self.price,
                "price_18": self.price,
                "price_19": self.price,
                "price_20": self.price,
                }

    def write(self, db):
        data = self.to_dict()
        db.insert_one(data)


if __name__ == '__main__':
    sample_size = 1000 * 1000

    makes = {
        'Toyota': ['Celica', 'Camry', 'Aygo'],
        'Renault': ['Scenic', 'Espace', 'R4', 'R16'],
        'Peugeot': ['404', '5008', '504']
    }
    client = MongoClient(cnx.URI)
    db = client.test1.cars

    cars = []
    for i in range(sample_size):
        print(i)
        make = random.choice(list(makes.keys()))
        model = random.choice(makes[make])
        price = 10000 + random.random() * 10000
        car = Car(index=i,make=make, model=model, price=price)
        car.write(db)
