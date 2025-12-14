import tkinter as tk
import random


# PHASE 1 - GAME LOGIC ( reguli, tabla, castigator/remiza )

class TicTacToe:
    def __init__(self):
        # initializare joc
        self.tabla_de_joc = [[" " for coloana in range(3)] for rand in range(3)]
        self.jucator_curent = "X"
        self.joc_terminat = False
        self.castigator = None

    def resetare_joc(self):
        # reseteaza jocul afisand si setand totul la starea initiala
        self.tabla_de_joc = [[" " for coloana in range(3)] for rand in range(3)]
        self.jucator_curent = "X"
        self.joc_terminat = False
        self.castigator = None

    def mutari_disponibile(self):
        # return lista cu perechi (rand, coloana) de celule goale (mutari posibile)
        mutari = []
        for rand in range(3):
            for coloana in range(3):
                if self.tabla_de_joc[rand][coloana] == " ":
                    mutari.append((rand, coloana))
        return mutari

    def afisare_tabla_joc(self):
        # construieste un text pe mai multe linii cu tabla de joc  pentru afisarea in consola
        tabla = self.tabla_de_joc
        return "\n".join([
            f" {tabla[0][0]} | {tabla[0][1]} | {tabla[0][2]} ",
            "-----------",
            f" {tabla[1][0]} | {tabla[1][1]} | {tabla[1][2]} ",
            "-----------",
            f" {tabla[2][0]} | {tabla[2][1]} | {tabla[2][2]} ",
        ])

    def mesaj_status_joc(self):
        # return mesaje de stare: tura jucator curent / castigator / remiza
        if self.castigator:
            return f"Castigator: {self.castigator}"
        if self.joc_terminat:
            return "Remiza!"
        return f"Mutare pentru jucatorul {self.jucator_curent}"

    def gestionare_mutare(self, rand, coloana):
        """
        face o mutare (rand, coloana):
        1 verifica dacq mutarea e validq (celula e goala/mutarea nu e in afara grilei)
        2 pune in grila simbolul jucatorului curent
        3 verifica daca jocul s a terminat (castigator/remiza)
        4 altfel schimba jucatorul curent
        """
        if self.joc_terminat:
            raise ValueError("Jocul s-a terminat.")
        if not (0 <= rand < 3 and 0 <= coloana < 3):
            raise ValueError("Mutarea este in afara tabelei de joc.")
        if self.tabla_de_joc[rand][coloana] != " ":
            raise ValueError("Celula aleasa nu este disponibila.")

        self.tabla_de_joc[rand][coloana] = self.jucator_curent
        self.castigator = self.verificare_castigator()

        if self.castigator:
            self.joc_terminat = True
            return

        if self.verificare_remiza():
            self.joc_terminat = True
            return

        self.jucator_curent = "O" if self.jucator_curent == "X" else "X"

    def verificare_castigator(self):
        """
        verifica toate liniile castigatoare (3 - randuri / 3 - coloane / 2 - diagonale)
        return X / 0 dacă exista castigator
        else return none pentru nu exista castigator
        """

        tabla = self.tabla_de_joc

        # randuri
        for rand in range(3):
            if tabla[rand][0] != " " and tabla[rand][0] == tabla[rand][1] == tabla[rand][2]:
                return tabla[rand][0]

        # coloane
        for coloana in range(3):
            if tabla[0][coloana] != " " and tabla[0][coloana] == tabla[1][coloana] == tabla[2][coloana]:
                return tabla[0][coloana]

        # diagonale
        if tabla[0][0] != " " and tabla[0][0] == tabla[1][1] == tabla[2][2]:
            return tabla[0][0]
        if tabla[0][2] != " " and tabla[0][2] == tabla[1][1] == tabla[2][0]:
            return tabla[0][2]

        return None

    def verificare_remiza(self):
        """
        true = tabla e plina si nu exista niciun castigator
        else false
        """
        return all(self.tabla_de_joc[rand][coloana] != " " for rand in range(3) for coloana in range(3)) and self.verificare_castigator() is None


# PHASE 3 - AI ( random, best - minimax, 3 dificultati: random, random + best, best )

class TicTacToeAI:
    def mutare_dificultate_usor(self, tabla_de_joc):
        mutari_disponibile = []
        for rand in range(3):
            for coloana in range(3):
                if tabla_de_joc[rand][coloana] == " ":
                    mutari_disponibile.append((rand, coloana))
        if not mutari_disponibile:
            return None
        return random.choice(mutari_disponibile)

    # 00 01 02 linia 0
    # 10 11 12 linia 1
    # 20 21 22 linia 2
    def mutare_dificultate_greu(self, tabla_de_joc, jucator_AI="O", jucator_OM="X"):
        mutari_de_testat = [(1,1),(0,0),(0,2),(2,2),(2,0),(0,1),(1,2),(2,1),(1,0)]

        # randuri
        def castigator(tabla_de_joc_ai):
            for rand in range(3):
                if tabla_de_joc_ai[rand][0] != " " and tabla_de_joc_ai[rand][0] == tabla_de_joc_ai[rand][1] == tabla_de_joc_ai[rand][2]:
                    return tabla_de_joc_ai[rand][0]

            # coloane
            for coloana in range(3):
                if tabla_de_joc_ai[0][coloana] != " " and tabla_de_joc_ai[0][coloana] == tabla_de_joc_ai[1][coloana] == tabla_de_joc_ai[2][coloana]:
                    return tabla_de_joc_ai[0][coloana]

            # diagonale
            # diagonala principala
            if tabla_de_joc_ai[0][0] != " " and tabla_de_joc_ai[0][0] == tabla_de_joc_ai[1][1] == tabla_de_joc_ai[2][2]:
                return tabla_de_joc_ai[0][0]

            # diagonala secundara
            if tabla_de_joc_ai[0][2] != " " and tabla_de_joc_ai[0][2] == tabla_de_joc_ai[1][1] == tabla_de_joc_ai[2][0]:
                return tabla_de_joc_ai[0][2]

            return None

        def remiza(tabla_de_joc_ai):
            return all(tabla_de_joc_ai[rand][coloana] != " " for rand in range(3) for coloana in range(3)) and castigator(tabla_de_joc_ai) is None

        def algoritm_minimax(tabla_de_joc_ai, jucator_CURENT):
            castigator_verificat = castigator(tabla_de_joc_ai)

            if castigator_verificat == jucator_AI:
                return 1, None
            if castigator_verificat == jucator_OM:
                return -1, None
            if remiza(tabla_de_joc_ai):
                return 0, None

            mutari_disponibile_minimax = [(rand,coloana) for (rand,coloana) in mutari_de_testat if tabla_de_joc_ai[rand][coloana] == " "]

            if jucator_CURENT == jucator_AI:
                mutare_finala = None
                scor_maxim = -99999

                for (rand, coloana) in mutari_disponibile_minimax:
                    tabla_de_joc_ai[rand][coloana] = jucator_AI
                    rezultat_minimax = algoritm_minimax(tabla_de_joc_ai, jucator_OM)
                    scor_rezultat = rezultat_minimax[0]
                    tabla_de_joc_ai[rand][coloana] = " "
                    if scor_rezultat > scor_maxim:
                        scor_maxim = scor_rezultat
                        mutare_finala = (rand, coloana)
                return scor_maxim, mutare_finala

            else:
                mutare_finala = None
                scor_minim = 99999

                for (rand, coloana) in mutari_disponibile_minimax:
                    tabla_de_joc_ai[rand][coloana] = jucator_OM  # muta omul
                    rezultat_minimax = algoritm_minimax(tabla_de_joc_ai, jucator_AI)
                    scor_rezultat = rezultat_minimax[0]
                    tabla_de_joc_ai[rand][coloana] = " "
                    if scor_rezultat < scor_minim:
                        scor_minim = scor_rezultat
                        mutare_finala = (rand, coloana)
                return scor_minim, mutare_finala

        rezultat_final_minimax = algoritm_minimax(tabla_de_joc, jucator_AI)
        mutare_finala = rezultat_final_minimax[1]
        return mutare_finala

    def strategie_AI(self, tabla_de_joc, dificultate_joc, jucator_AI="O", jucator_OM="X"):
        # aplica mutarile pentru fiecare dificultate + logica de alternare la mediu
        # usor mediu greu
        if dificultate_joc == "usor":
            return self.mutare_dificultate_usor(tabla_de_joc)

        if dificultate_joc == "mediu":
            mutari_facute_ai = sum(1 for rand in range(3) for coloana in range(3) if tabla_de_joc[rand][coloana] == jucator_AI)
            if mutari_facute_ai % 2 == 0:
                return self.mutare_dificultate_usor(tabla_de_joc) # nr de piese par pe tabla = mutare random
            else:
                return self.mutare_dificultate_greu(tabla_de_joc, jucator_AI, jucator_OM)

        if dificultate_joc == "greu":
            return self.mutare_dificultate_greu(tabla_de_joc, jucator_AI, jucator_OM)



# PHASE 2 - GUI

class TicTacToeGUI:
    def __init__(self, fereastra_principala: tk.Tk):
        # setari generale fereastra principala - titlu + dimensiune + redimensionare dezactivata (de facut: sa schimb setarile pt fullscreen)
        self.fereastra_principala = fereastra_principala
        self.fereastra_principala.title("TIC TAC TOE")
        self.fereastra_principala.geometry("500x500")  # latime x inaltime
        self.fereastra_principala.resizable(False, False)


        # creare status bar: afiseaza randul jucatorului curent + mesaj final (castigator/remiza) + alte mesaje la schimbarea ferestrelor
        self.mesaj_status_bar = tk.StringVar(value="Meniu")
        self.eticheta_status_bar = tk.Label(
            fereastra_principala,
            textvariable=self.mesaj_status_bar,
            font=("Arial", 18, "bold")
        )
        self.eticheta_status_bar.pack(pady=(10, 10))


        self.depozit_ferestre = tk.Frame(self.fereastra_principala)
        self.depozit_ferestre.pack(expand=True, fill="both")



        # partea de JOC propriu zs + integrare AI

        self.joc_ai = TicTacToeAI()
        self.joc = TicTacToe()
        self.dificultate_joc = None   # usor / mediu / greu
        self.jucator_OM = "X"
        self.jucator_AI = "O"
        self.dificultate_selectata_joc = None    # "om_vs_ai / om_vs_om : to do alte nume de afisat

        self.grila = None
        self.butoane_grila = None

        self.afisare_meniu_principal()


    # functia pentru schimbarea ferestrei
    # in depozit_ferestre redesenez o fereastra si o pastrez pana trebuie sa o sterg ca sa afisez alta
    def stergere_fereastra_curenta(self):
        for fereastra_curenta in self.depozit_ferestre.winfo_children():
            fereastra_curenta.destroy()


    # fereastra 1: meniu principal cu 2 butoane
    #

    def afisare_meniu_principal(self):
        self.stergere_fereastra_curenta()
        self.mesaj_status_bar.set("Meniu")
        self.eticheta_status_bar.config(fg="black")

        buton_1_jucator = tk.Button(
            self.depozit_ferestre,
            text="1 jucător\n om vs ai",
            command=self.afisare_meniu_dificultate_ai,
            font=("Arial", 14, "bold"),
            width=25,
            height=2
        )
        buton_1_jucator.pack(ipadx=20, ipady=20, pady=70, anchor=tk.N)

        buton_2_jucatori = tk.Button(
            self.depozit_ferestre,
            text="2 jucători\n om vs om",
            command=lambda: self.pornire_joc(dificultate_selectata_joc="om_vs_om", dificultate_joc=None),
            font=("Arial", 14, "bold"),
            width=25,
            height=2
        )
        buton_2_jucatori.pack(ipadx=20, ipady=20, pady=10, anchor=tk.S)


    # fereastra 2: meniul de  dificultate pt ai cu 4 butoane in total, de vazut cum le redimensionez pentru phase 4
    # to do: rearanjare butoane de dificultate in linie cu butonul de meniu sub ele la mijloc
    def afisare_meniu_dificultate_ai(self):
        self.stergere_fereastra_curenta()
        self.mesaj_status_bar.set("Alege dificultatea jocului")
        self.eticheta_status_bar.config(fg="black")

        buton_dificultate_usor = tk.Button(
            self.depozit_ferestre,
            text="Ușor",
            command=lambda: self.pornire_joc(dificultate_selectata_joc="om_vs_ai", dificultate_joc="usor"),
            font=("Arial", 14, "bold"),
            width=20,
            height=2
        )
        buton_dificultate_usor.pack(side="bottom", ipadx=20, ipady=20, pady=6)

        buton_dificultate_mediu = tk.Button(
            self.depozit_ferestre,
            text="Mediu",
            command=lambda: self.pornire_joc(dificultate_selectata_joc="om_vs_ai", dificultate_joc="mediu"),
            font=("Arial", 14, "bold"),
            width=20,
            height=2
        )
        buton_dificultate_mediu.pack(side="bottom", ipadx=20, ipady=20, pady=6)

        buton_dificultate_greu = tk.Button(
            self.depozit_ferestre,
            text="Greu",
            command=lambda: self.pornire_joc(dificultate_selectata_joc="om_vs_ai", dificultate_joc="greu"),
            font=("Arial", 14, "bold"),
            width=20,
            height=2
        )
        buton_dificultate_greu.pack(side="bottom", ipadx=20, ipady=20, pady=6)

        buton_meniu = tk.Button(
            self.depozit_ferestre,
            text="Meniu",
            command=self.afisare_meniu_principal,
            font=("Arial", 14, "bold"),
            width=20,
            height=2
        )
        buton_meniu.pack(side="top", ipadx=20, ipady=20, pady=(20, 0))


    # fereastra 3: grila pentru tabla indiferent de modul de joc + buton meniu si buton joaca din nou

    def pornire_joc(self, dificultate_selectata_joc, dificultate_joc):
        self.stergere_fereastra_curenta()
        self.dificultate_selectata_joc = dificultate_selectata_joc
        self.dificultate_joc = dificultate_joc
        self.joc.resetare_joc()

        #
        self.grila = tk.Frame(self.depozit_ferestre)
        self.grila.pack(pady=10)

        """
        creez butoanele de pe grila
        fiecare buton comanda o mutare la click
        """
        self.butoane_grila = [[None for _ in range(3)] for _ in range(3)]
        for rand in range(3):
            for coloana in range(3):
                # cand se da click pe celula se apeleaza apasa_celula(r, c)
                buton_grila = tk.Button(
                    self.grila,
                    text="",
                    font=("Arial", 18, "bold"),
                    width=6,
                    height=3,
                    command=lambda r=rand, c=coloana: self.apasa_celula(r, c)
                )
                buton_grila.grid(row=rand, column=coloana, padx=3, pady=3)
                self.butoane_grila[rand][coloana] = buton_grila

        # butoane din partea de jos a tablei in bottom: joaca din nou + meniu
        self.partea_de_jos_tabla = tk.Frame(self.depozit_ferestre)
        self.partea_de_jos_tabla.pack(side="bottom", fill="x", padx=10, pady=(10, 15))


        self.buton_resetare = tk.Button(
            self.partea_de_jos_tabla,
            text="Joacă din nou",
            command=self.resetare,
            font=("Arial", 15, "bold"),
            width=20,
            height=2
        )
        self.buton_resetare.pack(side="right")

        self.buton_meniu = tk.Button(
            self.partea_de_jos_tabla,
            text="Meniu",
            command=self.afisare_meniu_principal,
            font=("Arial", 15, "bold"),
            width=20,
            height=2
        )
        self.buton_meniu.pack(side="left")

        self.actualizare_ui()



    def apasa_celula(self, rand: int, coloana: int) -> None:
        """
        verifica cazurile in care butoanele nu pot fi apsate
        face mutarea user ului, face mutarea ai ului dupa 700 ms dupa ce a mutat user ul
        """

        # ignora click ul daca jocul e terminat
        if self.joc.joc_terminat:
            return

        # cand muta ai ul user ul nu poate muta, deci nu se da click
        if self.dificultate_selectata_joc == "om_vs_ai" and self.joc.jucator_curent != self.jucator_OM:
            return

        # ignora click ul pe o celula care nu e goala
        if self.joc.tabla_de_joc[rand][coloana] != " ":
            return

        # aplica mutarea player ului
        try:
            self.joc.gestionare_mutare(rand, coloana)
        except ValueError:
            return

        if self.dificultate_selectata_joc == "om_vs_ai" and (not self.joc.joc_terminat):
            self.fereastra_principala.after(700, self.mutare_ai)

        self.actualizare_ui()



    def mutare_ai(self):
        """
        verific daca ai ul are voie sa mute acum si e tura lui
        calculeaza mutarea pe care o face in functie de dificultate folosind strategie_AI
        actualizeaza tabla din fereastra cu mutarea aleasa
        """

        if self.joc.joc_terminat:
            return

        if self.joc.jucator_curent != self.jucator_AI:
            return

        mutare = self.joc_ai.strategie_AI(self.joc.tabla_de_joc, self.dificultate_joc, jucator_AI = self.jucator_AI, jucator_OM = self.jucator_OM)

        if mutare is None:
            return

        rand, coloana = mutare
        try:
            self.joc.gestionare_mutare(rand, coloana)
        except ValueError:
            return

        self.actualizare_ui()


    def actualizare_ui(self) -> None:
        # update pe tabla de joc live
        for rand in range(3):
            for coloana in range(3):
                valoare_de_pus_in_celula = self.joc.tabla_de_joc[rand][coloana]
                self.butoane_grila[rand][coloana].config(text="" if valoare_de_pus_in_celula == " " else valoare_de_pus_in_celula)

                # highlither x sau 0
                if valoare_de_pus_in_celula in ("X", "O"):
                    # culori in caz de remiza
                    if self.joc.joc_terminat and self.joc.castigator is None:
                        culoare = "#9527F5" if valoare_de_pus_in_celula == "X" else "green"

                    # culoare joc in desfasurare / victorie
                    else:
                        if valoare_de_pus_in_celula == self.joc.jucator_curent:
                            culoare = "#9527F5" if valoare_de_pus_in_celula == "X" else "green"
                        else:
                            culoare = "black"

                    self.butoane_grila[rand][coloana].config(fg=culoare, disabledforeground=culoare)
                else:
                    self.butoane_grila[rand][coloana].config(fg="black", disabledforeground="black")

                if self.joc.joc_terminat:
                    self.butoane_grila[rand][coloana].config(state=tk.DISABLED)
                else:
                    self.butoane_grila[rand][coloana].config(state=tk.DISABLED if valoare_de_pus_in_celula != " " else tk.NORMAL)


        # actualizare status bar jucator curent si mesaj final castigator/remiza
        if not self.joc.joc_terminat:
            self.mesaj_status_bar.set(f"Jucător curent: {self.joc.jucator_curent}")
            self.eticheta_status_bar.config(fg="#9527F5" if self.joc.jucator_curent == "X" else "green")
        else:
            self.mesaj_status_bar.set(self.joc.mesaj_status_joc())
            if self.joc.castigator == "X":
                self.eticheta_status_bar.config(fg="#9527F5")
            else:
                if self.joc.castigator == "O":
                    self.eticheta_status_bar.config(fg="green")
                else:
                    self.eticheta_status_bar.config(fg="black")

    # cand se apasa butonul "joaca din nou" se apeleaza resetare
    def resetare(self) -> None:
        self.joc.resetare_joc()
        self.actualizare_ui()


# functii de pornire consola si gui

def run_consola():
    joc = TicTacToe()
    print("Pentru jocul Tic Tac Toe, introdu doua numere pentru rand, respectiv coloana, de la 1 la 3. Exemplu: 2 3\n")
    print(joc.afisare_tabla_joc())

    while not joc.joc_terminat:
        input_utilizator = input(f"\n{joc.mesaj_status_joc()} | Introdu mutarea ta: ").strip()
        try:
            rand_str, coloana_str = input_utilizator.split()
            rand, coloana = int(rand_str) - 1, int(coloana_str) - 1 # incep de la 0
            joc.gestionare_mutare(rand, coloana)
            print("\n" + joc.afisare_tabla_joc())
        except ValueError as e:
            print(f"Eroare: {e}")
        except Exception:
            print("Input invalid. Exemplu input: 1 1")

    print("\n" + joc.mesaj_status_joc())

def run_gui():
    fereastra_principala = tk.Tk()
    TicTacToeGUI(fereastra_principala)
    fereastra_principala.mainloop()

# meniul de start

if __name__ == "__main__":

    while(True):
        print("Alege modul de joc:")
        print("1 - Interfata grafica")
        print("2 - Consola")

        alegere_joc = input("Introdu 1 sau 2: ").strip()

        if alegere_joc == "1":
            run_gui()
        else:
            if alegere_joc == "2":
                run_consola()
            else:
                print("Input invalid. Incearca din nou.\n")