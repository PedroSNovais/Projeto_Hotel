import os
import pickle


def carregar_reservas():
    caminho= os.path.join("data","reservas.pkl")
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return pickle.load(f)
    else:
        os.mkdir("data")
        with open(caminho, "x") as f:
            pass

        with open(caminho, "wb") as f:
            pickle.dump([], f)
            return []
        
def salvar_reservas(reservas):
    caminho= os.path.join("data","reservas.pkl")
    if not os.path.exists(caminho):
        os.mkdir("data")
        with open(caminho, "x") as f:
            pass
    
    with open(caminho, "wb") as f:
        return pickle.dump(reservas, f)