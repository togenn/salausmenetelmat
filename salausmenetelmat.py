import json

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


def muuta_numerot_kirjaimeksi(numerot, kieli):
    if kieli == "EN":
        salaus = SALAUS_EN
    elif kieli == "FI":
        salaus = SALAUS_FI

    palautus = ""
    for nro in numerot:
        numero = nro % (len(salaus) // 2)
        palautus += salaus[numero]

    return palautus


def muuta_viesti_numeroiksi(viesti, kieli):
    if kieli == "EN":
        salaus = SALAUS_EN
    elif kieli == "FI":
        salaus = SALAUS_FI

    palautus = []
    for kirjain in viesti:
        palautus.append(salaus[kirjain])

    return palautus


def valitse_kieli(kieli):
    if kieli == "FI":
        return SALAUS_FI
    elif kieli == "EN":
        return SALAUS_EN


def caesarin_yhteenlaskumenetelma(viesti, kieli, avain=1, decrypt=False):
    """
    Salaaa tai purkaa viestin caesarin yhteenlaskumenetelmällä.
    Salausfunkktio f(x) = x + avain
    """
    salaus = valitse_kieli(kieli)
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


def caesarin_yhteenlaskumenetelma_brute_force(viesti, kieli):
    salaus = valitse_kieli(kieli)
    viesti = viesti.lower()

    yritykset = []
    for i in range(len(salaus) // 2):
        yritykset.append([caesarin_yhteenlaskumenetelma(viesti, kieli, i, True), i])

    taulukko = ""
    for i in yritykset:
        taulukko += "{} avain={}\n".format(i[0], i[1])

    return taulukko


def caesarin_kertolaskumenetelma(viesti, kieli, avain=1, decrypt=False):
    """
    Salaa tai purkaa viestin caesarin kertolaskumenetelmällä. Viestiä avatessa avain ei saa olla jaollinen aakkosten määrällä.
    Salausfunktio f(x) = x * avain
    """
    salaus = valitse_kieli(kieli)
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


def caesarin_kertolaskumenetelma_brute_force(viesti, kieli):
    salaus = valitse_kieli(kieli)
    viesti = viesti.lower()

    yritykset = []
    for i in range(1, len(salaus) // 2):
        if syt(i, len(salaus) // 2) != 1:
            continue

        yritykset.append([caesarin_kertolaskumenetelma(viesti, kieli, i, True), i])

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


def affini_salaus(viesti, kieli, avain_a=1, avain_b=1, decrypt=False):
    """
    Salaa tai purkaa funktion affinilla järjestelmällä.
    Salausfunktio f(x) = x * avain_a + avain_b
    """
    if not decrypt:
        viesti = caesarin_kertolaskumenetelma(viesti, kieli, avain_a)
        viesti = caesarin_yhteenlaskumenetelma(viesti, kieli, avain_b)

        return viesti

    viesti = caesarin_yhteenlaskumenetelma(viesti, kieli, avain_b, True)
    viesti = caesarin_kertolaskumenetelma(viesti, kieli, avain_a, True)

    return viesti


def affini_salaus_brute_force(viesti, kieli):
    """
    Brute force purkamisen tulos tallentuu brute_force_tulos.txt tiedostoon.
    """
    viesti = viesti.replace(" ", "")

    taulukko = caesarin_yhteenlaskumenetelma_brute_force(viesti, kieli).split("\n")
    taulukko.pop()

    with open("brute_force_tulos.txt", "w") as tiedosto:

        for rivi in taulukko:

            yritys, yritys_avain_b = rivi.split()
            kaannetty_taulukko = caesarin_kertolaskumenetelma_brute_force(
                yritys, kieli
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


def etsi_sanoja_tuloksesta(kieli):
    if kieli == "EN":
        tiedosto = "sanalista_EN.json"
    elif kieli == "FI":
        tiedosto = "sanalista_FI.json"

    with open(tiedosto) as sanat_tiedosto:
        sanat = json.load(sanat_tiedosto)
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
                        print(sana)
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


if __name__ == "__main__":
    # print(SALAUS_EN)
    # print(muuta_numero_kirjaimeksi(447, "FI"))

    # print(muuta_viesti_numeroiksi("aerodynamics", "EN"))
    # print(muuta_numerot_kirjaimeksi([0, 23, 13, 14, 24], "EN"))

    # rint(diofantoksen_yhtalo_ratkaisu(217, 20, 1))
    # print(syt(213, 89))

    print(etsi_sanoja_tuloksesta("FI"))
