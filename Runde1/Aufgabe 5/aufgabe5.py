#Für Datei Umgang
import os
#Dictionary Funktionalität
from collections import defaultdict

#Klasse für Schüler
class Student():
    def __init__(self, number, wishes):
        #Schüler-Nummer
        self.iD = number
        #Schüler-Wünsche, mit ihrer Priorität
        self.wishes = {int(i):c for c, i in enumerate(wishes)}

#Wichtel-Klasse
class Wichteln():
    def __init__(self, present_amount, *student_wishes):
        #Alle Geschenke (int-Repräsentierung)
        self.presents = [i for i in range(1, int(present_amount)+1)]
        #Alle Schüler als Student-instances
        self.students = [Student(c+1, s.split()) for c, s in enumerate(student_wishes)]

    #Ermittelt beste Verteilung
    def run(self):
        #Es wird ein Dictionary names 'data' erstellt, welches für alle Prioritäten (1. Wunsch, 2. Wunsch, etc.)
        #alle enthaltenden Geschenke und zugehörigen Schüler beinhaltet
        data = {}
        for prioritys in range(3):
            new_priority = defaultdict(list)
            for present in self.presents:
                for student in self.students:
                    if present in student.wishes.keys() and prioritys == student.wishes[present]:
                        new_priority[present].append(student)
            data[prioritys] = dict(new_priority)

        #Dictionary der bereits verwendeten Geschenke, mit Schüler
        used = {}
        #Index der Wunschpriorität (1. Wunsch, 2. Wunsch, etc.)
        priority_index = 0
        #Es wird eine while-Schleife initiiert
        #Welche in jedem Durchlauf...
        while True:
            #...eine Liste erstellt, mit Geschenken, die auf mehrere Schüler zutreffen
            evaluate = []
            #...das Dictionary für den betrachteten priority_index ausgibt und bereits zugeteilte Geschenke, sowie Schüle exkludiert
            present_data = self.presents_without_used(data[priority_index], used)
            #Es wird für jedes Geschenk, aus dem present_data dictionary...
            for present in present_data:
                #...geprüft, ob es nur  einen Schüler mit diesem Wunsch gibt
                if len(data[priority_index][present]) == 1:
                    #Wenn ja, dann soll dieser, mit Geschenk zu used hinzugefügt werden
                    used[present] = (present_data[present][0], priority_index)
                #Gibt es mehr Schüler, mit dem gleichen Wunsch, dann...
                elif len(data[priority_index][present]) > 1:
                    #... werden diese, mit Geschenk zu evaluate hinzufügt
                    evaluate.append((present, present_data[present]))

            #Für Schüler-Listen und entsprechendem Geschenk, aus der evaluate-Liste...
            for equal in evaluate:
                #...wird eine Liste zum vergleichen erstellt
                comparison = []
                #...wird found auf False gesetzt
                found = 0
                #Für jeden Schüler, aus der Schüler-Liste...
                for student in equal[1]:
                    #...wird geguckt, welche möglichen Wünsche erfüllt werden können
                    pos = self.next_possible(student, used, priority_index)
                    #Wenn es mindestens eine weiter Möglichkeit gibt, dann wird der Schüler + pos zu comparission hinzugefügt
                    if len(pos) > 0:
                        comparison.append([student, pos])
                    #Wenn sich keine weiteren Möglichkeiten, aus den Prioritäten ergeben, dann...
                    else:
                        #Wird dieser Schüler, mit Geschenk direkt in used eingefügt und die Verteilung des Geschenkes gilt als abgeschlossen
                        used[equal[0]] = (student, priority_index)
                        #found wird auf True gesetzt
                        found = 1
                        #Und weitere Betrachtungen der Schüler werden beendet
                        break
                #Wenn found True sein sollte, dann werden weitere Auswertungen unterbrochen (Geschenk wurde bereits zugeteilt)
                if found:
                    break
                #Wenn alle betrachteten Schüler, für das jeweilge Geschenk dennoch weitere Möglichkeiten haben sollten, dann wird hier sortiert.
                #Es bekommt der Schüler das Geschenk, dessen nächster Wunsch am weitesten zurückliegt.
                used[equal[0]] = (sorted(comparison, key=lambda x: x[1][0][1], reverse=1)[0][0], priority_index)

            #Wenn der Wert, für den betrachteten Index gleich 2 oder größer ist, dann...
            if priority_index >= 2:
                #...wird die while Schleife beendet, da jede Wunschzeile betrachtet wurde.
                break
            #Andernfalls wird der Index um 1 inkrementiert
            priority_index += 1

        #Eine Liste, der nicht zugeordneten Geschenke
        unassigned_presents = [p for p in self.presents if p not in used]
        #Eine Liste, der nicht zugeordneten Schüler
        unassigned_students = [s for s in self.students if s not in [i[0] for i in used.values()]]
        for i, unassigned_student in enumerate(unassigned_students):
            #Es wird für jeden Schüler ein Geschenk, nach Nummer zugeordnet
            used[unassigned_presents[i]] = (unassigned_student, 3)

        #Das Endergebnis (used) wird sortiert und durch die Objekt eigene Funktion formatiert und ausgegeben
        self.__format_information(dict(sorted(used.items(), key=lambda x:x[0])))

    #Sortiert alle bereits genutzten Einträge von Geschenken und Schülern aus
    def presents_without_used(self, dictionary, used):
        #Es wird eine neues Dictionary erstellt
        new_dict = {}
        #für jedes Geschenk im original Dictionary...
        for present in dictionary:
            #...wird eine Liste, der nicht verwendeten Schüler erstellt
            new_data = [student for student in dictionary[present] if student not in [i[0] for i in used.values()]]
            #Wenn dann das Geschenk noch nicht verteil wurde und es mehr als einen zugehörigen Schüler geben sollte, dann...
            if present not in used and len(new_data) > 0:
                #...wird dieses Geschenk, samt der möglichen Schüler bei new_dict eingetragen
                new_dict[present] = new_data
        #Das gefilterte Dictionary wird zurückgegeben
        return new_dict

    #Sucht für einen Schüler, anhand eines Indexes heraus, ob es noch folgende Geschenke gibt, mit ihrem Index
    def next_possible(self, student, used, index):
        #Für alle folgenden Wünsche eines Schülers, ab Index, wird geguckt, ob dieses Geschenk schon verwendet wurde und wenn nicht,
        #dann wird dieses zusammen mit der Priorität hinzugefügt.
        #Zum Schluss wird dann noch nach der Priorität sortiert
        return sorted([(wish, student.wishes[wish]) for wish in list(student.wishes.keys())[index+1:] if wish not in used.keys()], key=lambda x:x[1])

    #Formatiert die Rohdaten aus 'run'
    def __format_information(self, raw):
        print("Die ideale Verteilung lautet:")
        for present in raw:
            print(f">Geschenk: '{present}' geht an '{raw[present][0].iD}' (Priorität: {raw[present][1]+1})")
        data = [i[1][1] for i in raw.items()]
        print(f"Gesamtanzahl: '{len(self.presents)}' Geschenke")
        print(f">> 1. Wünsche [{data.count(0)}] | 2. Wünsche [{data.count(1)}] | 3. Wünsche [{data.count(2)}] |Zugeordnet [{data.count(3)}] <<")


if __name__ == "__main__":
    # Verzeichnis der Beispiele.
    e_dir = "Beispiele"
    # Auflistung der Beispiel-Datein.
    examples = os.listdir(e_dir)
    # Jedes Beispiel, in 'examples'...
    for e in examples:
    #... wird geöffnet und gelesen.
        print(f"[--- Datei: '{e}' ---]")
        with open(os.path.join(e_dir, e), "r", encoding="utf8") as f:
            #Es werden alle Zeilen eingelsen...
            content = [i.strip() for i in f.readlines()]
            #Und ein Wichteln-Objekt erstellt und ausgeführt
            #In den Konstruktor werden dabei die Anzahl der Geschenke und die Schüler-Wünsche übergeben
            Wichteln(content[0], *content[1:]).run()
