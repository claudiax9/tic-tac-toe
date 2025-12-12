# PHASE 1 - LOGICA JOC + AFISARE CONSOLA

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
            return f"Castigatorul este jucatorul {self.castigator}"
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
        return all(self.tabla_de_joc[rand][coloana] != " " for rand in range(3) for coloana in range(3)) and self.verificare_castigator() is None


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


if __name__ == "__main__":
    run_console()