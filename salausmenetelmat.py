import math
import numpy as np
from json import load
from textwrap import wrap
from itertools import product
from sympy.ntheory import qs


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

    jakojaannos = numero1 % numero2

    while jakojaannos != 0:
        numero1 = numero2
        numero2 = jakojaannos
        jakojaannos = numero1 % numero2

    return numero2


def diofantoksen_yhtalo_ratkaisu(a, b, c):
    """
    Palauttaa erään ratkaisun yhtälölle ax+by=c , missä a ja b ovat nollasta eroavia kokonaislukuja ja c = syt(a, b):n monikerta.
    Jos yhtälö ei täytä ehtoja, niin aiheuttaa ValueErrorin.
    """
    syt_ab = syt(a, b)
    c = math.ceil(c / syt_ab)
    kanna = bool(b > a)

    apu = a
    a = max(a, b)
    b = min(apu, b)

    if a % b == 0:
        raise ValueError("Ei ratkaisua")

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
        x, y = y, x

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
    viesti = viesti.lower().replace(" ", "")

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


def valitse_sanalista(kieli):
    if kieli == "FI":
        return "sanalista_FI.json"
    elif kieli == "EN":
        return "sanalista_EN.json"
    else:
        raise ValueError("Virheellinen kieli")


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
        yritykset.append([caesarin_yhteenlaskumenetelma(viesti, i, aakkoset, True), i])

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
    salaus = valitse_aakkoset(aakkoset)
    viesti = viesti.lower()

    yritykset = []
    taulukko = ""
    for i in range(1, len(salaus) // 2):
        if syt(i, len(salaus) // 2) != 1:
            continue

        yritykset.append([caesarin_kertolaskumenetelma(viesti, i, aakkoset, True), i])
        taulukko += "{} avain={}\n".format(
            caesarin_kertolaskumenetelma(viesti, i, aakkoset, True), i
        )

    return taulukko


def kirjaimien_frekvenssi(viesti):
    """
    Palauttaa merkkijonona viestissä esiintyvien kirjaimien frekvenssin.
    """
    kirjaimet = {}
    viesti = viesti.lower()
    viesti = viesti.replace(" ", "")
    for kirjain in viesti:
        if kirjain not in kirjaimet.keys():
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
    Brute forcen tulos tallentuu brute_force_tulos.txt tiedostoon.
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

                if etsi_sanoja_viestista(viesti, sanat):
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
    elif kieli == "EN":
        aakkoset = AAKKOSET_EN

    tiedosto = valitse_sanalista(kieli)

    viesti = viesti.lower().replace(" ", "")
    with open("vigenere_brute_force.txt", "w") as tulos, open(tiedosto) as sanat_tiedosto:
        
        sanat = load(sanat_tiedosto)

        for pituus in range(1, len(viesti) + 1):
            for yhdistelma in product(aakkoset, repeat=pituus):
                salasana = "".join(yhdistelma)
                yritys = vigeneren_salaus(viesti, salasana, kieli, True)

                if etsi_sanoja_viestista(yritys, sanat):
                    tulos.write(
                        "{} {}\n".format(
                            vigeneren_salaus(viesti, salasana, kieli, True),
                            salasana,
                        )
                    )


def etsi_sanoja_viestista(viesti, sanat):
    pituus = len(viesti)

    pituus = min(21, pituus)

    for i in range(1, pituus + 1):
        sana = viesti[0:i]

        if sana in sanat:
            break
    else:
        return False

    for j in range(1, pituus + 1):
        sana2 = viesti[len(viesti) - j : len(viesti)]

        if sana2 in sanat:
            break
    else:
        return False

    return True


def matriisisalaus(viesti, avain_a, avain_b, aakkoset, decrypt=False):
    """
    Viesti muunnetaan 2 x n matriisiksi ja kerrotaan 2 x 2 matriisilla avain_a, ja siihen 2 x 1 lisätään matriisi avain_b, joka "venytetään" n pituiseksi.
    """
    salaus = valitse_aakkoset(aakkoset)
    viesti_palat = wrap(viesti, 2)
    viesti_matriisi = []
    for pala in viesti_palat:
        pala_numeroina = muuta_viesti_numeroiksi(pala, aakkoset)
        if len(pala_numeroina) == 1:
            pala_numeroina.append(0)

        viesti_matriisi.append(pala_numeroina)

    viesti_matriisi = np.transpose(viesti_matriisi)
    avain_b = np.transpose([avain_b] * len(viesti_matriisi[0]))

    if not decrypt:
        muunnettu = (np.dot(avain_a, viesti_matriisi) + avain_b) % (len(salaus) // 2)
    else:
        kaannetty_avain = kaanteismatriisi(avain_a, len(salaus) // 2)
        if not isinstance(kaannetty_avain, bool):
            muunnettu = (
                np.dot(kaannetty_avain, viesti_matriisi)
                - np.dot(kaannetty_avain, avain_b)
            ) % (len(salaus) // 2)
        else:
            raise ValueError("Annetulla matriisilla ei ole käänteismatriisia")

    muunnettu_kirjaimina = ""
    for i, kirjain in enumerate(muunnettu[0]):
        muunnettu_kirjaimina += salaus[kirjain]
        muunnettu_kirjaimina += salaus[muunnettu[1][i]]

    return muunnettu_kirjaimina


def matriisisalaus_brute_force(viesti, kieli):
    """
    Tallentaa tuloksen "matriisisalaus_brute_force.txt tiedostoon.
    """
    salaus = valitse_aakkoset(kieli)
    tiedosto = valitse_sanalista(kieli)
    numerot = list(range(len(salaus) // 2))

    with open(tiedosto) as sanalista:
        sanat = load(sanalista)
        with open("matriisisalaus_brute_force.txt", "w") as tulos:
            for yrite in product(numerot, repeat=6):
                try:
                    avattu_viesti = matriisisalaus(
                        viesti,
                        [[yrite[0], yrite[1]], [yrite[2], yrite[3]]],
                        [yrite[4], yrite[5]],
                        kieli,
                        True,
                    )
                except ValueError:
                    continue

                if etsi_sanoja_viestista(avattu_viesti, sanat):
                    tulos.write("{} {}\n".format(avattu_viesti, yrite))


def kaanteismatriisi(matriisi, n):
    """
    Laskee 2 X 2 matriisin käänteismatriisin joukossa z_n
    """

    det = (matriisi[0][0] * matriisi[1][1] - matriisi[0][1] * matriisi[1][0]) % n
    if det == 0:
        return False

    kaanteisluku = diofantoksen_yhtalo_ratkaisu(n, det, 1)[1]

    uusi_matriisi = (
        kaanteisluku
        * np.array(
            [
                [matriisi[1][1], -1 * matriisi[0][1]],
                [-1 * matriisi[1][0], matriisi[0][0]],
            ]
        )
        % n
    )

    return uusi_matriisi


def paloittelumenetelma(viesti, avain, aakkoset, z, decrypt=False):
    """
    n = kirjainten lukumaara - 1
    Etsitään mahdollisimman suuri k siten, että kun kirjoitetaann luku n k kertaa peräkkäin, niin luku on pienempi kuin jäännösluokka z.
    Sitten viesti jaetaan k:n pituisiin osiin, jotka tulkitaan yhtenä lukuna, jotka taas kerrotaan avaimella ja salataan viesti.
    Salattu viesti syötetään merkkijonona.
    """
    salaus = valitse_aakkoset(aakkoset)
    n = len(salaus) // 2 - 1
    k = 0
    temp = 0

    while temp < z:
        k += 1
        temp = int(str(n) * k)

    k -= 1

    if k < 1:
        raise ValueError("Liian pieni z:n arvo.")

    if not decrypt:
        viesti = viesti.lower().replace(" ", "")
        osat = wrap(viesti, k)
        osat_numeroina = []
        for osa in osat:
            osa = muuta_viesti_numeroiksi(osa, aakkoset)
            osa = [str(numero).zfill(k) for numero in osa]
            osa = "".join(osa)
            osat_numeroina.append(int(osa))
    else:
        osat_numeroina = [int(osa) for osa in wrap(viesti, k * 2)]

    if decrypt:
        avain = diofantoksen_yhtalo_ratkaisu(z, avain, 1)[1]

    muunnettu = [str(osa * avain % z).zfill(k * 2) for osa in osat_numeroina]

    if decrypt:
        kirjaimet = ""
        for osa in muunnettu:
            osat = wrap(str(osa), k)
            osat = [int(numero) for numero in osat]
            kirjaimet += muuta_numerot_kirjaimiksi(osat, aakkoset)

        return kirjaimet

    return muunnettu


def kantamenetelma(viesti, avain, aakkoset, z, decrypt=False):
    """
    Valitaan mahdollisimman iso k siten, että len(aakkoset) ** k < z.
    Viesti jaetaan k pituisiin paloihin ja palat esitetään muodossa kirjain1 * len(aakkoset) ** (k - 1) + kirjain2 * len(aakkoset) ** (k - 2) + ... + kirjain_n * 1
    Palat kerrotaan avaimella ja palat esitetään len(aakkoset) kantaisena lukuna, jolloin salattu viesti voidaan esittää tekstinä.
    """
    salaus = valitse_aakkoset(aakkoset)
    kirjaimien_maara = len(salaus) // 2
    k = 0

    while kirjaimien_maara ** k < z:
        k += 1

    k -= 1

    if k < 1:
        raise ValueError("Liian pieni z:n arvo.")

    viesti_numeroina = muuta_viesti_numeroiksi(viesti, aakkoset)

    if decrypt:
        avain = diofantoksen_yhtalo_ratkaisu(z, avain, 1)[1]
        potenssi = k
    else:
        potenssi = k - 1

    muunnetut_osat = []
    viesti_numeroina_iter = iter(viesti_numeroina)
    for i in range(len(viesti_numeroina) // k + 1):
        summa = 0
        try:
            for j in range(potenssi, -1, -1):

                summa += kirjaimien_maara ** j * next(viesti_numeroina_iter)
        except StopIteration:
            break

        muunnetut_osat.append(summa * avain % z)

    if decrypt:
        potenssi2 = k - 1
    else:
        potenssi2 = k

    muunnettu_viesti = ""
    for numero in muunnetut_osat:
        muunnettu_viesti += muuta_numerot_kirjaimiksi(
            kantamenetelma_kertoimet(numero, potenssi2, kirjaimien_maara), aakkoset
        )

    return muunnettu_viesti


def kantamenetelma_kertoimet(numero, k, kanta):
    kertoimet = []
    summa = 0
    for i in range(k, -1, -1):
        kerroin = (numero - summa) // kanta ** i
        summa += kerroin * kanta ** i
        kertoimet.append(kerroin)

    return kertoimet


def RSA_salaus(data, avain, n):
    """
    Avain on joko julkinen avain tai dekryptauseksponentti riippuen siitä salataanko vai avataanko dataa.
    """

    salattu_data = potenssiinkorotus_joukossa_z(data, avain, n)
    return salattu_data


def RSA_salaus_allekirjoituksella(
    data,
    julkinen_avain,
    dekryptauseksponentti,
    n_a,
    n_b,
    decrypt=False,
    allekirjoitus=None,
):
    """
    a = lähettäjä
    b = vastaanottaja
    n_a < n_b
    """
    if not decrypt:
        salattu_data = RSA_salaus(data, julkinen_avain, n_b)
        allekirjoitus = RSA_salaus(data, dekryptauseksponentti, n_a)
        salattu_allekirjoitus = RSA_salaus(allekirjoitus, julkinen_avain, n_b)

        return salattu_data, salattu_allekirjoitus

    avattu_data = RSA_salaus(data, dekryptauseksponentti, n_b)
    avattu_allekirjoitus = RSA_salaus(allekirjoitus, dekryptauseksponentti, n_b)
    vahvistettu_allekirjoitus = RSA_salaus(avattu_allekirjoitus, julkinen_avain, n_a)

    return avattu_data, avattu_data == vahvistettu_allekirjoitus


def potenssiinkorotus_joukossa_z(kantaluku, eksponentti, z):
    eksponentti_binaari = bin(eksponentti).lstrip("0b")

    pituus = len(eksponentti_binaari)
    tulo = 1

    for i in range(pituus):
        if eksponentti_binaari[pituus - i - 1] == "1":
            tulo = tulo * kantaluku % z

        kantaluku = kantaluku ** 2 % z

    return tulo


def laske_dekryptauseksponentti(alkuluku1, alkuluku2, julkinen_avain):
    n = (alkuluku1 - 1) * (alkuluku2 - 1)

    return diofantoksen_yhtalo_ratkaisu(n, julkinen_avain, 1)[1] % n


def murra_rsa(n, julkinen_avain):
    """
    Toimii, kun n on korkeintaan 100 merkkiä pitkä.
    Jakaa n:n käyttämällä neliöseulaa SymPy moduulista.
    """
    tekijat = list(
        qs(
            n,
            2000,
            10000,
        )
    )

    return laske_dekryptauseksponentti(tekijat[0], tekijat[1], julkinen_avain)


def kryptausiteraatio(salattu_data, julkinen_avain, n, toistot):
    """
    Yrittää dekryptata datan kryptausfunktio-iteraatioilla.
    """
    muunnettu_data = salattu_data
    for i in range(toistot):
        edellinen = muunnettu_data
        muunnettu_data = potenssiinkorotus_joukossa_z(muunnettu_data, julkinen_avain, n)
        if muunnettu_data == salattu_data:
            return edellinen

    return None 


def diffie_hellman_avaimenvaihto(salainen_avain_a, julkinen_avain_b, z):
    """
    Palauttaa käyttäjien a ja b yhteisen salausavaimen.
    """
    return potenssiinkorotus_joukossa_z(julkinen_avain_b, salainen_avain_a, z)


def diffie_hellman_julkinen_avain(generaattori, eksponentti, z):

    return potenssiinkorotus_joukossa_z(generaattori, eksponentti, z)


def elgamal_salaus(data, yhteinen_avain, z, decrypt=False):
    """
    Viesti kerrotaan yhteisellä avaimella.
    Avatessa käytetään yhteisen avaimen käänteisalkiota.
    """
    if decrypt:
        yhteinen_avain = diofantoksen_yhtalo_ratkaisu(z, yhteinen_avain, 1)[1] % z

    return data * yhteinen_avain % z


def selkareppu(
    data,
    julkinen_avain=None,
    decrypt=False,
    z=None,
    salainen_avain=None,
    salainen_avain_luku=None,
):
    """
    Jokaisen käyttäjän salainen avain on superkasvava numerojono, eli seuraavan jonon jäsenen arvo on suurempi kuin edellisten jäsenien summa.
    Julkinen avain saadaan, kun salainen avain kerrotaan jollain salaisella luvulla (mod z).
    Data esitetään binäärimuodossa ja kerrotaan vastaavat ykköset julkisen avaimen vastaavalla numerolla ja summataan yhteen.
    """
    summa = 0

    if not decrypt:
        data = bin(data).lstrip("0b")
        for i, bitti in enumerate(data):
            if bitti == "1":
                summa += julkinen_avain[i]

        return summa

    salainen_avain_luku = diofantoksen_yhtalo_ratkaisu(z, salainen_avain_luku, 1)[1] % z
    data = salainen_avain_luku * data % z
    salainen_avain.reverse()
    binaari_data = ""
    for luku in salainen_avain:
        if data - summa >= luku:
            binaari_data += "1"
            summa += luku
        else:
            binaari_data += "0"

    avattu = 0
    for i, bitti in enumerate(binaari_data):
        if bitti == "1":
            avattu += 2 ** i

    return avattu


def selkareppu_julkinen_avain(salainen_avain, salainen_avain_luku, z):
    julkinen_avain = []
    for luku in salainen_avain:
        julkinen_avain.append(luku * salainen_avain_luku % z)

    return julkinen_avain


def murra_selkareppu(julkinen_avain, salattu_data):
    """
    Yrittää murtaa selkärepun lll-algoritmilla.
    http://www.cs.sjsu.edu/faculty/stamp/papers/topics/topic16/Knapsack.pdf
    """
    julkinen_avain_kopio = julkinen_avain.copy()
    julkinen_avain_kopio.append(-1 * salattu_data)
    matriisi = np.identity(len(julkinen_avain_kopio))
    matriisi[-1] = julkinen_avain_kopio
    vektorit = np.transpose(matriisi)
    lll_muunnetut_vektorit = lll_algoritmi(vektorit)

    for vektori in lll_muunnetut_vektorit:
        for numero in vektori:
            if numero not in [0, 1]:
                break
        else:
            vektori = list(map(str, vektori.astype(int)))
            data = "".join(vektori)

            return int(data, 2)

    return "murtaminen ei onnistunut"


def lll_algoritmi(vektorit):
    vektorit = np.array(vektorit)
    indeksi = 1
    while indeksi < len(vektorit):
        gram_schimdt_vektorit = laske_gram_schimdt_vektorit(vektorit, indeksi)
        vahennetty_vektori = vektorit[indeksi]
        for i in range(indeksi - 1, -1, -1):
            kerroin = np.dot(vektorit[indeksi], gram_schimdt_vektorit[i]) / np.dot(
                gram_schimdt_vektorit[i], gram_schimdt_vektorit[i]
            )
            if abs(kerroin) > 0.5:
                vahennetty_vektori = vahenna_vektorit(
                    vektorit[i], vahennetty_vektori, gram_schimdt_vektorit[i]
                )
                vektorit[indeksi] = vahennetty_vektori
                gram_schimdt_vektorit = laske_gram_schimdt_vektorit(vektorit, indeksi)

        if lovasz_ehto(
            vahennetty_vektori,
            gram_schimdt_vektorit[indeksi - 1],
            gram_schimdt_vektorit[indeksi],
        ):
            indeksi += 1

        else:
            vektorit[[indeksi, indeksi - 1]] = vektorit[[indeksi - 1, indeksi]]
            indeksi = max([1, indeksi - 1])

    return vektorit


def vahenna_vektorit(v1, v2, v1_gram_schimdt_vektori):

    v1 = np.array(v1)
    v2 = np.array(v2)
    v1_gram_schimdt_vektori = np.array(v1_gram_schimdt_vektori)

    return v2 - (
        round(
            np.dot(v2, v1_gram_schimdt_vektori)
            / np.dot(v1_gram_schimdt_vektori, v1_gram_schimdt_vektori)
        )
        * v1
    )


def lovasz_ehto(v2, v1_gram_schimdt, v2_gram_schimdt):
    v1_suuruus = sum([i ** 2 for i in v1_gram_schimdt])
    v2_suuruus = sum([i ** 2 for i in v2_gram_schimdt])
    kerroin = np.dot(v2, v1_gram_schimdt) / np.dot(v1_gram_schimdt, v1_gram_schimdt)

    return v2_suuruus >= (0.75 - kerroin ** 2) * v1_suuruus


def laske_gram_schimdt_vektori(kasiteltava_vektori, gram_schmidt_vektorit):
    alku_vektori = np.array(kasiteltava_vektori).astype(float)
    kasiteltava_vektori = alku_vektori
    for vektori in gram_schmidt_vektorit:
        vektori = np.array(vektori).astype(float)
        uusi_vektori = (
            np.dot(kasiteltava_vektori, vektori) / np.dot(vektori, vektori) * vektori
        )

        uusi_vektori = uusi_vektori.astype(float)
        alku_vektori -= uusi_vektori

    return alku_vektori


def laske_gram_schimdt_vektorit(vektorit, indeksi):
    """
    Laskee gram-schmidt vektorit tiettyyn indeksiin asti.
    """
    vektorit = np.array(vektorit[0 : indeksi + 1])
    gram_schimdt_vektorit = []
    for vektori in vektorit:
        vektori = np.array(vektori).astype(float)
        gram_schimdt_vektorit.append(
            laske_gram_schimdt_vektori(vektori, gram_schimdt_vektorit)
        )

    return gram_schimdt_vektorit


if __name__ == "__main__":

    print(murra_selkareppu([82, 123, 287, 83, 248, 373, 10, 471], 548))
