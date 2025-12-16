import tkinter as tk
import random

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
            return f"Câștigător: {self.castigator}"
        if self.joc_terminat:
            return "Remiză!"
        return f"Mutare pentru jucătorul {self.jucator_curent}"

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

class TicTacToeGUI:
    def __init__(self, fereastra_principala: tk.Tk):
        # initializari fereastra principala
        self.fereastra_principala = fereastra_principala
        self.fereastra_principala.title("X și O")
        self.fereastra_principala.geometry("1000x1000")  # dimensiune: latime x inaltime
        self.fereastra_principala.resizable(True, True)

        self.joc_ai = TicTacToeAI()
        self.joc = TicTacToe()

        """
        # crearea status bar din partea de sus a ferestrelor:
        setez textul Meniu pentru a fi afisat in prima fereastra
        in celelalte ferestre mesaj_status_bar va fi actualizat cu alte texte folosind .set
        eticheta_status_bar afiseaza textul din variabila mesaj_status_bar
        cu .pack afisez eticheta mesajului in fereastra ca sa devin textul vizibil
        """
        self.mesaj_status_bar = tk.StringVar(value="Meniu")
        self.eticheta_status_bar = tk.Label(
            fereastra_principala,
            textvariable=self.mesaj_status_bar,
            font=("Arial", 20, "bold")
        )
        self.eticheta_status_bar.pack(pady=(10, 10))

        """
        creez un container depozit_fereste in fereastra_principala
        ca sa pot sa sterg ce am in fereastra curenta si
        sa trec la urmatoarea punand butoanele si ce imi trebuie pentru urmatoarea fereastra
        """
        self.depozit_ferestre = tk.Frame(self.fereastra_principala)
        self.depozit_ferestre.pack(expand=True, fill="both")

        self.zona_comuna_scor_grila = None
        self.grila = None
        self.butoane_grila = None
        self.tabla_scor = None
        self.buton_scor_jucator_O = None
        self.eticheta_scor_jucator_O = tk.StringVar()
        self.buton_scor_jucator_X = None
        self.eticheta_scor_jucator_X = tk.StringVar()
        self.buton_scor_remiza = None
        self.eticheta_scor_remiza = tk.StringVar()

        self.partea_de_jos_tabla = None
        self.buton_resetare = None
        self.buton_meniu = None

        # initializari de variabile pentru dificultati impotriva AI
        self.dificultate_joc = None  # usor / mediu / greu
        self.jucator_OM = "X"
        self.jucator_AI = "O"
        self.dificultate_selectata_joc = None  # 1 jucator: om_vs_ai / 2 jucatori: om_vs_om

        # initializari de variabile pentru scor
        self.scor_castigator_X = 0
        self.scor_castigator_O = 0
        self.scor_remiza = 0
        self.am_numarat_runda_curenta = False

        # fereastra pop up pentru a juca din nou sau a inchide jocul
        self.pop_up_joaca_din_nou_deschis = False

        self.fereastra_1_meniu_principal()

    """
    fereastra pop up cu intrebarea de a juca din nou
    si 2 butoane pentru a opri jocul de tot
    sau pentru a juca din nou in acelasi mod de joc deja selectat din meniu
    si optiunea de a o inchide din x fara a selecta niciun buton
    """
    def pop_up_joaca_din_nou(self):
        if self.pop_up_joaca_din_nou_deschis:
            return
        self.pop_up_joaca_din_nou_deschis = True

        fereastra_pop_up = tk.Toplevel(self.fereastra_principala)
        fereastra_pop_up.title("Meci terminat")
        fereastra_pop_up.geometry("350x160")
        fereastra_pop_up.resizable(False, False)
        fereastra_pop_up.transient(self.fereastra_principala)
        # blochez apasarile pe fereastra principala cat timp fereastra pop up e deschisa
        fereastra_pop_up.grab_set()

        mesaj_fereastra_pop_up = tk.Label(
            fereastra_pop_up,
            text="Vrei să mai joci o dată?",
            font=("Arial", 14, "bold")
        )
        mesaj_fereastra_pop_up.pack(pady=15)

        butoane_fereastra_pop_up = tk.Frame(fereastra_pop_up)
        butoane_fereastra_pop_up.pack(pady=10)

        def joaca_din_nou():
            self.pop_up_joaca_din_nou_deschis = False
            fereastra_pop_up.destroy()
            self.resetare()

        tk.Button(
            butoane_fereastra_pop_up,
            text="Play again",
            font=("Arial", 12, "bold"),
            width=12,
            command=joaca_din_nou
        ).pack(side="right", padx=10)

        def inchidere_joc():
            self.pop_up_joaca_din_nou_deschis = False
            fereastra_pop_up.destroy()
            self.fereastra_principala.quit()
            self.fereastra_principala.destroy()

        tk.Button(
            butoane_fereastra_pop_up,
            text="Exit game",
            font=("Arial", 12, "bold"),
            width=12,
            command=inchidere_joc).pack(side="left", padx=10)

        def inchidere_fereastra_pop_up_cu_x():
            self.pop_up_joaca_din_nou_deschis = False
            fereastra_pop_up.destroy()

        fereastra_pop_up.protocol("WM_DELETE_WINDOW", inchidere_fereastra_pop_up_cu_x)

    def actualizare_scor(self):
        if not self.joc.joc_terminat or self.am_numarat_runda_curenta:
            return
        self.am_numarat_runda_curenta = True

        if self.joc.castigator == "X":
            self.scor_castigator_X += 1
            self.eticheta_scor_jucator_X.set(f"Jucător X\n{self.scor_castigator_X}")
        else:
            if self.joc.castigator == "O":
                self.scor_castigator_O += 1
                self.eticheta_scor_jucator_O.set(f"Jucător O\n{self.scor_castigator_O}")
            else:
                self.scor_remiza += 1
                self.eticheta_scor_remiza.set(f"Remiză\n{self.scor_remiza}")

    def resetare_scor(self):
        self.scor_castigator_X = 0
        self.eticheta_scor_jucator_X.set("Jucător X\n0")
        self.scor_castigator_O = 0
        self.eticheta_scor_jucator_O.set("Jucător O\n0")
        self.scor_remiza = 0
        self.eticheta_scor_remiza.set("Remiză\n0")
        self.am_numarat_runda_curenta = False

    """
    functia pentru schimbarea ferestrei pe care vreau sa o afisez pe ecran
    in depozit_ferestre retin butoane, grile etc
    si ca sa trec la alta fereastra sterg tot ce era in cea curenta
    #si dupa in cea noua pun butoanele etc care imi trebuie in prezent
    """
    def stergere_fereastra_curenta(self):
        for fereastra_curenta in self.depozit_ferestre.winfo_children():
            fereastra_curenta.destroy()

    """
    fereastra 1: meniu principal cu 2 butoane:
    buton 1 jucator pentru optiunea de a juca contra ai
    buton 2 jucatori pentru optiunea de a juca cu alta persoana fizic
    """
    def fereastra_1_meniu_principal(self):
        self.stergere_fereastra_curenta()
        self.mesaj_status_bar.set("MENIU PRINCIPAL")
        self.eticheta_status_bar.config(fg="black")

        buton_1_jucator = tk.Button(
            self.depozit_ferestre,
            text="1 JUCĂTOR\n vs AI",
            command=self.fereastra_2_meniu_dificultate_ai,
            font=("Arial", 16, "bold"),
            width=25,
            height=5
        )
        buton_1_jucator.pack(ipadx=20, ipady=20, pady=100, anchor=tk.N)

        buton_2_jucatori = tk.Button(
            self.depozit_ferestre,
            text="2 JUCĂTORI",
            command=lambda: self.fereastra_3_jocul_pornit(dificultate_selectata_joc="om_vs_om", dificultate_joc=None),
            font=("Arial", 16, "bold"),
            width=25,
            height=5
        )
        buton_2_jucatori.pack(ipadx=20, ipady=20, pady=10, anchor=tk.S)

    """
    # fereastra 2: meniul de dificultate pt ai cu 4 butoane:
    buton dificultate usor
    buton dificultate mediu
    """
    def fereastra_2_meniu_dificultate_ai(self):
        self.stergere_fereastra_curenta()
        self.mesaj_status_bar.set("MENIU DIFICULTĂȚI")
        self.eticheta_status_bar.config(fg="black")

        buton_dificultate_usor = tk.Button(
            self.depozit_ferestre,
            text="UȘOR",
            command=lambda: self.fereastra_3_jocul_pornit(dificultate_selectata_joc="om_vs_ai", dificultate_joc="usor"),
            font=("Arial", 16, "bold"),
            width=25,
            height=5
        )
        buton_dificultate_usor.pack(side="bottom", ipadx=20, ipady=20, pady=6)

        buton_dificultate_mediu = tk.Button(
            self.depozit_ferestre,
            text="MEDIU",
            command=lambda: self.fereastra_3_jocul_pornit(dificultate_selectata_joc="om_vs_ai", dificultate_joc="mediu"),
            font=("Arial", 16, "bold"),
            width=25,
            height=5
        )
        buton_dificultate_mediu.pack(side="bottom", ipadx=20, ipady=20, pady=6)

        buton_dificultate_greu = tk.Button(
            self.depozit_ferestre,
            text="GREU",
            command=lambda: self.fereastra_3_jocul_pornit(dificultate_selectata_joc="om_vs_ai", dificultate_joc="greu"),
            font=("Arial", 16, "bold"),
            width=25,
            height=5
        )
        buton_dificultate_greu.pack(side="bottom", ipadx=20, ipady=20, pady=6)

        buton_meniu = tk.Button(
            self.depozit_ferestre,
            text="MENIU",
            command=self.fereastra_1_meniu_principal,
            font=("Arial", 16, "bold"),
            width=30,
            height=5
        )
        buton_meniu.pack(side="top", ipadx=20, ipady=20, pady=(20, 0))

    """
    # fereastra 3: grila pentru tabla indiferent de modul de joc + buton meniu si buton joaca din nou
    """
    def fereastra_3_jocul_pornit(self, dificultate_selectata_joc, dificultate_joc):
        self.stergere_fereastra_curenta()
        self.dificultate_selectata_joc = dificultate_selectata_joc
        self.dificultate_joc = dificultate_joc
        self.joc.resetare_joc()

        # creez un frame separat pentru grila si scoreboard
        self.zona_comuna_scor_grila = tk.Frame(self.depozit_ferestre)
        self.zona_comuna_scor_grila.pack(expand=True, fill=tk.BOTH)

        self.grila = tk.Frame(self.zona_comuna_scor_grila)
        self.grila.pack(side="right", anchor="ne", padx=(0,300), pady=(160,10))

        """
        creez butoanele de pe grila
        fiecare buton comanda o mutare la click
        """
        self.butoane_grila = [[None for coloana in range(3)] for rand in range(3)]
        for rand in range(3):
            for coloana in range(3):
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

        self.tabla_scor = tk.Frame(self.zona_comuna_scor_grila)
        tk.Label(
            self.tabla_scor,
            text="SCOR JUCĂTORI",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=(10, 10))
        self.tabla_scor.pack(side="left", anchor="nw", padx=(300, 0), pady=(70, 10))

        """
        creez butoanele din frame ul pentru scor
        butoanele nu pot fi apasate, doar afiseaza scorul updatat
        """
        self.buton_scor_jucator_X = tk.Button(
            self.tabla_scor,
            textvariable=self.eticheta_scor_jucator_X,
            state=tk.DISABLED,
            font=("Arial", 14, "bold"),
            width=17,
            height=5,
            disabledforeground="black"
        )
        self.buton_scor_jucator_X.pack(anchor="w", pady=6)
        self.eticheta_scor_jucator_X.set(f"Jucător X\n{self.scor_castigator_X}")

        self.buton_scor_jucator_O = tk.Button(
            self.tabla_scor,
            textvariable=self.eticheta_scor_jucator_O,
            state=tk.DISABLED,
            font=("Arial", 14, "bold"),
            width=17,
            height=5,
            disabledforeground="black"
        )
        self.buton_scor_jucator_O.pack(anchor="w", pady=6)
        self.eticheta_scor_jucator_O.set(f"Jucător O\n{self.scor_castigator_O}")

        self.buton_scor_remiza = tk.Button(
            self.tabla_scor,
            textvariable=self.eticheta_scor_remiza,
            state=tk.DISABLED,
            font=("Arial", 14, "bold"),
            width=17,
            height=5,
            disabledforeground="black"
        )
        self.buton_scor_remiza.pack(anchor="w", pady=6)
        self.eticheta_scor_remiza.set(f"Remiză\n{self.scor_remiza}")

        # frame separat pentru butoanele care apar in partea de jos a ferestrei
        self.partea_de_jos_tabla = tk.Frame(self.depozit_ferestre)
        self.partea_de_jos_tabla.pack(side="bottom", fill="x", padx=10, pady=(10, 15))

        self.buton_resetare = tk.Button(
            self.partea_de_jos_tabla,
            text="PLAY AGAIN",
            command=self.resetare,
            font=("Arial", 15, "bold"),
            width=20,
            height=2
        )
        self.buton_resetare.pack(side="right")

        self.buton_meniu = tk.Button(
            self.partea_de_jos_tabla,
            text="MENIU",
            command=lambda: (self.resetare_scor(), self.fereastra_1_meniu_principal()),
            font=("Arial", 15, "bold"),
            width=20,
            height=2
        )
        self.buton_meniu.pack(side="left")

        self.actualizare_ui()

    """
    verifica cazurile in care butoanele nu pot fi apsate
    face mutarea user ului (X)
    face mutarea ai ului (O) la distanta de 700 ms dupa ce a mutat user ul
    """
    def apasa_celula(self, rand: int, coloana: int) -> None:
        # ignora apasarea butonului daca jocul e terminat
        if self.joc.joc_terminat:
            return

        # cand ai ul face o mutare, user ul nu poate muta, deci ignora apasarea butonului
        if self.dificultate_selectata_joc == "om_vs_ai" and self.joc.jucator_curent != self.jucator_OM:
            return

        # ignora apasarea pe o celula care nu e goala
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

    """
    verific daca ai ul are voie sa mute acum si e tura lui
    calculeaza mutarea pe care o face in functie de dificultate folosind strategie_AI
    actualizeaza tabla din fereastra cu mutarea aleasa
    """
    def mutare_ai(self):
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

    # sincronizarea butoanelor de pe grila live in functie de schimbarile interne care au loc
    def actualizare_ui(self) -> None:
        for rand in range(3):
            for coloana in range(3):
                valoare_de_pus_in_celula = self.joc.tabla_de_joc[rand][coloana]
                self.butoane_grila[rand][coloana].config(text="" if valoare_de_pus_in_celula == " " else valoare_de_pus_in_celula)

                # highlight colorat pentru piesele jucatorilor in functie de mutare/victorie/remiza
                if valoare_de_pus_in_celula in ("X", "O"):
                    # in caz de remiza highlight ul ramane vizibil pentru ambii jucatori
                    if self.joc.joc_terminat and self.joc.castigator is None:
                        culoare = "#9527F5" if valoare_de_pus_in_celula == "X" else "green"
                    else:
                        # se coloreaza doar piesele jucatorului curent, iar piesele celuilalt raman negre si invers
                        if valoare_de_pus_in_celula == self.joc.jucator_curent:
                            culoare = "#9527F5" if valoare_de_pus_in_celula == "X" else "green"
                        else:
                            culoare = "black"

                    self.butoane_grila[rand][coloana].config(fg=culoare, disabledforeground=culoare)
                else:
                    self.butoane_grila[rand][coloana].config(fg="black", disabledforeground="black")

                # daca jocul s a terminat butoanele nu mai pot fi apasate
                if self.joc.joc_terminat:
                    self.butoane_grila[rand][coloana].config(state=tk.DISABLED)
                else:
                    # pot fi apasate doar butoanele care nu au un simbol pus pe ele deja
                    self.butoane_grila[rand][coloana].config(state=tk.DISABLED if valoare_de_pus_in_celula != " " else tk.NORMAL)

        # actualizeaza status bar: jucator curent sau mesaj final (castigator/remiza)
        if not self.joc.joc_terminat:
            self.mesaj_status_bar.set(f"MUTARE PENTRU JUCĂTORUL {self.joc.jucator_curent}")
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

        self.actualizare_scor()

        # dupa ce s a terminat jocul, deschide fereastra pop up dupa 150 ms
        if self.joc.joc_terminat:
            self.fereastra_principala.after(150, self.pop_up_joaca_din_nou)

    # cand se apasa butonul "play again" se apeleaza resetare
    def resetare(self) -> None:
        self.am_numarat_runda_curenta = False
        self.joc.resetare_joc()
        self.actualizare_ui()
        self.pop_up_joaca_din_nou_deschis = False

# functii de pornire pentru consola/gui
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

if __name__ == "__main__":
    while(True):
        print("Alege modul de joc pentru X și 0:")
        print("1 - Interfață grafică")
        print("2 - Consolă")

        alegere_joc = input("Introdu 1 sau 2 pentru alegerea pe care o vrei: ").strip()

        if alegere_joc == "1":
            run_gui()
        else:
            if alegere_joc == "2":
                run_consola()
            else:
                print("Input invalid. Încearcă să scrii alegerea din nou cu mai multă atenție.\n")