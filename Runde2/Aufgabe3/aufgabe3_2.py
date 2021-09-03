import os
import numpy as np
import time, sys, math
from multiprocessing import Pool
#Löschen, falls nicht benötigt

def Timer(func):
    def inner():
        s = time.time()
        r = func()
        return r, time.time()-s
    return inner

def num_prettyfier(num):
    num = str(num)
    if "." in num:
        decimal, num = num.split(".")[1], list(num)
        del num[num.index("."):]
        decimal = list(decimal)
        decimal.insert(0,".")
    else:
        num, decimal = list(num), []
    position,c  = len(num), 0
    for i in num[::-1]:
        position -= 1
        c += 1
        if c == 3:
            c = 0
            num.insert(position, "'")
    num += decimal
    if num[0] == "'":
        del num[0]
    elif num[0] == "-" and num[1] == "'":
        del num[1]
    return "".join(num)


class See():
    def __init__(self, circumference, address_amount, addresses, ice_parlor_amount=3):
        self.circumference = int(circumference)
        self.address_amount = int(address_amount)
        self.addresses2 = np.array([int(i) for i in addresses])
        self.iceParlorAmount = ice_parlor_amount

    def possible_positions(self, Knot_amount):
        #Sollte möglichst schnell sein, da viele 10mio-Möglichkeiten berechnet werden
        #n über k Möglichkeiten
        #bzw. self.circumference über Knot_amount Möglichkeiten
        s = time.time()
        if Knot_amount < 1:
            return []
        possible_knots = range(self.circumference)
        combinations = [[i] for i in possible_knots]
        for _ in range(Knot_amount-1):
            new = []
            for starting_knot in combinations:
                for value in [i for i in possible_knots if i > starting_knot[-1]]:
                    new.append(starting_knot + [value])
            combinations = new
        print("Kombinationen berechnet")
        print("")
        print(f"Pos(): {time.time() - s}s")
        return combinations
        #Noch nicht optimiert

    #does stuff
    def run(self):
        print("Anzahl der Positionskombinationen: ", num_prettyfier(self._expected_combinations(self.iceParlorAmount)))
        pos = self.possible_positions(self.iceParlorAmount)


        print(pos)


        return pos


    def distance2(self, v1, v2):
        distance1 = abs(v1-v2)
        distance2 = self.circumference-distance1
        if distance1 >= distance2:
            return distance2, distance1
        else:
            return distance1, distance2


    def factorial(self, n):
        return n if n <= 1 else n * self.factorial(n-1)
    def _expected_combinations(self, knot_amount):
        return int(self.factorial(self.circumference+1)/(self.factorial(self.circumference+1-knot_amount)*self.factorial(knot_amount))) if knot_amount > 0 else 0



if __name__ == "__main__":
    # Verzeichnis der Beispiele.
    e_dir = "Beispiele"
    # Auflistung der Beispiel-Datein.
    examples = os.listdir(e_dir)

    # Jedes Beispiel, in 'examples'...
    for e in examples:
    #... wird geöffnet und gelesen.
        print(f"[---Die Ergebnisse für '{e}'---]")
        with open(os.path.join(e_dir, e), "r", encoding="utf8") as f:
            data = f.readlines()
            See(*data[0].strip().split(), data[1].strip().split(), ice_parlor_amount=3).run()
            quit()


