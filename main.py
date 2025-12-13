import tkinter as tk

# PHASE 1 - GAME LOGIC

class TicTacToe:
    def __init__(self):
        # matrice 3x3
        self.tabla_de_joc = [[" " for _ in range(3)] for _ in range(3)]
        self.jucator_curent = "X"
        self.joc_terminat = False
        self.castigator = None

    def resetare_joc(self):
        self.tabla_de_joc = [[" " for _ in range(3)] for _ in range(3)]
        self.jucator_curent = "X"
        self.joc_terminat = False
        self.castigator = None

    def mutari_disponibile(self):
        mutari = []
        for rand in range(3):
            for coloana in range(3):
                if self.tabla_de_joc[rand][coloana] == " ":
                    mutari.append((rand, coloana))
        return mutari

    def afisare_tabla_joc(self):
        tabla = self.tabla_de_joc
        return "\n".join([
            f" {tabla[0][0]} | {tabla[0][1]} | {tabla[0][2]} ",
            "-----------",
            f" {tabla[1][0]} | {tabla[1][1]} | {tabla[1][2]} ",
            "-----------",
            f" {tabla[2][0]} | {tabla[2][1]} | {tabla[2][2]} ",
        ])

    def mesaj_status_joc(self):
        if self.castigator:
            return f"Castigator: {self.castigator}"
        if self.joc_terminat:
            return "Remiza! Felicitari ambilor jucatori!"
        return f"Mutare pentru jucatorul {self.jucator_curent}"

    def gestionare_mutare(self, rand, coloana):
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
        tabla = self.tabla_de_joc

        # randuri
        # (0 1 2)
        # (3 4 5)
        # (6 7 8)
        for rand in range(3):
            if tabla[rand][0] != " " and tabla[rand][0] == tabla[rand][1] == tabla[rand][2]:
                return tabla[rand][0]

        # coloane
        # (0 3 6)
        # (1 4 7)
        # (2 5 8)
        for coloana in range(3):
            if tabla[0][coloana] != " " and tabla[0][coloana] == tabla[1][coloana] == tabla[2][coloana]:
                return tabla[0][coloana]

        # diagonale
        # (0 4 8)
        # (2 4 6)
        if tabla[0][0] != " " and tabla[0][0] == tabla[1][1] == tabla[2][2]:
            return tabla[0][0]
        if tabla[0][2] != " " and tabla[0][2] == tabla[1][1] == tabla[2][0]:
            return tabla[0][2]

        return None

    def verificare_remiza(self):
        return all(self.tabla_de_joc[r][c] != " " for r in range(3) for c in range(3)) and self.verificare_castigator() is None


def run_console():
    joc = TicTacToe()
    print("Pentru jocul Tic Tac Toe, introdu doua numere pentru rand, respectiv coloana, de la 1 la 3. Exemplu: 2 3\n")
    print(joc.afisare_tabla_joc())

    while not joc.joc_terminat:
        input_utilizator = input(f"\n{joc.mesaj_status_joc()} | Introdu indicii pentru mutarea ta: ").strip()
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


# PHASE 2 - GUI

class TicTacToeGUI:
    def __init__(self, fereastra_principala: tk.Tk):
        self.fereastra_principala = fereastra_principala
        self.joc = TicTacToe()

        # fereastra principala (Tkinter window) / titlu + dimensiune
        self.fereastra_principala.title("TIC TAC TOE")
        self.fereastra_principala.geometry("500x500")  # latime x inaltime
        self.fereastra_principala.resizable(False, False)

        # creare status bar cu jucator curent + mesaj final castigator/remiza
        self.mesaj_status_bar = tk.StringVar() # randul playerilor, status final joc
        self.eticheta_status_bar = tk.Label(
            fereastra_principala,
            textvariable=self.mesaj_status_bar,
            font=("Arial", 14, "bold")
        )
        self.eticheta_status_bar.pack(padx=10, pady=(10, 5))

        # tabla de joc cu grila 3×3 cu 9 butoane care pot fi apasate
        grila = tk.Frame(fereastra_principala)
        grila.pack(padx=10, pady=30)

        # butoanele de pe grila
        self.butoane = [[None for _ in range(3)] for _ in range(3)]
        for rand in range(3):
            for coloana in range(3):
                # cand se da click pe celula se apeleaza apasa_celula(r, c)
                buton = tk.Button(
                    grila,
                    text="",
                    width=6,
                    height=3,
                    font=("Arial", 18, "bold"),
                    command=lambda r=rand, c=coloana: self.apasa_celula(r, c)
                )
                buton.grid(row=rand, column=coloana, padx=3, pady=3)
                self.butoane[rand][coloana] = buton

        # buton resetare "joaca din nou"
        bottom = tk.Frame(fereastra_principala)
        bottom.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        # butonul de resetare: reseteaza tabla de joc si porneste jocul de la 0
        self.buton_resetare = tk.Button(
                                bottom,
                                text="Joacă din nou",
                                command=self.resetare,
                                font=("Arial", 15, "bold"),
                                width=20,
                                height=2
                                )
        self.buton_resetare.pack(side="bottom")

        self.actualizare_ui() # initializare ui / afisare mutare curenta si tabla goala

    def apasa_celula(self, rand: int, coloana: int) -> None:
        # ignora click ul daca jocul e terminat
        if self.joc.joc_terminat:
            return

        # ignora click ul pe o celula care nu e goala
        if self.joc.tabla_de_joc[rand][coloana] != " ":
            return

        # aplica mutarea player ului
        try:
            self.joc.gestionare_mutare(rand, coloana)
        except ValueError:
            return

        self.actualizare_ui() # actualizeaza tabla de joc si blocheaza celulele ocupate sau daca jocul e terminat

    def actualizare_ui(self) -> None:
        # update pe tabla de joc live
        for rand in range(3):
            for coloana in range(3):
                valoare_de_pus_in_celula = self.joc.tabla_de_joc[rand][coloana]
                self.butoane[rand][coloana].config(text="" if valoare_de_pus_in_celula == " " else valoare_de_pus_in_celula)

                # culoare simboluri x O
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

                    self.butoane[rand][coloana].config(fg=culoare, disabledforeground=culoare)
                else:
                    self.butoane[rand][coloana].config(fg="black", disabledforeground="black")

                """
                # culoare simboluri X / O
                if valoare_de_pus_in_celula == "X":
                    self.butoane[rand][coloana].config(fg="#9527F5", disabledforeground="#9527F5")
                elif valoare_de_pus_in_celula == "O":
                    self.butoane[rand][coloana].config(fg="green", disabledforeground="green")
                else:
                    self.butoane[rand][coloana].config(fg="black", disabledforeground="black")
                """

                if self.joc.joc_terminat:
                    self.butoane[rand][coloana].config(state=tk.DISABLED)
                else:
                    self.butoane[rand][coloana].config(state=tk.DISABLED if valoare_de_pus_in_celula != " " else tk.NORMAL)


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


def run_gui():
    fereastra_principala = tk.Tk()
    TicTacToeGUI(fereastra_principala)
    fereastra_principala.mainloop()


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
                run_console()
            else:
                print("Input invalid. Incearca din nou.\n")