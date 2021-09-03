#Für Datei Umgang
import os

#Klasse für mögliche Puzzleteil Ausrichtungen
class Orientation():
    def __init__(self, piece_data):
        #Puzzleteil Repräsentierung
        self.piece_data = piece_data
    #Prüft auf Gleichheit, des mittelsten Wertes zweier Teile
    def check_middle(self, second_piece_data):
        return 1 if int(self.piece_data[1]) == -1*(int(second_piece_data[1])) else 0
    # Prüft auf Gleichheit, des linken Wertes beim Objekt und rechten Wert beim Parameter
    def check_left_side(self, second_piece_data):
        return 1 if int(self.piece_data[0]) == -1*(int(second_piece_data[2])) else 0

#Allgemeine Klasse für Puzzleteile
class Piece():
    def __init__(self, piece):
        #Puzzleteil Repräsentierung (Rohformat)
        self.raw_piece = piece
        #Puzzleteil Repräsentierung als Liste
        self.piece_data = piece.split()
        #Mögliche Ausrichtungen eines Puzzles als 'Orientation'-Objekte
        self.possible_states = [Orientation(self.rotate(i)) for i in range(3)]
    #"Dreht" das Puzzleteil beliebig oft
    def rotate(self, amount):
        r = self.piece_data
        for i in range(amount):
            r = r[-1:] + r[:2]
        return r

#Klasse des Dreieckspuzzle-Datentyp
class Puzzle_Matrix():
    def __init__(self, piece_amount):
        #Wert für Leere Felder
        self.empty = []
        #Teilanzahl
        self.piece_amount = piece_amount
        #Reihenanzahl
        self.row_amount = int(self.piece_amount ** 0.5)
        #Die "PuzzleMatrix"
        self.matrix = self.__create_matrix()
        #Erstellt ein Dictionary, das für jeden Index der "PuzzleMatrix" Informationen abspeichert
        self.index_data = {i:[] for i in range(self.piece_amount)}
        #Liste der benutzten Teile
        self.used = []
    #Erstellt die Matrix (Repräsentierung des Dreieckes in Form von verschachtelten Listen)
    #Somit wird für jede Reihe eine Liste, mit der Anzahl benötigter Teile eingefügt
    def __create_matrix(self):
        return [[self.empty] * (2 * i + 1) for i in range(self.row_amount)]

    #Gibt die "PuzzleMatrix" als 1-dimensionale Liste wieder
    def straight_list(self):
        l = []
        for i in self.matrix:
            l.extend(i)
        return l

    #Gibt jeden belibiegen Eintrag der "PuzzleMatrix", mit einem 1-dimensionalen Index wieder
    def retrieve_from_index(self, index):
        return self.straight_list()[index]

    #Man kann ein beliebiges Element, mit einem 1-dimensionalen Index an jede Stelle der "PuzzleMatrix" setzen
    def add_to_index(self, index, item):
        twoDIndex = self.translate1DimIndex_to_2DimIndex(index)
        self.matrix[twoDIndex[0]][twoDIndex[1]] = item

    # Man kann ein beliebiges Element, mit einem 1-dimensionalen Index von jeder Stelle der "PuzzleMatrix" entfernen
    def remove_from_index(self, index):
        twoDIndex = self.translate1DimIndex_to_2DimIndex(index)
        self.matrix[twoDIndex[0]][twoDIndex[1]] = self.empty

    #Setzt die Index-Daten, eines Indexes zurück
    def reset_index_data_at(self, index):
        self.index_data[index] = []

    #Fügt beliebige Daten, zu einem Index hinzu
    def add_index_data_at(self, index, item):
        self.index_data[index].append(item)

    #Übersetzt einen 1-dimensionalen Index in einen 2-dimensionalen (ermöglicht Arbeit an der "PuzzleMatrix")
    def translate1DimIndex_to_2DimIndex(self, index):
        for c, row in enumerate([2*i for i in range(self.row_amount)]):
            if index > row:
                index -= row+1
                continue
            else:
                return c, index
    #Gibt für einen beliebgen Index, den Wert zurück, der in der "PuzzleMatrix" darüber steht
    def retrieve_above(self, index):
        position = self.translate1DimIndex_to_2DimIndex(index)
        return self.matrix[position[0]-1][position[1]-1]

#Klasse zum lösen von Puzzlen
class Puzzle_solver():
    def __init__(self, name, figure_amount, piece_amount, *pieces):
        #Puzzlename
        self.name = name
        #Figurenanzahl
        self.figure_amount = int(figure_amount)
        #Teilanzahl
        self.piece_amount = int(piece_amount)
        #Teile das Piece-Objekte repräsentiert
        self.pieces = [Piece(p) for p in pieces]
        #"PuzzleMatrix" zur entsprechenden Puzzle Größe
        self.puzzle_matrix = Puzzle_Matrix(self.piece_amount)

    #Erschließt Puzzle Lösung
    def solve(self):
        #Wenn durch "solveable", als wahrscheinlich lösbar deklariert, dann...
        if self.solveable():
            #Wird der puzzle_index erstellt
            puzzle_index = 0
            #Es startet eine while-Schleife, die in jedem Durchlauf...
            while 1:
                #...die Möglichkeiten, für die Stelle puzzle_index in der "PuzzleMatrix" bestimmt
                possible = self.possible_pieces(puzzle_index)
                #Wenn es mindestens ein mögliches Teil gibt, dann...
                if len(possible) > 0:
                    #...wird das erste mögliche als Variable festgesetzt...
                    item = possible[0]
                    #...für diesen Index als benutzt abgespeichert
                    self.puzzle_matrix.add_to_index(puzzle_index, item[1].piece_data)
                    #Das Teil wird zu den benutzten Teilen hinzugefügt
                    self.puzzle_matrix.used.append(item[0])
                    #Und in die "PuzzleMatrix" eingefügt
                    self.puzzle_matrix.add_index_data_at(puzzle_index, item)
                    #Der puzzle_index wird um 1 inkremiert, sodass im nächsten Durchlauf, die nächste Stelle betrachtet wird
                    puzzle_index += 1
                #Gibt es keine Möglichkeiten, dann...
                else:
                    #...setzte alle Daten des aktuellen Indexes zurück
                    self.puzzle_matrix.reset_index_data_at(puzzle_index)
                    #...und entferne das Puzzlestück, aus der "PuzzleMatrix", von der aktuellen Stelle
                    self.puzzle_matrix.remove_from_index(puzzle_index)
                    #Der puzzle_index wird um 1 dekrementiert. Ist wird im nächsten loop, die vorherige Lücke betrachtet
                    puzzle_index -= 1
                    #Sollte der Index negativ werden, dann...
                    if puzzle_index < 0:
                        #...ist das Puzzle nicht lösbar
                        return self.__evaluation(f"Das Puzzle: '{self.name}', ist nicht lösbar.")
                    #Es wird das letzte Elemement, der genutzten Puzzleteile entfernt
                    self.puzzle_matrix.used.pop()

                #Sollte der puzzle_index gleich größ, wie die Teilanzahl sein, dann terminiere und gebe das Ergebnis aus
                if puzzle_index >= self.piece_amount:
                    return self.__evaluation(self.puzzle_matrix)
        #Wenn als nicht lösbar deklariert, dann returne dies
        else:
            return self.__evaluation(f"Das Puzzle: '{self.name}', ist nicht lösbar.")

    #Erstellt für jeden Index, in der "PuzzleMatrix", die möglichen Teile bzw. ihre Ausrichtung
    def possible_pieces(self, index):
        #Liste der möglichen Teile
        pos_pieces = []
        #Für jedes Puzzleteil...
        for piece in self.pieces:
            #Für jede Ausrichtung dieses Teils...
            for orientation in piece.possible_states:
                #Wenn das Teil zuvor nicht genutzt wurde und
                #Das Teil, in dieser spezifischen Ausrichtung, nocht nicht für den gegebenden Index eingesetz wurde, dann...
                if piece not in self.puzzle_matrix.used and (piece, orientation) not in self.puzzle_matrix.index_data[index]:
                    #...wird das Teil, mit der Ausrichtung in pos_pieces gespeichert, wenn es das erste jeder Reihe ist
                    if self.puzzle_matrix.translate1DimIndex_to_2DimIndex(index)[1] == 0:
                        pos_pieces.append((piece, orientation))
                    #Andernfalls, wird...
                    else:
                        #Geprüft, ob das Teil nach unten ausgerichtet ist, denn dann...
                        if (self.puzzle_matrix.translate1DimIndex_to_2DimIndex(index)[1]+1)%2 == 0:
                            #Wird geprüft, ob es an das vorherige linke und obere Stück passt
                            if orientation.check_left_side(self.puzzle_matrix.retrieve_from_index(index-1)) and orientation.check_middle(self.puzzle_matrix.retrieve_above(index)):
                                #Wenn ja, dann wird es zu den Möglichkeiten hinzugefügt
                                pos_pieces.append((piece, orientation))
                            else:
                                #Sollte es nicht passen, wird die nächste Ausrichtung betrachtet
                                continue
                        #Wenn es nach oben zeigt, wird geprüft, ob es an das vorherige Teil passt.
                        elif orientation.check_left_side(self.puzzle_matrix.retrieve_from_index(index-1)):
                            # Wenn ja, dann wird es zu den Möglichkeiten hinzugefügt
                            pos_pieces.append((piece, orientation))
        #Es werden alle Möglichkeiten ausgegeben
        return pos_pieces

    #Gibt wieder, ob ein Puzzle grundsätzlich, wahrscheinlich lösbar ist
    def solveable(self):
        #Formel für die Anzahl, der mindest benötigten Verbindungen, um eine Dreieckspuzzle zu bilden
        formula = lambda x: int((3*(x-x**0.5)/2))
        #Es werden alle Zahlen, der Puzzleteile in eine Liste gepackt...
        all_pieces_together = []
        for piece in [piece.piece_data for piece in self.pieces]:
            all_pieces_together += [int(i) for i in piece]
        pair_count = 0
        #...und geguckt, wie viele Pärchen, die jeweilgen Zahlen bilden
        for i in range(1, self.figure_amount+1):
            pair_count += sorted([all_pieces_together.count(i), all_pieces_together.count(-i)], key=lambda x:x)[0]
        #Gibt es weniger Paare, als benötigt, um alle Verbindungen zu bilden, dann
        if pair_count < formula(self.piece_amount):
            #...wird False wiedergegeben
            return False
        else:
            #...sonst True
            return True

    #Gibt die Ergebnisse der solve-Methode aus
    def __evaluation(self, data):
        if type(data) == str:
            print(data)
        else:
            for c, i in enumerate(data.matrix):
                print((len(data.matrix) - c + 1) * "                  " + str(i))

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
            #Es wird jede Datei ausgelesen und eine Puzzle_solver-Objekt erstellt, das per solve() ausgeführt wird
            content = [i.strip() for i in f.readlines()]
            Puzzle_solver(e, *content[:2], *content[2:]).solve()
            print("")