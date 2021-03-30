import json
import timeit

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
    Palauttaa kahden erisuure numeron yhteisen tekijän.
    """
    numero1 = max(a, b)
    numero2 = min(a, b)

    jakojaannos = numero1 % numero2

    while jakojaannos != 0:
        numero1 = numero2
        numero2 = jakojaannos
        jakojaannos = numero1 % numero2

    return numero2


def diofantoksen_yhtalo_ratkaisu(a, b, c):
    """
    Palauttaa erään ratkaisun yhtälölle ax+by=c, missä a, b ja c ovat nollasta eroavia kokonaislukuja ja  a ja b eivä ole keskenään jaollisia.
    Jos yhtälöllä ei ole ratkaisua tai yhtälö ei täytä ehtoja, niin se palauttaa False, False.
    """
    syt_ab = syt(a, b)
    if c / syt_ab != c // syt_ab:
        return False, False

    if b > a:
        kaanna = True
    else:
        kaanna = False

    apu = a
    a = max(a, b)
    b = min(apu, b)

    if a % b == 0:
        return False, False

    jakojaannos = a % b
    bkertoimet = [a // b * -1]

    while jakojaannos != 1:
        a = b
        b = jakojaannos
        jakojaannos = a % b
        bkertoimet.append(a // b * -1)

    bkertoimet.reverse()
    i = 1
    x = 1
    y = bkertoimet[0]

    while len(bkertoimet) > i:
        kerroin_a = x
        kerroin_b = y
        x = kerroin_b
        y = kerroin_b * bkertoimet[i] + kerroin_a
        i += 1

    if kaanna:
        apu = x
        x = y
        y = apu

    return c * x, c * y


def caesarin_yhteenlaskumenetelma(
    viesti, kieli, avain=1, decrypt=False, brute_force=False
):
    """
    Salaaa tai purkaa viestin caesarin yhteenlaskumenetelmällä.
    Salausfunkktio f(x) = x + avain
    """
    if kieli == "FI":
        salaus = SALAUS_FI
    elif kieli == "EN":
        salaus = SALAUS_EN
    viesti = viesti.lower()

    if brute_force:
        yritykset = []
        for i in range(1, len(salaus) // 2):
            yritykset.append([caesarin_yhteenlaskumenetelma(viesti, kieli, i, True), i])

        taulukko = ""
        for i in yritykset:
            taulukko += "{} avain={}\n".format(i[0], i[1])

        return taulukko

    kaannetty_viesti = ""
    for i, kirjain in enumerate(viesti):
        if kirjain == " ":
            kaannetty_viesti += " "
            continue

        if not decrypt:
            numero = salaus[kirjain] + avain
        elif not brute_force:
            numero = salaus[kirjain] - avain

        numero = numero % (len(salaus) // 2)
        kaannetty_viesti += salaus[numero]

    return kaannetty_viesti


def caesarin_kertolaskumenetelma(
    viesti, kieli, avain=2, decrypt=False, brute_force=False
):
    """
    Salaa tai purkaa viestin caesarin kertolaskumenetelmällä. Viestiä avatessa avain ei saa olla jaollinen aakkosten määrällä.
    Salausfunktio f(x) = x * avain
    """
    if kieli == "FI":
        salaus = SALAUS_FI
    elif kieli == "EN":
        salaus = SALAUS_EN
    viesti = viesti.lower()

    if brute_force:
        yritykset = []
        for i in range(2, len(salaus) // 2):
            if syt(len(salaus) // 2, i) != 1:
                continue
            
            yritykset.append([caesarin_kertolaskumenetelma(viesti, kieli, i, True), i])

        taulukko = ""
        for i in yritykset:
            taulukko += "{} avain={}\n".format(i[0], i[1])

        return taulukko

    kaannetty_viesti = ""
    if decrypt:
        if syt(len(salaus) // 2, avain) != 1:
            return "Viestiä avatessa avain ei saa olla jaollinen aakkosten määrällä"

        avain = diofantoksen_yhtalo_ratkaisu(len(salaus) // 2, avain, 1)[1]

    for kirjain in viesti:
        if kirjain == " ":
            kaannetty_viesti += " "
            continue

        numero = salaus[kirjain] * avain
        numero = numero % (len(salaus) // 2)
        kaannetty_viesti += salaus[numero]

    return kaannetty_viesti


def kirjaimien_frekvenssi(viesti):
    """
    Palauttaa merkkijonona viestissä esiintyvien kirjaimien frekvenssin.
    """
    kirjaimet = {}
    viesti = viesti.lower()
    viesti = viesti.replace(" ", "")
    for kirjain in viesti:
        if not kirjain in kirjaimet.keys():
            kirjaimet[kirjain] = 1
        else:
            kirjaimet[kirjain] += 1

    kirjaimet_jarjestetty = dict(
        sorted(kirjaimet.items(), reverse=True, key=lambda arvo: arvo[1])
    )
    taulukko = ""
    for kirjain in kirjaimet_jarjestetty:
        taulukko += "{}: {}\n".format(kirjain, kirjaimet_jarjestetty[kirjain])

    return taulukko


def affini_salaus(
    viesti, kieli, avain_a=1, avain_b=1, decrypt=False, brute_force=False
):
    """
    Salaa tai purkaa funktion affinilla järjestelmällä.
    Salausfunktio f(x) = x * avain_a + avain_b
    Brute force purkamisen tulos tallentuu brute_force_tulos.txt tiedostoon.
    """
    if not decrypt and not brute_force:
        viesti = caesarin_kertolaskumenetelma(viesti, kieli, avain_a)
        viesti = caesarin_yhteenlaskumenetelma(viesti, kieli, avain_b)

        return viesti

    if not brute_force:
        viesti = caesarin_yhteenlaskumenetelma(viesti, kieli, avain_b, True)
        viesti = caesarin_kertolaskumenetelma(viesti, kieli, avain_a, True)

        return viesti

    taulukko = caesarin_yhteenlaskumenetelma(viesti, kieli, brute_force=True).split(
        "\n"
    )
    taulukko.pop()

    with open("brute_force_tulos.txt", "w") as tiedosto:

        for rivi in taulukko:

            yritys, yritys_avain_b = rivi.split()
            kaannetty_taulukko = caesarin_kertolaskumenetelma(
                yritys, kieli, brute_force=True
            ).split("\n")
            yritys_avain_b = yritys_avain_b.replace("avain=", "")
            kaannetty_taulukko.pop()

            for rivi2 in kaannetty_taulukko:
                kaannetty_viesti, yritys_avain_a = rivi2.split()
                yritys_avain_a = yritys_avain_a.replace("avain=", "")
                tiedosto.write(
                    "{} avain_a={} avain_b={}\n".format(
                        kaannetty_viesti, yritys_avain_a, yritys_avain_b
                    )
                )


def etsi_sanoja_tuloksesta():
    # if kieli == "EN":
    with open("words_dictionary.json") as sanat_tiedosto:
        sanat = json.load(sanat_tiedosto)
        with open("brute_force_tulos.txt", "r") as brute_force_tulos:

            viesti, avain_a, avain_b = brute_force_tulos.readline().split()
            while True:
                loytyiko = False
                pituus = len(viesti)
                if pituus > 21:
                    pituus = 21
                for i in range(1, pituus):
                    sana = viesti[0 : i + 1]
                    if sana in sanat:
                        loytyiko = True
                        break
                if loytyiko:
                    print(viesti, "löytyi {}, {}".format(avain_a, avain_b), sana)

                try:
                    viesti, avain_a, avain_b = brute_force_tulos.readline().split()
                except ValueError:
                    return


if __name__ == "__main__":
    
    print(caesarin_kertolaskumenetelma("bqjuzbzqnz", "EN", brute_force=True))
