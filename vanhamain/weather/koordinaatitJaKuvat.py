import requests

# asemoiden IDt
def getAsemaIDt() -> list:
    """
    Palauttaa listan kelikamera-asemien koordinaateista. Kaupungit luetaan tiedostosta
    "kaupungit.txt". AsemaIDt ovat listassa samassa järjestyksessä kuin kaupungit.
    """
    kaupungit = []

    # luetaan kaupungit tiedostosta "kaupungit.txt"
    tiedosto = open("weather/kaupungit.txt")
    for rivi in tiedosto:
        kaupunki = rivi.split(":")[0].replace("Ã¤","ä")
        kaupungit.append(kaupunki)
    tiedosto.close()

    # haetaan kaikkien kelikamera-asemien tiedot Digitrafficilta
    asemat = "https://tie.digitraffic.fi/api/weathercam/v1/stations"
    tiedot = requests.get(asemat).json()["features"]

    # haetaan kaupunkeja vastaavat kelikameroiden koordinaatit ja laitetaan ne kyseisen
    # kaupungin kohdalle (vastaan tuleva ensimmäinen kaupungin kelikamera)
    for i in range(len(kaupungit)):
        for j in range(len(tiedot)):
            if tiedot[j]["properties"]["name"].split("_")[1] == kaupungit[i]:
                kaupungit[i] = tiedot[j]["id"]
    
    return kaupungit

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
        koordinaatit = requests.get(asema).json()["geometry"]["coordinates"][:2]
        koordinaatit.reverse()
        kaikkiKoordinaatit.append(koordinaatit)

    return kaikkiKoordinaatit

# kelikameroiden kuvat
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
