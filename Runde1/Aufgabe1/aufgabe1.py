#Für Datei Umgang
import os

#MasterString vererbt als super class wichtige Methoden an die Klassen: 'Blank' und 'Word'.
class MasterString():
    def __init__(self):
        #Dient der einheitlichen Stringrepräsentierung.
        self.string_data = None

    #Ersetzt beliebige Zeichen, im repräsentierenden Objekt-String (self.string_data) und returned diesen.
    def multi_replace(self, items=[",", ".", "?", "!", "_"]):
        s = self.string_data
        for i in items:
            s = s.replace(i, "")
        return s

#Klasse für die einzelnen Lücken.
class Blank(MasterString):
    def __init__(self, blank, position):
        #Die Stringrepräsentierung.
        self.string_data = blank
        #Postion der Lücke, im source Text.
        self.pos = position
        #Gibt an, ob Lücke vorgegende Zeichen enthält.
        self.empty = self.isempty()
    def isempty(self):
        #Prüft, ob ein Buchstabe, in self.string_data enthalten ist.
        return 1 if len(self.multi_replace()) == 0 else 0

#Klasse für die einzelnen Wörter.
class Word(MasterString):
    def __init__(self, word):
        #Die Stringrepräsentierung.
        self.string_data = word

#Klasse des Solvers
class Solver():
    def __init__(self, blanks, words):
        #Erstellt eine Liste mit allen Lücken-Objekten, mit Position.
        self.raw_blanks = [Blank(b, pos) for pos, b in enumerate(blanks)]
        #Erstellt eine 2. Liste, die die Stringrepräsentierung aller Blanks enthält.
        self.raw_blanks_string_data = blanks
        #Erstellt eine Liste, mit allen Wörtern.
        self.raw_words = [Word(w) for w in words]

    #Die Lückentext-Lösungs-Methode
    def run(self):
        #Erstellt ein Dictionary, welches für jede Lücke alle Möglichkeiten enthält
        #und diese danach sortiert, ob sie einen Buchstaben vorgegeben habe oder nicht.
        #In beiden Fällen wird danach nochmal unterschieden, zwischen der Anzahl der Möglichkeiten.
        #Aufbau: {Blank0:[ [Mögliche Wörter] , [Bereits verwendete] ], ...}.
        solver_dic = self.create_order({b: self.possibilities(b) for b in self.raw_blanks})
        #pos: Position, der aktuell betrachteten Lücke.
        #used: Bereits, im Lückentext verwendete Wörter.
        pos, used = 0, []
        #Lösungs-Schleife
        while True:
            #Betrachtete Lücke und die zugehörigen Möglichkeiten.
            blank, word_data = list(solver_dic.items())[pos]
            #Zuvor verwendete Wörter.
            used = used[:pos]
            #Die aus 'used' reultierenden Möglichkeiten, welche Wörter noch einsetzbar sind
            possible = list(filter(lambda x: x not in used, word_data[0]))
            #Wenn es mindestens 1 mögliches Wort gibt, das vorhanden ist und noch nicht genutzt wurde, dann...
            #print(len(self.raw_blanks_string_data)-pos)
            if len(word_data[0]) > 0 and len(possible) > 0:
                #...ist das einzusetzene Wort, das 1. aus 'possible'.
                word = possible[0]
                #Das wird dann aus den möglichen Wörter, der Lücke, entfernt...
                solver_dic[blank][0].remove(word)
                #... und bei den verwendeten Wörtern, der Lücke, eingetragen.
                solver_dic[blank][1].append(word)
                #Danach wird der Klartext-String mit diesem Wort, an der richtigen Stelle vervollständigt.
                self.raw_blanks_string_data[blank.pos] = word.string_data + self.raw_blanks_string_data[blank.pos][len(word.string_data):]
                #Worauf, das Wort noch in die Liste, der bereits Benutzten, aufgenommen wird.
                used.append(word)
                #Zum Schluss wird 'pos' um 1 inkrementiert, sodass im nächsten loop, die folgende Lücke betrachtet wird.
                pos += 1
                #Sollte 'pos' der Anzahl an Lücken entsprechen, dann...
                if pos == len(solver_dic):
                    #...wird der gesamte Lücken-String, als Lösung returned
                    return " ".join(self.raw_blanks_string_data)
            #Wenn es keine einsetzbaren Wörter geben sollte, dann...
            else:
                #... wird die gesamte Menge, der ursprünglichen Möglichkeiten wiederhergestellt
                #und die verwendenten Wörter, der Lücke, zurückgesetzt.
                solver_dic[blank] = [[*solver_dic[blank][0],*solver_dic[blank][1]],[]]
                #Es wird der ursprüngliche Inhalt, der Lücke, im Klartext, wiederhergestellt.
                self.raw_blanks_string_data[blank.pos] = blank.string_data
                #Zum Schluss wird die Position um 1 dekrementiert, sodass im nächsten loop, die vorherige Lücke betrachtet wird.
                pos -= 1

    #Gibt die möglichen Wörter, für eine Lücke wieder.
    def possibilities(self, blank):
        #Ersetzt alle Zeichen, sodass, wenn vorhanden, nur der Buchstabe übrig bleibt.
        letter = blank.multi_replace()
        #Wenn es keinen Buchstaben, in der Lücke, gibt, dann...
        if len(letter) == 0:
            #...werden alle Wörter zurückgegeben, wenn sie so viele Buchstaben, wie es Buchstabenlücken gibt, haben.
            return [[word for word in self.raw_words if len(word.string_data) == len(blank.multi_replace([",", "?", ".", "!"]))], []]
        #Sollte ein Buchstaben vorhanden sein, dann...
        else:
            # ...werden alle Wörter zurückgegeben, wenn sie so viele Buchstaben, wie es Buchstabenlücken gibt, haben.
            #Und zusätzlich, den Buchstaben 'letter' an der gleichen Stelle haben sollten.
            return [[word for word in self.raw_words if len(word.string_data) == len(blank.multi_replace([",", "?", ".", "!"])) and letter == word.string_data[blank.string_data.find(letter)]], []]

    #Sortiert das Lösungs-Dictionary
    def create_order(self, dictionary):
        #empty: Liste der Lücken, ohne Buchstaben.
        #signed: Lister der Lücken, mit Buchstaben.
        empty, signed = [], []
        #Für jede Lücke im Lösungs-Dictionary,...
        for b in dictionary:
            #...wenn kein Buchstabe vorhanden, dann...
            if b.empty:
                #... b zu 'empty' hinzufügen.
                empty.append((b, dictionary[b]))
            else:
                # Andernfalls, 'signed' hinzufügen.
                signed.append((b, dictionary[b]))
        #Es wird einen neues Lösungs-Dictionary zurückgegeben, welches 'signed' und 'empty', in dieser Reihenfolge kombiniert
        #und jeweils, nach Anzahl, der Möglichkeiten, für die einzelnen Blanks sortiert.
        return dict(sorted(signed, key=lambda x: len(x[1][0])) + sorted(empty, key=lambda x: len(x[1][0])))

#Programm Ausführung.
if __name__ == "__main__":
    #Verzeichnis der Beispiele.
    e_dir = "Beispiele"
    #Auflistung der Beispiel-Datein.
    examples = os.listdir(e_dir)

    #Jedes Beispiel, in 'examples'...
    for e in examples:
        #... wird geöffnet und gelesen.
        with open(os.path.join(e_dir, e), "r", encoding="utf8") as f:
            #Es wird mit den Lücken und Wörter, der Datei, ein neues Solver-Objekt erstellt,
            #welches per 'run' ausgeführt wird und die returned Lösung per 'print' ausgibt.
            print(Solver(*[line.strip().split() for line in f.readlines()]).run())