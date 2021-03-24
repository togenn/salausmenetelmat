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
        for i in range(len(salaus) // 2):
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
    viesti, kieli, avain=1, decrypt=False, brute_force=False
):
    """
    Salaa tai purkaa viestin caesarin kertolaskumenetelmällä.
    Salausfunktio f(x) = x * avain
    """
    if kieli == "FI":
        salaus = SALAUS_FI
    elif kieli == "EN":
        salaus = SALAUS_EN
    viesti = viesti.lower()

    if brute_force:
        yritykset = []
        for i in range(1, len(salaus) // 2):
            yritykset.append([caesarin_kertolaskumenetelma(viesti, kieli, i, True), i])

        taulukko = ""
        for i in yritykset:
            taulukko += "{} avain={}\n".format(i[0], i[1])

        return taulukko

    kaannetty_viesti = ""
    if decrypt:
        kaanteisalkio = diofantoksen_yhtalo_ratkaisu(len(salaus) // 2, avain, 1)
        avain = kaanteisalkio[1]

    for i, kirjain in enumerate(viesti):
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


def affini_salaus(viesti, kieli, avain_a, avain_b, decrypt=False, brute_force=False):
    """
    Salaa tai purkaa funktion affinilla järjestelmällä.
    Salausfunktio f(x) = x * avain_a + avain_b
    """
    if not decrypt:
        viesti = caesarin_yhteenlaskumenetelma(viesti, kieli, avain_a)
        viesti = caesarin_kertolaskumenetelma(viesti, kieli, avain_b)

        return viesti

    if brute_force:
        pass


if __name__ == "__main__":
    print(caesarin_kertolaskumenetelma("äieriyoaäa", "FI", 13, brute_force=1))
