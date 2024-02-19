import requests

# asemoiden IDt
def getAsemaIDt() -> list:
    asemaIDt = [
        "C01674",   # Helsinki, Ruoholahti
        "C08576",   # Joensuu, Repokallio
        "C09510",   # Jyväskylä, Vaajakoski
        "C12547",   # Kajaani
        "C08538",   # Kuopio, Siikalahti
        "C10538",   # Lapua
        "C12504",   # Oulu, Laanila
        "C14547",   # Rovaniemi, Revontuli_1
        "C10501",   # Seinäjoki, Nurmo
        "C04555",   # Tampere, Rautaharkko
        "C02520",   # Turku, Kärsämäki
        "C10523"    # Vaasa, Kotiranta
        ]
    
    return asemaIDt

# kelikameroiden koordinaatit
def getKoordinaatit() -> list:
    """
    Palauttaa listan, joka sisältää listat kelikameroiden koordinaateista.
    Hakee kelikameroiden tiedot Digitarfficilta.
    """
    asemaIDt = getAsemaIDt()
    kaikkiKoordinaatit = []

    for asemaID in asemaIDt:
        asema = "https://tie.digitraffic.fi/api/weathercam/v1/stations/" + asemaID
        koordinaatit = requests.get(asema).json()["geometry"]["coordinates"]
        kaikkiKoordinaatit.append(koordinaatit)

    return kaikkiKoordinaatit

# kelikameroiden koordinaatit
def getKuvat() -> list:
    """
    Palauttaa listan, joka sisältää listat kelikameroiden kuvista.
    Hakee kelikameroiden tiedot Digitarfficilta.
    """
    asemaIDt = getAsemaIDt()
    kaikkiKuvat = []

    for asemaID in asemaIDt:
        kamerat = "https://tie.digitraffic.fi/api/weathercam/v1/stations/" + asemaID + "/data"
        kuvat = []

        for kamera in requests.get(kamerat).json()["presets"]:
            kuvat.append("https://weathercam.digitraffic.fi/" + kamera["id"] + ".jpg")
        kaikkiKuvat.append(kuvat)

    return kaikkiKuvat

def main():
    print(getKoordinaatit())
    print(getKuvat())

if __name__ == "__main__":
    main()
