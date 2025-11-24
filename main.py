from quest1_AFD import *
from interface import *


def main():
    """Função principal que inicia a aplicação"""
    root = tk.Tk()
    app = SimuladorAFD(root)
    root.mainloop()


if __name__ == "__main__":
    main()
