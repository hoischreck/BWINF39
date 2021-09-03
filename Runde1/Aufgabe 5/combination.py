#Eine Funktion, die alle Permutationen, von verschiedene Listen, mit Elementen bildet
def combination(main_list):
    main_list = [i for i in main_list if len(i) > 0]
    r = [[i] for i in main_list[0]]
    index = 1
    while 1:
        new = []
        for existing in r:
            for knot in main_list[index]:
                new.append(existing.__add__([knot]))
        r = new
        index += 1
        if index >= len(main_list):
            return r