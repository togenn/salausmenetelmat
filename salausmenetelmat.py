import numpy as np
from json import load
from textwrap import wrap
from itertools import product

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
    Palauttaa kahden numeron suurimman yhteisen tekijän.
    """
    numero1 = max(a, b)
    numero2 = min(a, b)

    if numero2 == 0:
        return 0

    jakojaannos = numero1 % numero2

    while jakojaannos != 0:
        numero1 = numero2
        numero2 = jakojaannos
        jakojaannos = numero1 % numero2

    return numero2


def diofantoksen_yhtalo_ratkaisu(a, b, c):
    """
    Palauttaa erään ratkaisun yhtälölle ax+by=c , missä a ja b ovat nollasta eroavia kokonaislukuja ja c = syt(a, b):n monikerta.
    Jos yhtälöllä ei ole ratkaisua tai yhtälö ei täytä ehtoja, niin se palauttaa (None, None).
    """
    syt_ab = syt(a, b)
    c = c // syt_ab
    if b > a:
        kaanna = True
    else:
        kaanna = False

    apu = a
    a = max(a, b)
    b = min(apu, b)

    if a % b == 0:
        return None, None

    jakojaannos = a % b
    bkertoimet = [a // b * -1]

    while jakojaannos != syt_ab:
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


def muuta_numerot_kirjaimiksi(numerot, aakkoset):
    salaus = valitse_aakkoset(aakkoset)

    palautus = ""
    for nro in numerot:
        numero = nro % (len(salaus) // 2)
        palautus += salaus[numero]

    return palautus


def muuta_viesti_numeroiksi(viesti, aakkoset):
    salaus = valitse_aakkoset(aakkoset)
    viesti = viesti.lower()

    palautus = []
    for kirjain in viesti:
        palautus.append(salaus[kirjain])

    return palautus


def valitse_aakkoset(aakkoset):
    if aakkoset == "FI":
        return SALAUS_FI
    elif aakkoset == "EN":
        return SALAUS_EN
    else:
        salaus = {}
        for i, kirjain in enumerate(aakkoset):
            salaus[i] = kirjain
            salaus[kirjain] = i

        return salaus


def caesarin_yhteenlaskumenetelma(viesti, avain, aakkoset, decrypt=False):
    """
    Salaaa tai purkaa viestin caesarin yhteenlaskumenetelmällä.
    Salausfunkktio f(x) = x + avain
    """
    salaus = valitse_aakkoset(aakkoset)
    viesti = viesti.lower()

    kaannetty_viesti = ""
    for kirjain in viesti:
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


def caesarin_yhteenlaskumenetelma_brute_force(viesti, aakkoset):
    salaus = valitse_aakkoset(aakkoset)
    viesti = viesti.lower()

    yritykset = []
    for i in range(len(salaus) // 2):
        yritykset.append([caesarin_yhteenlaskumenetelma(viesti, aakkoset, i, True), i])

    taulukko = ""
    for i in yritykset:
        taulukko += "{} avain={}\n".format(i[0], i[1])

    return taulukko


def caesarin_kertolaskumenetelma(viesti, avain, aakkoset, decrypt=False):
    """
    Salaa tai purkaa viestin caesarin kertolaskumenetelmällä. Viestiä avatessa avain ei saa olla jaollinen aakkosten määrällä.
    Salausfunktio f(x) = x * avain
    """
    salaus = valitse_aakkoset(aakkoset)
    viesti = viesti.lower()

    kaannetty_viesti = ""
    if decrypt:

        if syt(avain, len(salaus) // 2) != 1:
            return None

        if avain > 1:
            kaanteisalkio = diofantoksen_yhtalo_ratkaisu(len(salaus) // 2, avain, 1)
            avain = kaanteisalkio[1]

    for kirjain in viesti:
        if kirjain == " ":
            kaannetty_viesti += " "
            continue

        numero = salaus[kirjain] * avain
        numero = numero % (len(salaus) // 2)
        kaannetty_viesti += salaus[numero]

    return kaannetty_viesti


def caesarin_kertolaskumenetelma_brute_force(viesti, aakkoset):
    salaus = valitse_aakkoset("")
    viesti = viesti.lower()

    yritykset = []
    for i in range(1, len(salaus) // 2):
        if syt(i, len(salaus) // 2) != 1:
            continue

        yritykset.append([caesarin_kertolaskumenetelma(viesti, aakkoset, i, True), i])

    taulukko = ""
    for i in yritykset:
        taulukko += "{} avain={}\n".format(i[0], i[1])

    return taulukko


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


def affini_salaus(viesti, aakkoset, avain_a=1, avain_b=1, decrypt=False):
    """
    Salaa tai purkaa funktion affinilla järjestelmällä.
    Salausfunktio f(x) = x * avain_a + avain_b
    """
    if not decrypt:
        viesti = caesarin_kertolaskumenetelma(viesti, avain_a, aakkoset)
        viesti = caesarin_yhteenlaskumenetelma(viesti, avain_b, aakkoset)

        return viesti

    viesti = caesarin_yhteenlaskumenetelma(viesti, avain_b, aakkoset, True)
    viesti = caesarin_kertolaskumenetelma(viesti, avain_a, aakkoset, True)

    return viesti


def affini_salaus_brute_force(viesti, aakkoset):
    """
    Brute force purkamisen tulos tallentuu brute_force_tulos.txt tiedostoon.
    """
    viesti = viesti.replace(" ", "")

    taulukko = caesarin_yhteenlaskumenetelma_brute_force(viesti, aakkoset).split("\n")
    taulukko.pop()

    with open("brute_force_tulos.txt", "w") as tiedosto:

        for rivi in taulukko:

            yritys, yritys_avain_b = rivi.split()
            kaannetty_taulukko = caesarin_kertolaskumenetelma_brute_force(
                yritys, aakkoset
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


def onko_sana(sana, kieli):
    pass


def etsi_sanoja_tuloksesta(kieli):
    if kieli == "EN":
        tiedosto = "sanalista_EN.json"
    elif kieli == "FI":
        tiedosto = "sanalista_FI.json"

    with open(tiedosto) as sanat_tiedosto:
        sanat = load(sanat_tiedosto)
        with open("brute_force_tulos.txt", "r") as brute_force_tulos:
            taulukko = ""

            while True:
                try:
                    viesti, avain_a, avain_b = brute_force_tulos.readline().split()
                except ValueError:
                    if not taulukko:
                        taulukko += "Ei tuloksia"

                    return taulukko

                pituus = len(viesti)

                if pituus > 21:
                    pituus = 21

                for i in range(1, pituus + 1):
                    sana = viesti[0:i]
                    if sana in sanat:
                        break
                else:
                    continue

                for j in range(1, pituus + 1):
                    sana2 = viesti[len(viesti) - j : len(viesti)]

                    if sana2 in sanat:
                        break
                else:
                    continue

                taulukko += "{}, löytyi {}, {}\n".format(viesti, avain_a, avain_b)


def maaraa_aakkoset(avainsana, siirto, kieli):
    if kieli == "EN":
        aakkoset = AAKKOSET_EN
    elif kieli == "FI":
        aakkoset = AAKKOSET_FI

    avainsana = avainsana.lower().replace(" ", "")
    kirjaimien_maara = len(aakkoset)
    poistettavat = []
    for kirjain in avainsana:
        if kirjain not in poistettavat:
            poistettavat.append(kirjain)
            aakkoset = aakkoset.replace(kirjain, "")

    poistettavat.extend(aakkoset)
    uusi_salaus = [None] * kirjaimien_maara
    for i, kirjain in enumerate(poistettavat, siirto):
        uusi_salaus[i % kirjaimien_maara] = kirjain

    return uusi_salaus


def caesar_avainsanalla(viesti, avainsana, siirto, kieli, decrypt=False):
    """
    Avainsanasta poistetaan toistuvat kirjaimet. Avainsana sijoitetaan aakkosiin siten, että se alkaa indeksistä siirto.
    Tämän jälkeen sijoitetaan jäljellä olevat aakkoset järjestyksessä eteenpäin. Viesti salataan vertaamalla aakkosen indeksiä vastaavaan kirjaimeen uusissa aakkosissa.
    Esim avainsana=aasi, kieli=FI, ja siirto=4:
    zåäöasibcdefghjklmnopqrtuvwxy

    """
    aakkoset = valitse_aakkoset(kieli)
    salaus = maaraa_aakkoset(avainsana, siirto, kieli)
    viesti = viesti.lower().replace(" ", "")
    muunnettu_viesti = ""

    if not decrypt:
        for kirjain in viesti:
            kirjaimen_indeksi = aakkoset[kirjain]
            muunnettu_viesti += salaus[kirjaimen_indeksi]
    else:
        for kirjain in viesti:
            kirjaimen_indeksi = salaus.index(kirjain)
            muunnettu_viesti += aakkoset[kirjaimen_indeksi]

    return muunnettu_viesti


def vigeneren_salaus(viesti, salasana, aakkoset, decrypt=False):
    """
    Jakaa viestin len(salasana):n pituisiin osiin ja salaa jokaisen osan kirjaimen sitä vastaavan salasanan kirjaimen vastaavalla numerolla.
    Esim.
    salasana=orsi viesti=iltapimenee aakkoset = FI
    ilta|pime|nee
     08 11 19 00|15 08 12 04|13 04 04
    +14 17 18 08|14 17 18 08|14 17 18
    = 22 28 8 8 0 25 01 12 27 21 22
    W Ö I I A Z B M Ä V W
    """
    salaus = valitse_aakkoset(aakkoset)
    viesti = viesti.lower().replace(" ", "")
    avaimet = []
    for kirjain in salasana:
        avaimet.append(salaus[kirjain])

    pilkottu_viesti = wrap(viesti, len(salasana))

    muunnettu_viesti = ""
    for osa in pilkottu_viesti:
        for i, kirjain in enumerate(osa):
            muunnettu_viesti += caesarin_yhteenlaskumenetelma(
                kirjain, avaimet[i], aakkoset, decrypt
            )

    return muunnettu_viesti


def vigeneren_salaus_brute_force(viesti, kieli):
    """
    Yrittää löytää kokeilemalla salasanan, jolla viestin alusta ja lopusta löytyisi sana.
    Tallentaa tulokset vigenere_brute_force.txt tiedostoon.
    """
    if kieli == "FI":
        aakkoset = AAKKOSET_FI
        tiedosto = "sanalista_FI.json"
    elif kieli == "EN":
        aakkoset = AAKKOSET_EN
        tiedosto = "sanalista_EN.json"
    else:
        raise ValueError("virheellinen kieli")

    viesti = viesti.lower().replace(" ", "")
    with open("vigenere_brute_force.txt", "w") as tulos:
        with open(tiedosto) as sanat_tiedosto:
            sanat = load(sanat_tiedosto)

            for pituus in range(1, len(viesti) + 1):
                for yhdistelma in product(aakkoset, repeat=pituus):
                    salasana = "".join(yhdistelma)
                    yritys = vigeneren_salaus(viesti, salasana, kieli, True)
                    pituus = len(yritys)

                    if pituus > 21:
                        pituus = 21

                    for i in range(1, pituus + 1):
                        sana = yritys[0:i]
                        if sana in sanat:
                            break
                    else:
                        continue

                    for j in range(1, pituus + 1):
                        sana2 = yritys[len(viesti) - j : len(viesti)]

                        if sana2 in sanat:
                            break
                    else:
                        continue

                    tulos.write(
                        "{} {}\n".format(
                            vigeneren_salaus(viesti, salasana, kieli, True), salasana
                        )
                    )


def matriisisalaus(viesti, avain_a, avain_b, aakkoset, decrypt=False):
    """
    Viesti muunnetaan 2 x n matriisiksi ja kerrotaan 2 x 2 matriisilla avain_a, ja siihen 2 x 1 lisätään matriisi avain_b, joka "venytetään" n pituiseksi.
    """

    if not decrypt:
        viesti_palat = wrap(viesti, 2)
        viesti_matriisi = []
        for pala in viesti_palat:
            pala_numeroina = muuta_viesti_numeroiksi(pala, aakkoset)
            if len(pala_numeroina) == 1:
                pala_numeroina.append(0)

            viesti_matriisi.append(pala_numeroina)

        viesti_matriisi = np.transpose(viesti_matriisi)
        print(viesti_matriisi)


# Viestin muuntaminen toimii TODO salaaminen
if __name__ == "__main__":

    matriisisalaus("kissa", 1, 1, "FI")
