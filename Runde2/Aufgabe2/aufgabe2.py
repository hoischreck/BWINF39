# Lösung für Aufgabe2
import os, timeit


def absPathsFromDir(dirname):
    absPath = os.path.abspath(dirname)
    for _, _, fileNames in os.walk(dirname):
        for f in fileNames:
            yield os.path.join(absPath, f)

def timeRuntime(method):
    def inner(object, stopTime=True, **kwargs):
        if stopTime:
            start = timeit.default_timer()
            return method(object, **kwargs), timeit.default_timer() - start
        else:
            return method(object, **kwargs), None

    return inner

def enumerateStep(iterable, stepSize, stepStart=0):
    i = iterable.__iter__()
    while 1:
        try:
            yield stepStart, next(i)
            stepStart += stepSize
        except StopIteration:
            break

def quicksort(iterable):
    return sorted(iterable)

def binarySearch(iterable, element):
    return element in iterable

def firstNonDupe(*iterables):
    iter = iterables[0]
    # uSet = [set(i) for i in iterables[1:]]

    uSet = intersectionOfOrderedIterables(*iterables[1:])

    for i in iter:
        if i not in uSet:
            return i
    return None

def firstDupe(*iterables):
    iter = iterables[0]
    uSet = [set(i) for i in iterables[1:]]
    for i in iter:
        if all([(i in s) for s in uSet]):
            return i
    return None


def intersectionOfOrderedIterables(*iterables):
    if len(iterables) == 0:
        return set()
    elif len(iterables) == 1:
        return set(iterables[0])

    intersection = set()
    iterableSets = [set(iterable) for iterable in iterables[1:]]
    for item in iterables[0]:
        if all([(item in s) for s in iterableSets]):
            intersection.add(item)
    return intersection


def treeCombinations(stop, start=1, min_length=1, sort_key=lambda x: len(x), reverse=False):
    combinations = []
    for i in range(start, stop + 1):
        new = [[i]]
        for n in range(i + 1, stop + 1):
            new2 = []
            for j in new:
                new2.append(j + [n])
            new += new2
        combinations += new
    return [i for i in sorted(combinations, key=sort_key, reverse=reverse) if len(i) >= min_length]


class PikeProblem:
    def __init__(self, fruitAmount, desiredCombination, pikeAmount, inputData):
        self.fruitAmount = int(fruitAmount)
        self.desiredCombination = desiredCombination
        self.pikeAmount = int(pikeAmount)
        # Daten vorsortieren?
        self.data = [(quicksort(map(int, inputData[i].split())), inputData[i + 1].split()) for i in range(0, len(inputData), 2)]
        self.associations = {}
        self.mentioned = {j for i in self.data for j in i[0]}

    @timeRuntime
    def solve(self, formatOutput=False):

        self.findIntersections()
        self.calculateRemainingProbabilities()
        self.addNotMentioned()

        if formatOutput:
            self.__formatOutput()
        else:
            return self.associations

    def findIntersections(self):
        comparableIndexes = treeCombinations(self.pikeAmount - 1, start=0, min_length=1, reverse=True)
        while 1:
            foundIntersection = False
            for combination in comparableIndexes:

                lists = self.listsByIndexes(combination)

                values = [l[0] for l in lists]

                intersections = intersectionOfOrderedIterables(*values)

                if len(intersections) == 1:
                    num = list(intersections)[0]
                    fruit = firstDupe(*[l[1] for l in lists])
                    self.addAssociation(num, fruit)
                    foundIntersection = True
                    break
                elif any([len(v) - 1 == len(intersections) for v in values]):
                    for i, l in enumerate(lists):
                        if len(l[0]) - 1 == len(intersections):
                            num = firstNonDupe(l[0], intersections)
                            fruit = firstNonDupe(l[1], *[li[1] for j, li in enumerate(lists) if j != i])
                            self.addAssociation(num, fruit)
                    foundIntersection = True
                    break
            if not foundIntersection:
                break

    def calculateRemainingProbabilities(self):
        # Unfinished, since probability calculation doesn't account for intersection comparision
        self.data = sorted(self.data, key=lambda x: len(x[0]))
        for comb in self.data:
            values = comb[0].copy()
            valueAmount = len(values)
            fruits = comb[1].copy()
            for f in fruits:
                self.addAssociation(values, f, 1 / valueAmount)

    def addNotMentioned(self):
        notMentioned = [i for i in range(1, self.fruitAmount+1) if i not in self.mentioned]
        for i in self.desiredCombination:
            if i not in self.associations:
                self.associations[i] = (notMentioned, 1 / len(notMentioned))

    def listsByIndexes(self, indexList):
        return [self.data[i] for i in indexList]

    def addAssociation(self, nums, fruit, certainty=1):
        if not isinstance(nums, list):
            nums = [nums]
        self.associations[fruit] = (nums, certainty)
        for combination in self.data:
            if fruit in combination[1]:
                combination[1].remove(fruit)
            for n in nums:
                if n in combination[0]:
                    combination[0].remove(n)

    def __formatOutput(self):
        delimiter = " - "
        print("[Der Algorithmus konnte die folgenden Zuordnungen feststellen]")
        print()
        labeling = ["Frucht - Schale(n) - Wahrscheinlichkeit", "", "[---Wunschsorten---]"]
        desiredData = []
        spacing = ["[---Weitere Sorten---]"]
        remainingData = []
        for i in sorted(self.associations, key=lambda x: len(self.associations[x][0])):
            if i in self.desiredCombination:
                desiredData.append(f"{i}{delimiter}{self.associations[i][0]}{delimiter}{round(self.associations[i][1] * 100, 3)}%")
            else:
                remainingData.append(f"{i}{delimiter}{self.associations[i][0]}{delimiter}{round(self.associations[i][1] * 100, 3)}%")
        output = labeling + desiredData + spacing + remainingData
        print(self.__scaleOutput(output, delimiter=delimiter, newDelimiter="| "))

        print("------------------------------------------------------------------------------------")

    def __scaleOutput(self, outputList, FixedDataAmount=None, delimiter=" - ", newDelimiter="|"):
        outputList = [i.split(delimiter) for i in outputList]
        if FixedDataAmount is None:
            FixedDataAmount = len(outputList[0])
        newDelimiterMaxLengths = []
        for i in range(FixedDataAmount - 1):
            longest = outputList[0][i]
            for j in outputList[1:]:
                if len(j) - 1 >= i and len(j[i]) > len(longest):
                    longest = j[i]
            newDelimiterMaxLengths.append(len(longest))
        for i in outputList:
            for c, l in enumerateStep(newDelimiterMaxLengths, 2):
                if len(i) - 1 > c:
                    element = i[c]
                    nDelimiter = " " * (l - len(element) + 1) + newDelimiter
                    i.insert(c + 1, nDelimiter)
        return "\n".join(["".join(i) for i in outputList])

if __name__ == "__main__":
    for e in list(absPathsFromDir("examples")):
        print(f">Beispiel: '{os.path.split(e)[-1]}'")
        with open(e, "r", encoding="utf8") as f:
            content = [i.strip() for i in f.readlines()]
            _, runtime = PikeProblem(content[0], content[1].split(), content[2], content[3:]).solve(formatOutput=True, stopTime=True)
            print(f"Runtime: {str(runtime) + 's' if runtime is not None else runtime}")
            print()