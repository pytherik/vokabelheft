from pathlib import Path
from os import system
from random import randint
import sys

gesamt_heute  = 0
richtig_heute = 0
falsch_heute  = 0
hinzugefügt   = 0

path = Path.home()/"vocnscore.txt"
path_no_score = Path.cwd()/"voc_en_de.txt"


class Vokabeln:
    """ Vokabeltrainer """
    title = (chr(1422) * 45 + "\n" +
         chr(1422) + "VOKABELHEFT".center(43) +
         chr(1421) + "\n" + chr(1421) *45)
    fremd = []       # Vok. Fremdsprache
    deutsch = []     # Vok. Deutsch
    score = []       # Scoring
    found = []       # Suchindizes
    
    def __init__(self, path):
        """ Textdatei einlesen und aufteilen """
        with path.open("r") as vok:
            for el in vok:
                fremd_deutsch = el.strip().split(",")
                self.fremd.append(fremd_deutsch[0])
                self.deutsch.append(fremd_deutsch[1:-3])
                self.score.append([int(fremd_deutsch[-3]),
                                   int(fremd_deutsch[-2]),
                                   int(fremd_deutsch[-1])])   
        self.menu()
        
    def statistik(self):
        """ macht Statistik """
        anz_vok = len(self.fremd)
        gesamt  = 0
        richtig = 0
        falsch  = 0
        for index in range(len(self.fremd)):
            gesamt  += self.score[index][0]
            richtig += self.score[index][1]
            falsch  += self.score[index][2]
        return (anz_vok, gesamt, richtig, falsch)
    
    def menu(self):
        """ Startseite, Auswahlmenu """
        system("clear")
        print(self.title)
        
        data = self.statistik()
        print(f"\nSammlung gesamt:{str(data[0]).rjust(5)}   Vokabeln.")
        if not hinzugefügt:
            print("\n\n")
        else:
            print(f"Hinzugefügt    :{str(hinzugefügt).rjust(5)}\n") 
        print("_" * 45)
        print(f"Abfragen gesamt:{str(data[1]).rjust(5)}   heute:{str(gesamt_heute).rjust(3)}\n")
        print(f"richtig  gesamt:{str(data[2]).rjust(5)}   heute:{str(richtig_heute).rjust(3)}")
        print(f"falsch   gesamt:{str(data[3]).rjust(5)}   heute:{str(falsch_heute).rjust(3)}")
        print("" + ("_" * 45))
        print("\n1: Abfragen")
        print("\n2: Nachschlagen")
        print("\n3: Neue Vokabel")
        print("\n4: Bearbeiten")
        print("\n5: BEENDEN")
        print("_" * 45)
        print("\n", end = self.prompt())
        wahl = 0
        while wahl not in (1, 2, 3, 4, 5, 42) or wahl == "":
            try:
                wahl = int(input())
            except ValueError:
                print("<1> bis <5> als Ziffer eingeben !\n",end = self.prompt())
        if   wahl == 1: self.lernen()
        elif wahl == 2: self.suchen()
        elif wahl == 3: self.anlegen()
        elif wahl == 4: self.aendern2()
        elif wahl ==42: self.score_löschen()
        else:
            self.ende()
        
    def find(self, vok):
        """ Indizes gefundener Einträge in Liste ausgeben """
        found = []
        for index in range(len(self.fremd)):
            if vok in self.fremd[index]:
                found.append(index)

        for index in range(len(self.deutsch)):
            for wort in range(len(self.deutsch[index])):
                if vok in self.deutsch[index][wort]:
                    if index in found:
                        continue
                    found.append(index)
        return found

    def trans(self,vok):
        """ gibt alle Übersetzungen aus """
        found = self.find(vok)
        if not found:
            print("Nicht vorhanden")
            return False
        for index in found:
            self.anzeigen(self.fremd[index], self.deutsch[index])

    def anzeigen(self, fremd, deutsch):
        """ Vokabel anzeigen """ 
        print((chr(717) * 45))
        print(f"Englisch  : {fremd}\n")
        i = 0
        for wort in deutsch:
            print(f"Deutsch {i+1} : {wort}")
            i += 1
        print(chr(713) * 45)
                
    def lernen(self):
        """ Vokabeln abfragen """
        system("clear")
        print(self.title)
        
        global gesamt_heute
        global richtig_heute
        global falsch_heute

        gesamt_heute += 1
        ran = randint(0, len(self.fremd)-1)
        print("\n\n" + chr(717) * 45)
        print(f"Was heißt '{self.fremd[ran]}' auf deutsch ?".center(45))
        print(chr(713) * 45)
        print("", end = self.prompt())

        antwort = input()
        self.score[ran][0] += 1
        if antwort in self.deutsch[ran]:
            print("\nRichtig !\n")
            self.anzeigen(self.fremd[ran], self.deutsch[ran])        
            richtig_heute +=1
            self.score[ran][1] += 1
        else:
            print("\nNicht ganz :")
            self.anzeigen(self.fremd[ran], self.deutsch[ran])
            if antwort:
                print("\nSiehst du ein, dass du falsch lagst  <1> ")
                print("oder soll deine Lösung mit ins Heft  <2> ?\n",end = self.prompt())
                nr = input()
                if not nr or nr == "1":
                    falsch_heute += 1
                    self.score[ran][2] += 1
                    system("clear")
                    print(self.title)
                    print("\n\n\nAlles klar !\n\n\n")
                    print(("*" * 25).center(45))
                    print(("*" * 21).center(45))
                    print("F A L S C H !".center(45))
                    print(("*" * 13).center(45))
                    print((("*" * 9).center(45))+"\n\n\n")
                elif nr == "2":
                    self.bearbeiten(ran, antwort)
            else:
                falsch_heute +=1
                self.score[ran][2] += 1
        print("\nWeiterlernen (j/n) ?", end = self.prompt())
        if self.j_n() :
            self.lernen()
        else:
            self.menu()

    def suchen(self):
        """ Übersetzung suchen und anzeigen, alternativ: Speicheroption"""
        system("clear")
        print(self.title)

        print("\n\n" + chr(717) * 45)
        print("Bitte gib Dein Suchwort ein".center(45))
        print(chr(713) * 45)
        print("", end = self.prompt())
        vok = input()
        if not vok:
            self.menu()
        if len(vok) < 3:
            weiter = input("      ... mindestens drei Buchstaben <enter>")
            self.suchen()
        found = self.find(vok)
        if found:
            print()
            for index in found:
                self.anzeigen(self.fremd[index], self.deutsch[index])
        elif not found:
            print("\n... ist noch nicht dabei !")
            print(f"\n'{vok}' anlegen (j/n) ?", end = self.prompt())
            if self.j_n():
                self.aendern2(vok)
        
        print("\nWeitersuchen (j/n) ?", end = self.prompt())
        if self.j_n(): self.suchen()
        else:
            self.menu()
            
    def anlegen(self, vok=False, i=1):
        """ neue Vokabeln hinzufügen """
        system("clear")
        print(self.title)
        
        deutsch = []
        if i == 2:
            deutsch.append(vok)
            vok = False
        
        print(f"\nS P A M !  Wort Nr.{len(self.fremd)+1}\n\n")
        print(f"Du  fügst  heute das {hinzugefügt + 1}. Wort hinzu!")
        print("_" * 45)
        if vok :
            print(f"\nDas neue Wort (en) :{self.prompt()}{vok}")
            print("richtig   (j_n) ?", end = " > ")
            if not self.j_n():
                self.anlegen()
            
        while not vok:
            print("\nDas neue Wort (en) :", end = self.prompt())
            vok = input()
            if not vok:
                self.menu()
            elif self.find(vok):           
                print("\nHamwa schon:")
                self.trans(vok)
                print("\n\nTrotzdem weiter (j/n) ?", end = self.prompt())
                if not self.j_n():
                    self.menu()
                else:
                    self.anlegen(vok)
            print("richtig   (j_n) ?", end = " > ")
            if not self.j_n():
                vok = False
        fremd = vok
        save = False
        if i == 2:
            print("Bedeutung 1        :", end = self.prompt())
            print(deutsch[0])
        while not save:
            print(f"Bedeutung {i}        :", end = self.prompt())
            bedeutung = input()               
            if not bedeutung and not deutsch:
                self.menu()
            elif not bedeutung:
                save = True
                self.behalten(fremd, deutsch)
            else:
                deutsch.append(bedeutung)
            i += 1    
        print("\nweitere Vokabeln (j/n) ?", end = self.prompt())
        if self.j_n():
            self.anlegen()
        else:
            self.menu()

    def behalten(self, fremd, deutsch):
        """ Vokabeln aktualisieren """
        global hinzugefügt
        system("clear")

        print(self.title)
        print("\n\n" + chr(717) * 45)
        print("Möchtest du den Eintrag so übernehmen ?".center(45))
        print(chr(713) * 45)
        print()   
        self.anzeigen(fremd, deutsch)
        self.fremd.append(fremd)
        self.deutsch.append(deutsch)
        self.score.append([0, 0, 0])
        print("\nAlles O.K. (j/n) ?", end = self.prompt())
        if not self.j_n():
            self.aendern(index=len(self.fremd)-1, hinzu=True)
        hinzugefügt += 1
            
    def bearbeiten(self, ran=False, dazu=False, hinzu=False):
        """ Eintrag ändern (erweitern, löschen) """
        system("clear")

        print(self.title)
        global richtig_heute
        global falsch_heute
        global hizugefügt
        
        if ran and dazu:
            self.deutsch[ran].append(dazu)
            self.anzeigen(self.fremd[ran], self.deutsch[ran])
            print("\nGefällt's dir so (j/n)?", end = self.prompt())
            janein = self.j_n()
            if not janein and hinzu:
                self.aendern(ran, hinzu)
            elif not janein:
                self.deutsch[ran].pop()
                self.bearbeiten(ran)
            elif hinzu:
                hinzugefügt += 1
            else:
                self.score[ran][1] += 1
                richtig_heute += 1
                print("\n\n" + "*" * 45)
                print("Dafür gibts einen Schlumpf ins Heft :-)".center(45))
                print("*" * 45)
                print("\n<enter>", end = "")
                weiter = input()
                self.menu()
        elif ran:
            print("\nWie denn jetzt ?",end = self.prompt())
            vok = input()
            if not vok:
                print("\nOkay. Dann bleibt's dabei!\n")
                self.anzeigen(self.fremd[ran], self.deutsch[ran])
                print("\nWeiter mit <enter>", end = "")
                weiter = input()
                self.score[ran][2] += 1
                falsch_heute += 1
                return
            else:
                self.bearbeiten(ran, vok)
    def aendern2(self, vok=False):
        """ äander oder anlegen ? """
        system("clear")
        print(self.title)
        
        if not vok:
            print("\n\n" + chr(717) * 45)
            print("Gib das Wort ein, das du ändern möchtest.".center(45))
            print(chr(713) * 45)
            print("\n", end = self.prompt())
            vok = input()
            if not vok:
                self.menu()
            found = self.find(vok)
            if not found:
                print(f"\n'{vok}' ist noch nicht im Heft !")
                print("\nDu kannst es jetzt hinzufügen (j/n).",end = self.prompt())
                if  not self.j_n():
                    self.menu()
                else:
                    self.aendern2(vok)
            if len(found) > 1:
                print()
                for index in found:
                    print(f"    <{found.index(index)+1}>")
                    self.anzeigen(self.fremd[index], self.deutsch[index])    
                print("\nWelchen Eintrag möchtest du ändern ?", end = self.prompt())
                nr = 0
                while nr < 1 or nr > len(found):
                    try:
                        nr = int(input())
                    except ValueError:
                        print(f"<1> - <{len(found)}>", end = self.prompt())
                        nr = 0
                self.aendern(index = found[nr - 1])
            else:
                self.aendern(index = found[0])
        print(f"\n\n\nIst {vok} das englische Wort ?", end = self.prompt())
        if self.j_n():
            self.anlegen(vok)
        else:
            self.anlegen(vok, 2)
        
    def aendern(self, index, hinzu=False):
        system("clear")

        global hinzugefügt
        
        print(self.title)
        print("\n\n")
        self.anzeigen(self.fremd[index], self.deutsch[index])
        print("\nmöchtest du: Eintrag löschen     <1> oder")
        print("deutsche Bedeutung hinzufügen    <2> oder")
        print("deutsche Bedeutung   löschen     <3> oder")
        print("\ndoch nichts, zurück zum Menu <enter> ", end = self.prompt())     
        nr = input()
        if not nr or nr not in ["1", "2", "3"]:
            if hinzu:
                hinzugefügt += 1
            self.menu()
        elif nr == "1":
            del self.deutsch[index]
            del self.fremd[index]
            del self.score[index]
            print("\nDer Eintrag ist gelöscht !\n\nweiter mit <enter>", end = self.prompt())
            weiter = input()
            self.menu()
        elif nr == "2":
            system("clear")

            print(self.title)
            self.anzeigen(self.fremd[index], self.deutsch[index])
            print(f"\nBedeutung {len(self.deutsch[index])+1}        :", end = self.prompt())
            bedeutung = input()
            if bedeutung:
                self.bearbeiten(index, bedeutung, hinzu)
            else:
                self.aendern(index, hinzu)
        else:
            system("clear")
            
            i = 1
            x = []
            print(self.title)
            print("\n\n" + chr(717) * 45)
            for bedeutung in self.deutsch[index]:
                print(f"Bedeutung <{i}> : {self.deutsch[index][i-1]}")
                x.append(str(i))
                i += 1
            print(chr(713) * 45)
            print("\nWelche Bdeutung soll weg ?", end = self.prompt())
            nr = input()
            
            if nr not in x:
                self.aendern(index, hinzu)
            else:
                weg = self.deutsch[index][int(nr)-1]
                self.deutsch[index].remove(weg)
                self.anzeigen(self.fremd[index], self.deutsch[index])
                print("\nOkay so ?", end = self.prompt())
                if not self.j_n():
                    self.deutsch[index].append(weg)
                    self.aendern(index, hinzu)
                if hinzu:
                    hinzugefügt +=1
                self.menu()

        
    def score_löschen(self):
        """ löscht das Internet """
        self.score = []
        for null in range(len(self.fremd)):
            self.score.append([0, 0, 0])
        self.menu()
        
    def ende(self):
        """ Programm beenden, Statistik anzeigen und speichern """
        system("clear")

        print(self.title)
        print("\n\n" + chr(717) * 45)
        print("Heutige Änderungen speichern ? ".center(45))
        print(chr(713) * 45)
        print("\nj/n ? ", end = self.prompt())
        if self.j_n():
            with path.open("w") as neu_mit_score:
                with path_no_score.open("w") as neu_no_score:
                    for index in range(len(self.fremd)):
                        save = self.fremd[index]
                        for wort in self.deutsch[index]:
                            save += "," + wort
                        neu_no_score.write(save + "\n")
                        for score in self.score[index]:
                            save += "," + str(score)
                        neu_mit_score.write(save + "\n")
            print("\n\n" + chr(1421) * 45)
            print("g e s p e i c h e r t".center(45))
            print(chr(1421) * 45)
        
        else:
            print("\n\n" + chr(717) * 45)
            print("n i c h t  g e s p e i c h e r t".center(45))
            print(chr(713) * 45)
        print("\n")
        print("TSCHÜSS !!".center(45))
        print("\n\n")
        sys.exit(0)

    def j_n(self):
        """ häufige ja/nein Abfrage """
        j_n = input()
        ja =   ["j", "y", "ja", "yes"]
        if j_n in ja:
            return True
        return False
    def prompt(self):
        """ Prompt- Symbol """
        return " >> "

menu = Vokabeln(path)
