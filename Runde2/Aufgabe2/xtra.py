# def firstDuplicate(iterable1, iterable2):
#     for i in iterable1:
#         if i in iterable2:
#             return i
#     return None
#
# def firstNonDuplicate(iterable1, iterable2):
#     for i in iterable1:
#         if i not in iterable2:
#             return i
#     return None
#
# def intersectionOfOrderedIterable(iterable1, iterable2):
#     Intersection = []
#     for i in iterable1:
#         if i not in Intersection and binarySearch(iterable2, i):
#             Intersection.append(i)
#     return Intersection
#
#  def checkIntersection(self):
#         foundIntersection = True
#         for c, combination in enumerate(self.data):
#             v1 = combination[0]
#             for other in self.data[c+1:]:
#                 v2 = other[0]
#                 intersection = intersectionOfOrderedIterable(v1, v2)
#                 # print(intersection)
#                 # Wenn genau 1 Objekt in der Schnittmenge
#                 if len(intersection) == 1:
#                     self.addAssociation(intersection[0], firstDuplicate(combination[1], other[1]))
#                 elif len(intersection)+1 == len(v1):
#                     self.addAssociation(firstNonDuplicate(v1, intersection), firstNonDuplicate(combination[1], other[1]))
#                 elif len(intersection)+1 == len(v2):
#                     self.addAssociation(firstNonDuplicate(v2, intersection), firstNonDuplicate(other[1], combination[1]))
#                 elif len(intersection) == len(v1) and len(intersection) == len(v2):
#                     foundIntersection = False
#                 # Wenn nur noch 1 Objekt vorhanden
#                 else:
#                     foundIntersection = False
#             if foundIntersection:
#                 return True
#         return False