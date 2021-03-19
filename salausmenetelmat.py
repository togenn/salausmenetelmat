import math

AAKKOSET_FI = "abcdefghijklmnopqrstuvwxyzåäö"
AAKKOSET_EN = "abcdefghijklmnopqrstuvwxyz"
SALAUS_FI = {}
SALAUS_EN = {}

for i, kirjain in enumerate(AAKKOSET_FI):
    SALAUS_FI[kirjain] = i
    SALAUS_FI[i] = kirjain

for i, kirjain in enumerate(AAKKOSET_EN):
    SALAUS_EN[kirjain] = i
    SALAUS_EN[i] = kirjain

def syt(a, b):
    """
    Palauttaa lukujen suurimman yhteisen tekijän.
    """ 
    numero1 = max(a, b)
    numero2 = min(a,b)

    jakojaannos = numero1 % numero2

    while jakojaannos != 0:
        numero1 = numero2
        numero2 = jakojaannos
        jakojaannos = numero1 % numero2
    
    return numero2

def diofantoksen_yhtalo_ratkaisu(a, b, c):
    if isinstance(c / syt(a, b), float):
        return False, False

    syt
    while syt 
    

def alkulukuhajotelma():
    pass

def caesarin_yhteenlaskumenetelma(viesti, kieli, avain, decrypt=True):
    """
    Salaaa tai purkaa viestin caesarin yhteenlaskumenetelmällä.
    """
    if kieli == "FI":
        salaus = SALAUS_FI
    elif kieli == "EN":
        salaus = SALAUS_EN
    viesti = viesti.lower()

    kaannetty_viesti = ""
    for i, kirjain in enumerate(viesti):
        if kirjain == " ":
            kaannetty_viesti += " "
            continue

        if not decrypt:
            numero = salaus[kirjain] + avain
        else:
            numero = salaus[kirjain] - avain

        numero = numero % (len(salaus) // 2) 
        kaannetty_viesti += salaus[numero]

    return kaannetty_viesti

def caesarin_kertolaskumenetelma(viesti, kieli, avain, decrypt=True) {
    if kieli == "FI":
        salaus = SALAUS_FI
    elif kieli == "EN":
        salaus = SALAUS_EN
    viesti = viesti.lower()

    kaannetty_viesti = ""
    for i, kirjain in enumerate(viesti):
        if kirjain == " ":
            kaannetty_viesti += " "
            continue

        if not decrypt:
            numero = salaus[kirjain] * avain
        else:
            numero = salaus[kirjain] * avain

        numero = numero % (len(salaus) // 2) 
        kaannetty_viesti += salaus[numero]


}




if __name__ == "__main__":
    print(caesarin_yhteenlaskumenetelma("TÄLTDEÄAXÄD", "FI", 19))
    
 
