import requests

class google:
    BAZOWY_URL = "https://images-api.nasa.gov/search"
    
    def __init__(self, zapytanie: str):
        self.zapytanie = zapytanie
    
    def szukaj_obrazow(self):
        parametry = {"q": self.zapytanie, "media_type": "image"}
        odpowiedz = requests.get(self.BAZOWY_URL, params=parametry)
        
        if odpowiedz.status_code == 200:
            dane = odpowiedz.json()
            elementy = dane.get("collection", {}).get("items", [])
            
            linki_obrazow = []
            for element in elementy:
                linki = element.get("links", [])
                if linki:
                    linki_obrazow.append(linki[0]["href"])
            return linki_obrazow
        else:
            return []

if __name__ == "__main__":
    zapytanie = input("Wprowadź zapytanie do wyszukania: ")
    wyszukiwarka = google(zapytanie)
    wyniki = wyszukiwarka.szukaj_obrazow()
    
    if wyniki:
        print("Znalezione obrazy:")
        for url in wyniki[:5]:
            print(url)
    else:
        print("Nic nie znaleziono.")
