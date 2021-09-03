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

        self.score_dict = {}

    def distance_score(self, distances):
        return sum([i[0] for i in distances])

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

    def compare_test(self, pos):
        distance_compare = {}
        for positions in pos:
            distance = []
            for address in self.addresses2:
                distance.append(min([self.distance2(p, address)[0] for p in positions]))
            distance_compare[tuple(positions)] = sum(distance)
        return distance_compare

    def compare(self, pos):
        s = time.time()

        # p_amount = 22
        #
        # chunks = math.ceil(len(pos) / p_amount)
        # pos = [pos[chunks * i:chunks * (i + 1)] for i in range(len(pos[::chunks]))]
        #
        # with Pool(p_amount) as p:
        #     r = p.map(self.compare_test, pos)
        # dict = r[0]
        # for i in r[1:]:
        #     dict = {**dict, **i}

        d = self.compare_test(pos)

        print(f"Vergleich: {time.time() - s}s")

        return self.sort_results(d)
        # Sorting selbst benötigt viel Zeit

    def prove2(self, pos):
        s = time.time()
        print("------------- PROVE : 2 -------------")
        data = set()
        for c, possible_starting_pos in enumerate(pos):
            best_position, current = possible_starting_pos, None
            while best_position != None:
                current = best_position
                best_position = self.no_better_exists(best_position, pos)
                print(f"\r Checked: {round((c+1)*100/len(pos) , 2)}%", end=" ")
                #No Failsave
            data.add(str(current))
        print("\nData: ", data)
        print(f"Zeit: {round(time.time() - s, 4)}s")
        print("-------------------------------------")


    def prove(self, pos):
        s = time.time()
        max = len(pos)**2
        print("------------- PROVE : 1 -------------")
        print("Zu Berechnen: ", num_prettyfier(max))
        print("--Expected--")
        data = []
        c = 0

        for p in pos:
            c += 1
            r = self.no_better_exists(p, pos)
            #print(p, r)
            if r == None:
                data.append(p)
            print(f"\rChecked: {num_prettyfier(c*len(pos))} ({round(c*len(pos)*100/max, 2)}%) [Found: {len(data)}]", end=" ")

        print("\nData: ", data)
        print(f"Zeit: {round(time.time()-s, 4)}s")
        print("")
        return data
    def no_better_exists(self, position, all_positions):
        for position_ in all_positions:
            if position != position_:
                comparision = self.compare_positions(position, position_)
                if comparision != position:
                    return position_
        return None
    def compare_positions(self, p_main, p_tested):
        main_score = self.return_score_list(p_main)
        test_score = self.return_score_list(p_tested)
        r = self.compare_score_lists(main_score, test_score)
        if r == main_score:
            return p_main
        else:
            return p_tested
    def compare_score_lists(self, main_score, test_score):
        yes = 0
        for m, t in zip(main_score, test_score):
            if t < m:
                yes += 1
            else:
                yes -= 1
        if yes > 0:
            return test_score
        else:
            return main_score
    def return_score_list(self, pos):
        return self.score_dict[tuple(pos)]
    def create_score_list(self, positions):
        for pos in positions:
            self.score_dict[tuple(pos)] = [min(self.all_distances_to_parlors(a, pos)) for a in self.addresses2]
    def all_distances_to_parlors(self, address, parlor_positions):
        return [self.distance2(address, p)[0] for p in parlor_positions]

    def amount_of_nearest(self, pos):
        nearest = [[i,0] for i in pos]
        distances = []
        for a in self.addresses2:
            distances.append(self.all_distances_to_parlors(a, pos))
        for d in distances:
            _, index = self.smallest_with_index(d)
            nearest[index][1] += 1
        return nearest

    def smallest_with_index(self, iterable):
        i, smallest = 0, iterable[0]
        for c, j in enumerate(iterable):
            if j < smallest:
                smallest = j
                i = c
        return smallest, i

    def prove4(self, positions):
        s = time.time()
        max = len(positions) ** 2
        print("------------- PROVE : 4 -------------")
        print("Zu Berechnen: ", num_prettyfier(max))
        print("--Expected--")


        self.arrangements, data = {}, []
        for p in positions:
            a = tuple([i[1] for i in self.amount_of_nearest(p)])
            if a in self.arrangements:
                self.arrangements[a].append(p)
            else:
                self.arrangements[a] = [p]
        possible, new_pos = [], []
        for a in self.arrangements:
            if self.unbeatable(a):
                possible.append(a)
        for i in possible:
            new_pos += self.arrangements[i]

        c = 0
        new_max = len(new_pos) ** 2
        l_new_pos = len(new_pos)
        print("Max: ", num_prettyfier(max), num_prettyfier(new_max), f"({round(new_max / max, 5)})")
        print("Length: ", num_prettyfier(len(positions)), num_prettyfier(len(new_pos)), f"({round(len(new_pos)/len(positions), 5)})")
        print()

        for p in new_pos:
            c += 1
            r = self.no_better_exists(p, positions)
            if r == None:
                data.append(p)
            print(f"\rChecked: {num_prettyfier(c * l_new_pos)} ({round(c * l_new_pos * 100 / new_max, 2)}%) [Found: {len(data)}]",end=" ")

        print("\nData: ", data)
        print(f"Zeit: {round(time.time() - s, 4)}s")
        print("")

        return data
    def unbeatable(self, arrangement):
        min_difference = int(self.address_amount/2+1)
        for a in self.arrangements:
            if a != arrangement:
                d = 0
                for i, j in zip(arrangement, a):
                    d += abs(i-j)
                if int(d/2) >= min_difference:
                    return 0
        return 1






    def sort_results(self, data):
        s = time.time()
        r = sorted(data.items(), key=lambda x: x[1])
        print(f"Sortierzeit: {time.time() - s}s")
        return r

    #does stuff
    def run(self):
        print("Anzahl der Positionskombinationen: ", num_prettyfier(self._expected_combinations(self.iceParlorAmount)))
        pos = self.possible_positions(self.iceParlorAmount)
        self.create_score_list(pos)
        print("Score dictionary created\n")

        #pd = self.prove(pos)
        # for i in pd:
        #     print("Distances: ", self.amount_of_nearest(i))
        # print()
        #self.prove2(pos)


        pd2 = self.prove4(pos)

        # print(sorted(pd) == sorted(pd2))


        #quit()

        # data = self.compare(pos)
        # print(data)
        # quit()
        # totalD = data[0][1]
        # possible_positions = []
        # for i in data:
        #     if i[1] == totalD:
        #        possible_positions.append(i[0])
        #     else:
        #         break
        #
        # print(possible_positions, ":" ,totalD)
        # print("")
        # return None

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


