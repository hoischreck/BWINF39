#Für Datei Umgang
import os
#Für Zufallszahlen Generation
from random import random
#Für Dictionary Funktionalität
from collections import defaultdict

#Klasse zur Spielerrepräsentierung
class Player():
    def __init__(self, strength, player_number):
        #Spielernummer
        self.number = int(player_number)
        #Spielerstärke
        self.strength = int(strength)

#Turnier Super-class
class Tournament():
    def __init__(self, repetitions, players):
        #Anzahl der Turnierdurchläufe
        self.repetitions = repetitions
        #Liste der teilnehmenden Spieler
        self.players = players
        #Der stärkster Spieler
        self.strongest_player = sorted({p: p.strength for p in self.players}.items(), key=lambda x: int(x[1]), reverse=1)[0][0]
        #Dictionary, welches die Anzahl der Siege eines Spielers mitzählt
        self.results = defaultdict(int)
        #Gesamte Spielanzahl
        self.total_plays = 0
    #Bestimmt das Spielergebnis zwischen 2 Spielern und gibt den Sieger aus
    def play(self, player1, player2):
        total = player1.strength + player2.strength
        while True:
            r = random()
            if r < player1.strength/total:
                return player1
            elif r > player1.strength/total:
                return player2
    #Gibt das Ergebnis eines Turniers aus
    def evaluation(self):
        return (self.tournament_type() , self.results, self.strongest_player, self.repetitions, self.total_plays)

    #returned die Art des Turniers
    def tournament_type(self):
        return self.__class__.__name__

#Klasse des Liga-Turniers
class Liga(Tournament):
    def __init__(self, repititions, players):
        #Erbt den 'Tournament'-Konstruktor
        super().__init__(repititions, players)
    #Simuliert Spielverlauf
    def simulate(self):
        #Die Simulation wird in höhe von Wiederholungen mal durchgeführt
        for _ in range(self.repetitions):
            # Liste welche Sieger speichert
            winners = []
            #Für jeden Spieler und seinen Index...
            for count, player in enumerate(self.players):
                #...spiele gegen alle Spieler, außer gegen die vorherigen
                for opponent in self.players[count+1:]:
                    #Erhöhe die gesamte Spielanzahl um 1
                    self.total_plays += 1
                    #Fügen den Sieger bei 'winners' hinzu
                    winners.append(self.play(player, opponent))
            #Die Spieler werden nach gesamten Siegen sortiert
            most_wins = sorted({i:winners.count(i) for i in winners}.items(), key=lambda x: x[1], reverse=True)
            #Wenn Siegesanzahl des 1. Spielers nur einmal vorkommt, dann...
            if [i[1] for i in most_wins].count(most_wins[0][1]) == 1:
                #...ist er der Sieger und wird zu den hinzugefügt und erhält einen Sieg
                self.results[most_wins[0][0]] += 1
            #Andernfalls...
            else:
                #...gewinnt der Spieler bei Gleichstand, mit der niedrigsten Spielernummer
                self.results[sorted([i[0] for i in most_wins if i[1] == most_wins[0][1]], key=lambda x: x.number)[0]] += 1
        #Die Ergebnisse werden returned
        return self.evaluation()

#Klasse des KO-Turniers
class KO(Tournament):
    def __init__(self, repititions, players):
        # Erbt den 'Tournament'-Konstruktor
        super().__init__(repititions, players)

    def create_plan(self, players):
        #Erstellt anhand einer geraden Spieleranzahl, den Spieleplan
        return [players[i:i+2] for i in range(0, len(players), 2)]
    # Simuliert Spielverlauf
    def simulate(self, KOTimesFive=False):
        # Die Simulation wird in höhe von Wiederholungen mal durchgeführt
        for _ in range(self.repetitions):
            #Die teilnehmenden Spieler stammen aus dem Klassenaufruf
            players = self.players
            #Solange Wahr...
            while 1:
                #...erstelle anhand der Spieler einen Spieleplan
                plan = self.create_plan(players)
                #...leere die Spielerliste
                players = []
                #Für jedes Duel im Spielplan
                for duel in plan:
                    #Die gesamt Spiele um 1 inkrementieren

                    #Wenn es sich um das KOx5-Turnier handelt, dann...
                    if KOTimesFive == 1:
                        self.total_plays += 5
                        #...Soll das Ergebnis per best-of-5 ermittelt werden
                        r = [self.play(duel[0], duel[1]) for _ in range(5)]
                        #Der Sieger wird zu 'Player'-Liste hinzugefügt
                        if r.count(duel[0]) > r.count(duel[1]):
                            players.append(duel[0])
                        else:
                            players.append(duel[1])
                    #Handelt es sich um ein normals KO-Turnier, dann...
                    else:
                        self.total_plays += 1
                        #...wird der Siege durch eine Runde bestimmt
                        players.append(self.play(duel[0], duel[1]))
                #Wenn nur noch ein Spieler übrig ist terminiert die while-Schleife
                if len(players) == 1:
                    #Der letzte Spieler ist Sieger und wird zu den Ergebnissen hinzugefügt und erhält einen Sieg
                    self.results[players[0]] += 1
                    break
        #Die Ergebnisse werden returned
        if KOTimesFive:
            return self.evaluation_KOx5()
        else:
            return self.evaluation()

    def evaluation_KOx5(self):
        return ("KOx5" , self.results, self.strongest_player, self.repetitions, self.total_plays)

#Game-Klasse enthält alle Funktionalitäten zur Durchführung und Auswertung der Turniere
class Game():
    def __init__(self, name, repetitions, player_amount, *players):
        #Dateiname
        self.name = name
        #Spieleranzahl
        self.player_amount = player_amount
        #Alle Spielr in Form von 'Player'-Objekten
        self.players = [Player(p, n+1) for n, p in enumerate(players)]
        self.repetitions = repetitions

    #Ausführende Methode
    def run(self):
        #Es wird für jede Turnierform ein respektives Objekt, mit entsprechenden Parametern erstellt
        #Die Ergebnisse werden duch die '__format_information'-Methode ausgegeben
        print(f"[---Die Ergebnisse für '{self.name}'---]")
        self.__format_information(Liga(self.repetitions, self.players).simulate())
        self.__format_information(KO(self.repetitions, self.players).simulate())
        self.__format_information(KO(self.repetitions, self.players).simulate(KOTimesFive=1))
        print("_______________________________________________")
        print("")

    #Gibt die Turnierdaten, in verständlicher Form wieder
    def __format_information(self, data):
        print("_______________________________________________")
        print(f"[Turnierform: {data[0]}]")
        print(f"Stärkster Spieler: {data[2].number} (Spielstärke: {data[2].strength})")
        print("Turnierergebnisse: ")
        for player in dict(sorted(data[1].items(), key=lambda x:x[1], reverse=True)):
            if player == data[2]:
                print(f"-->Nummer: {player.number} | Siege: {data[1][player]} von {data[3]} ({round(data[1][player]*100/data[3], 2)}%) [Stärke: {player.strength}]")
            else:
                print(f">Nummer: {player.number} | Siege: {data[1][player]} von {data[3]} ({round(data[1][player]*100/data[3], 2)}%) [Stärke: {player.strength}]")
        print(f"(Insgesamt {data[4]} Spiele gespielt)")

if __name__ == "__main__":
    # Verzeichnis der Beispiele.
    e_dir = "Beispiele"
    # Auflistung der Beispiel-Datein.
    examples = os.listdir(e_dir)

    # Jedes Beispiel, in 'examples'...
    for e in examples:
    #... wird geöffnet und gelesen.
        with open(os.path.join(e_dir, e), "r", encoding="utf8") as f:
            #Liest Dateiinhalte ein und erstellt Game-Objekt, welches per run() ausgeführt wird
            Game(e, 100000,*[i.strip() for i in f.readlines()]).run()