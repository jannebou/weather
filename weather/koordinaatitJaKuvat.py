import requests

# kelikameran kuvat
def getKoordinaatit(asemaID:str) -> list:
    asema = "https://tie.digitraffic.fi/api/weathercam/v1/stations/" + asemaID
    koordinaatit = requests.get(asema).json()["geometry"]["coordinates"]
    
    return koordinaatit

def getKuvat(asemaID:str) -> list:
    kamerat = "https://tie.digitraffic.fi/api/weathercam/v1/stations/" + asemaID + "/data"
    kuvat = []
    for kamera in requests.get(kamerat).json()["presets"]:
        kuvat.append("https://weathercam.digitraffic.fi/" + kamera["id"] + ".jpg")

    return kuvat

def main():
    asemaIDt = ["C01674",   # Helsinki, Ruoholahti
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

    koordinaatit = []
    kuvat = []
    for asemaID in asemaIDt:
        koordinaatit.append(getKoordinaatit(asemaID))
        kuvat.append(getKuvat(asemaID))

    print(koordinaatit)
    print(kuvat)

    # lähetetään koordinaatit ja kuvat palvelimelle
    """
    obj = koordinaatit
    response = requests.post("http://localhost:5000/kameroidenkoordinaatit", json = obj)
    print(response.ok, response.json())

    obj = kuvat
    response = requests.post("http://localhost:5000/kameroidenkuvat", json = obj)
    print(response.ok, response.json())
    """

if __name__ == "__main__":
    main()
