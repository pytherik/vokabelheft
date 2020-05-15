from datetime import datetime
import re
from pathlib import Path
from os import system
from random import randint
import sys
import csv
gesamt_heute  = 0
richtig_heute = 0
falsch_heute  = 0
hinzugefügt   = 0

path_csv = Path.home()/"CODE/DATA/VOK/voxnscore.csv"
path_data = Path.home()/"CODE/DATA/VOK/stats.csv"

class Vokabeln:
    """ Vokabeltrainer """
    
    title = (chr(1422) * 45 + "\n" +
         chr(1422) +"\033[33m" + "VOKABELHEFT".center(43) + "\033[0m" +
         chr(1421) + "\n" + chr(1421) *45)
    fremd = []       # Vok. Fremdsprache  (path_csv)
    deutsch = []     # Vok. Deutsch       (path_csv)
    meta = []        # link zu Statistik  (path_csv)  (Erstelldatum)
    score = []       # Scoring            (path_csv)
    found = []       # Suchindizes
    stats = []       # Statistikdaten     (path_data)
    def __init__(self):#, path):
        """ Textdatei einlesen und aufteilen """
        with path_data.open("r") as data:
            reader = csv.reader(data)
            for line in reader:
                self.stats.append(line)
        with path_csv.open("r") as vok:
            reader = csv.reader(vok)
            for line in reader:
                line = line[:-3]+[int(score) for score in line[-3:]]
                self.fremd.append(line[0])
                self.deutsch.append(line[1:-4])
                self.meta.append(line[-4])
                self.score.append(line[-3:])
        
    def statistik(self):
        """ macht Statistik """
        YYYY, MM, DD, hh, mm =re.split("\W",str(datetime.today()))[:-2]
        if len(hh) == 1:
            hh = "0" + hh
        if len(mm) == 1:
            mm = "0" + hh
        anz_vok = len(self.fremd)
        gesamt  = 0
        richtig = 0
        falsch  = 0
        for index in range(len(self.fremd)):
            gesamt  += self.score[index][0]
            richtig += self.score[index][1]
            falsch  += self.score[index][2]
        return (anz_vok, gesamt, richtig, falsch, YYYY, MM, DD, hh, mm)
    
    def menu(self):
        """ Startseite, Auswahlmenu """
        system("clear")
    
        self.check_date()
        print(self.title)
        data = self.statistik()
        
        print(f"\n{data[6]}.{data[5]}.{data[4]}    Sammlung gesamt:{str(data[0]).rjust(5)}", end = "")           
        print(f"    {data[7]}:{data[8]}")
        if not hinzugefügt:
            print("\n\n")
        else:
            print(f"Hinzugefügt    :{str(hinzugefügt).rjust(5)}\n") 
        print("_" * 45)
        print(f"Abfragen gesamt:{str(data[1]).rjust(5)}   heute:{str(gesamt_heute).rjust(3)}\n")
        print(f"richtig  gesamt:{str(data[2]).rjust(5)}   heute:{str(richtig_heute).rjust(3)}")
        print(f"falsch   gesamt:{str(data[3]).rjust(5)}   heute:{str(falsch_heute).rjust(3)}")
        print("" + ("_" * 45))
        print("\n<1> Abfragen")
        print("\n<2> Nachschlagen")
        print("\n<3> Neue Vokabel")
        print("\n<4> Bearbeiten")
        print("\n<5> BEENDEN")
        print("\n>", end = "")
        wahl = 0
        while wahl not in (1, 2, 3, 4, 5, 42) or wahl == "":
            try:
                wahl = int(input())
            except ValueError:
                print(">1 - 5<", end ="\n>")
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

    def trans(self,vok, hamwa=False):
        """ gibt alle Übersetzungen aus """
        found = self.find(vok)
        if not found:
            print("Nicht vorhanden")
            return False
        for index in found:
            if len(found[found.index(index):]) > 3:
                i = (len(found)+1) - len(found[found.index(index):]) 
                if not i % 4:
                    print("<enter>", end = "")
                    weiter = input()
                    system("clear")
                    print(self.title)
                    print("\n\n\n")
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
        print()
                
    def lernen(self):
        """ Vokabeln abfragen """
        system("clear")
        self.check_date()
        print(self.title)
        
        global gesamt_heute
        global richtig_heute
        global falsch_heute

        gesamt_heute += 1
        ran = randint(0, len(self.fremd)-1)
        print("\n\n" + chr(717) * 45)
        print(f"Was heißt '{self.fremd[ran]}' auf deutsch ?".center(45))
        print(chr(713) * 45)
        if self.score[ran][0] != 0:
            print(f"Schon {self.score[ran][1]} mal richtig und {self.score[ran][2]}mal falsch!")
        print("\n", end = self.prompt())

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
        self.check_date()
        data = self.statistik()
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
                i = ((len(found)+1) - len(found[found.index(index):]))
                if i > 3:
                    if not i % 4:
                        print("<enter>", end = "")
                        weiter = input()
                        system("clear")
                        print(self.title)
                        print("\n\n\n")
                if int(self.meta[index]) > len(self.stats)-1 or self.stats[int(self.meta[index])][6] == data[6]:
                    print("geändert heute.")
                elif self.meta[index] == "0" or self.meta[index] == 0:
                    print("geändert vor dem 10.05.2020")
                else:
                    vom = self.stats[int(self.meta[index])]
                    print(f"Eintrag vom {vom[-3]}.{vom[-4]}.{vom[-5]}")
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
        self.check_date()
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
                self.trans(vok, hamwa = True)
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
                self.menu()                   # nichts geändert
            elif not bedeutung:
                save = True
                self.behalten(fremd, deutsch) # wird aufgenommen
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
        heute = len(self.stats)
        system("clear")

        print(self.title)
        print("\n\n" + chr(717) * 45)
        print("Möchtest du den Eintrag so übernehmen ?".center(45))
        print(chr(713) * 45)
        print()   
        self.anzeigen(fremd, deutsch)
        self.fremd.append(fremd)
        self.deutsch.append(deutsch)
        self.meta.append(heute)
        self.score.append([0, 0, 0])
        print("\nAlles O.K. (j/n) ?", end = self.prompt())
        if not self.j_n():
            self.aendern(index=len(self.fremd)-1, neue_vok=True)
        hinzugefügt += 1
        self.ende(neu=True)
            
    def bearbeiten(self, ran=False, dazu=False, neue_vok=False):
        """ Eintrag ändern (erweitern, löschen) """
        system("clear")

        print(self.title)
        global richtig_heute
        global falsch_heute
        global hinzugefügt
        
        if ran and dazu:
            self.deutsch[ran].append(dazu)
            self.anzeigen(self.fremd[ran], self.deutsch[ran])
            print("\nGefällt's dir so (j/n)?", end = self.prompt())
            janein = self.j_n()
            if not janein and neue_vok:         # bei Unzufriedenheit
                self.aendern(ran, neue_vok)     # zu den Änderungsoptionen 
            elif not janein and not neue_vok:
                self.deutsch[ran].pop()
                self.bearbeiten(ran)
            elif neue_vok:
                self.meta[ran] = len(self.stats)
                self.menu()
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
        """ ändern oder anlegen ? """
        system("clear")
        print(self.title)
        
        if not vok:                                 # neue Suche im Heft
            print("\n\n" + chr(717) * 45)
            print("Gib das Wort ein, das du ändern möchtest.".center(45))
            print(chr(713) * 45)
            print("\n", end = self.prompt())
            vok = input()
            if not vok:
                self.menu()
            found = self.find(vok)
            if not found:                           # nicht drin, kann angelegt werden
                print(f"\n'{vok}' ist noch nicht im Heft !")
                print("\nDu kannst es jetzt hinzufügen (j/n).",end = self.prompt())
                if  not self.j_n():
                    self.menu()                     # soll nicht rein 
                else:
                    self.aendern2(vok)              # soll rein
            if len(found) > 1:
                if found:
                    print()
                    for index in found:
                        i = ((len(found)+1) - len(found[found.index(index):]))
                        if i > 3:
                            if not i % 4:           # 4 Vok pro Seite anz.
                                print("<enter>", end = "")
                                weiter = input()
                                system("clear")
                                print(self.title)
                                print("\n\n\n")
                                                    # Änderugsdatum abfragen
                        if int(self.meta[index]) > len(self.stats)-1:
                            print(f"<{found.index(index)+1}>  ", end = "")
                            print("geändert heute.")
                        elif self.meta[index] == "0" or self.meta[index] == 0:
                            print(f"<{found.index(index)+1}>  ", end = "")
                            print("geändert vor dem 10.05.2020")
                        else:
                            vom = self.stats[int(self.meta[index])]
                            print(f"<{found.index(index)+1}>  ", end = "")
                            print(f"Eintrag vom {vom[-3]}.{vom[-4]}.{vom[-5]}")
                        self.anzeigen(self.fremd[index], self.deutsch[index])                        
                print("\nWelchen Eintrag möchtest du ändern ?\n")
                print(f"<1> - <{len(found)}>", end = "")
                nr = 0
                while nr < 1 or nr > len(found):
                    try:
                        nr = int(input())           # Auswahl aus Anz. gefundener
                    except ValueError:
                        print(f"<1> - <{len(found)}>", end = "")
                        nr = 0
                self.aendern(index = found[nr - 1])
            else:
                self.aendern(index = found[0])       
                                                     # Anlegen nach gescheiterter Suche
        print(f"\n\n\nIst {vok} das englische Wort ?", end = self.prompt())
        if self.j_n():
            self.anlegen(vok)                        # Anlegen normal
        else:
            self.anlegen(vok, 2)                     # Anlegen als Bedeutung 1
        
    def aendern(self, index, neue_vok=False):        # ändert Eintrag[index] oder
        system("clear")                              # new_vok = neu anzulegenden Eintr.
        global hinzugefügt
        self.check_date()
        
        print(self.title)
        print("\n\n")
        self.anzeigen(self.fremd[index], self.deutsch[index])
        print("\nmöchtest du: \n\n<1> den Eintrag löschen")
        print("<2> Bedeutung hinzfügen")
        print("<3> Bedeutung ändern/ löschen")
        print("\n>", end = "")     
        nr = input()
        if not nr or nr not in ["1", "2", "3"]:
            if neue_vok:
                hinzugefügt += 1
            self.menu()
        elif nr == "1":
            print("\nSicher (j/n) ? ", end = self.prompt())
            if not self.j_n():
                self.aendern(index)
            del self.deutsch[index]
            del self.fremd[index]
            del self.meta[index]
            del self.score[index]
            print("\nDer Eintrag ist gelöscht !\n\nweiter mit <enter>", end = "")
            weiter = input()
            self.menu()
        elif nr == "2":
            system("clear")

            print(self.title)
            self.anzeigen(self.fremd[index], self.deutsch[index])
            print(f"\nBedeutung {len(self.deutsch[index])+1}        :", end = self.prompt())
            bedeutung = input()
            if bedeutung:
                self.bearbeiten(index, bedeutung, neue_vok=True)
            else:
                self.aendern(index, neue_vok=True)
        elif nr == "3":
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
            print(f"\nWelche Bedeutung <1> - <{i}> ?", end = self.prompt())
            nr = input()
            
            if nr not in x:
                self.aendern(index, neue_vok=True)
            else:
                weg = self.deutsch[index][int(nr)-1]
                print(f"\n   Soso, {weg} ist also falsch ... ")
                print("\nRichtig wäre dann :")
                print("Löschen mit <enter>     ", end = self.prompt())
                behalten = input()
                if not behalten:
                    self.deutsch[index].remove(weg)
                else:
                    self.deutsch[index][int(nr)-1]= behalten
                self.anzeigen(self.fremd[index], self.deutsch[index])
                print("\nOkay so ?", end = self.prompt())
                if self.j_n():
                    self.menu()
                if not self.j_n() and not behalten:
                    self.deutsch[index].insert(int(nr) - 1, weg)
                    self.aendern(index, neue_vok=True)
                elif not self.j_n():
                    self.deutsch[index][int(nr)-1] = weg
                    self.aendern(index, neue_vok=True)
                if neue_vok:
                    hinzugefügt +=1
                self.menu()

    def score_löschen(self):
        """ löscht das Internet """
        self.score = []
        for null in range(len(self.fremd)):
            self.score.append([0, 0, 0])
        self.menu()
    def check_date(self):
        """ prüft Datumswechsel währen der Sitzung """
        global start
        data = self.statistik()
        
        if data[-3] != start[-3]:      # wenn neues Datum
            self.ende(data)
        else:
            return
     
    def ende(self, neu=False):
        """ Programm beenden, Statistik anzeigen und speichern """
        system("clear")
        
        new = self.statistik()           
        with path_data.open("a") as data:
            writer = csv.writer(data)
            writer.writerow(new)
        print(len(self.meta))
            
        neu_score = []    
        with path_csv.open("w") as csv_score:
            writer = csv.writer(csv_score)
            for i in range(len(self.fremd)):
                line = [self.fremd[i]]
                line += (de for de in self.deutsch[i])
                line += [self.meta[i]]     # Metalink zum stats Eintrag
                line += (sc for sc in self.score[i])
                neu_score.append(line)                       
            writer.writerows(neu_score)
        if neu:
            system("clear")
            print(self.title)
            print("\n\n" + chr(1421) * 45)
            print("g e s p e i c h e r t".center(45))
            print(chr(1421) * 45)
            #print("\n\n<enter>", end = "")
            weiter = input
            return
        else:
            system("clear")
            print(self.title)
            print("\n\n" + chr(1421) * 45)
            print("g e s p e i c h e r t".center(45))
            print(chr(1421) * 45)
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

menu = Vokabeln()
start = menu.statistik()
menu.menu()
