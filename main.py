import random
from test_Rabin_miller import rabin_miller

def charger_cle_publique():
    """Charge la clé publique à partir du fichier."""
    try:
        with open("cle_publique.key", "r") as f:
            n, e = map(int, f.read().strip().split(","))  # Lire n et e comme des entiers
        return (n, e)
    except FileNotFoundError:
        print("Erreur : Le fichier de la clé publique est introuvable.")
        return None
    except ValueError:
        print("Erreur : Format de la clé publique invalide.")
        return None

def charger_cle_privee():
    """Charge la clé privée à partir du fichier."""
    try:
        with open("cle_privee_chiffree.key", "r") as f:
            n, d = map(int, f.read().strip().split(","))  # Lire n et d comme des entiers
        return (n, d)
    except FileNotFoundError:
        print("Erreur : Le fichier de la clé privée est introuvable.")
        return None
    except ValueError:
        print("Erreur : Format de la clé privée invalide.")
        return None
    
def preuve_divulgation_nuller():
    """
    Preuve à divulgation nulle basée sur le protocole de Guillou-Quisquater (RSA).
    Les clés sont chargées depuis les fichiers 'cle_publique.txt' et 'cle_privee_chiffree.txt'.
    """
    # Charger les clés
    public_key = charger_cle_publique()
    private_key = charger_cle_privee()

    if public_key is None or private_key is None:
        print("Erreur : Impossible de charger les clés.")
        return

    n, e = public_key
    _, d = private_key

    # Paramètres fixes
    H = random.randint(2, n - 2)  # Choisir H dans [2, n-2]
    print(f"Message H choisi : {H}")
    S = pow(H, e, n)  # Signature RSA : S = H^e mod n
    print(f"Signature calculée S : {S}")

    # Étape 1 : Nicolas choisit m aléatoire et calcule M
    m = random.randint(2, n - 2)  # m dans [2, n-2]
    alpha = random.randint(2, n - 2)  # Générateur aléatoire
    M = pow(alpha, m, n)  # M = alpha^m mod n
    print(f"Valeur calculée M : {M}")

    # Étape 2 : Rémi génère un challenge r
    r = random.randint(1, e - 1)  # r < e
    print(f"Challenge r choisi par Rémi : {r}")

    # Étape 3 : Nicolas calcule la preuve
    try:
        H_r_inverse = pow(pow(H, r, n), -1, n)  # Calcul de H^-r mod n
    except ValueError:
        print("Erreur : Impossible de calculer l'inverse modulaire.")
        return

    preuve = (m * H_r_inverse) % n  # Preuve = m * H^-r mod n
    print(f"Preuve calculée : {preuve}")

    # Étape 4 : Rémi vérifie la preuve
    Sr = pow(S, r, n)  # S^r mod n
    Preuve_e = pow(preuve, e, n)  # Preuve^e mod n
    M_verifie = (Sr * Preuve_e) % n  # Vérification finale
    print(f"Valeur vérifiée M : {M_verifie}")

    is_valid = (M_verifie == M)
    print(f"Résultat de la vérification : {'Succès' if is_valid else 'Échec'}")
    return is_valid


    
def verifier_correspondance():
    print("Vérification de la correspondance des clés publique et privée...")
    
    # Appel de la preuve à divulgation nulle
    resultat = preuve_divulgation_nulle()
    if resultat:
        print("Succès : La clé publique correspond bien à la clé privée.")
    else:
        print("Échec : La clé publique ne correspond pas à la clé privée.")

def Euclide_etendu(a, b):
        if b == 0:
            return a, 1, 0
        pgcd, x1, y1 = Euclide_etendu(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return pgcd, x, y

# Calcul de l'inverse modulaire (Algorithme d'Euclide étendu)
def mod_inverse(e, phi):
    """Calcule l'inverse modulaire de e modulo phi."""
    pgcd, x, _ = Euclide_etendu(e, phi)
    if pgcd != 1:
        raise ValueError("e et phi ne sont pas premiers entre eux")
    return x % phi

def generer_nombre_premier(bits):
    """Génère un grand nombre premier de 'bits' bits."""
    while True:
        nombre_candidat = random.getrandbits(bits) | (1 << bits - 1) | 1  # Assure que le nombre est impair et de taille correcte
        if rabin_miller(nombre_candidat):
            return nombre_candidat

# Fonction principale pour générer un couple de clés publique/privée
def generer_couple_cles():
    """Génère une paire de clés RSA (publique et privée) d'au moins 1024 bits."""
    # Étape 1 : Générer deux grands nombres premiers p et q
    p = generer_nombre_premier(512)
    q = generer_nombre_premier(512)
    # Étape 2 : Calculer n et phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Étape 3 : Trouver un e valide
    e = 65537  # e standard pour RSA
    if phi % e == 0:  # Assurer que e est premier avec phi
        e = 3
        while True:
            if rabin_miller(e) and phi % e != 0:
                break
            e += 2

    # Étape 4 : Calculer d, l'inverse modulaire de e
    d = mod_inverse(e, phi)

    # Retourner les clés publique (n, e) et privée (n, d)
    return (n, e), (n, d)

def creer_compte():
    """Crée un compte utilisateur en générant un couple de clés RSA."""
    print("Création de compte...")
    public_key, private_key = generer_couple_cles()
    print(f"Clé publique : {public_key}")
    print(f"Clé privée : {private_key}")

    # Stockage des clés dans des fichiers
    with open("cle_publique.key", "w") as f:
        # Sauvegarder la clé publique dans le format : n,e
        f.write(f"{public_key[0]},{public_key[1]}\n")

    with open("cle_privee_chiffree.key", "w") as f:
        # Sauvegarder la clé privée dans le format : n,d
        f.write(f"{private_key[0]},{private_key[1]}\n")

    print("Clés générées et stockées avec succès !")

def menu_principal():
    """Affiche le menu principal du program"""
    while True:
        print("Bienvenue dans le coffre-fort numérique !")
        print("1. Créer un compte")
        print("2. Se connecter")
        print("3. Quitter")
        print("4. Vérifier une clé publique avec une preuve à divulgation nulle")
        choix = input("Choisissez une option : ")

        if choix == "1":
            creer_compte()
        elif choix == "2":
            print("Se connecter ...")
            """Ajout de la fonction de connection"""
        elif choix == "3":
            print("Au revoir !")
            break
        elif choix == "4":
            print("Vous avez selectionne l'option 4 !")
            verifier_correspondance()
        else:
            print("Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    menu_principal()