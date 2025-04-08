import requests
import json

class NasaAPI:
    def __init__(self, query): 
        self.url = "https://images-api.nasa.gov/search"
        self.query = query
        self.params = {'q': self.query}

    def fetch_data(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Nie udało się pobrać pliku: {response.status_code}')

    def get_images(self):
        data = self.fetch_data()
        return data.get("collection", {}).get("items", [])

def main():
    query = input("Podaj zapytanie: ")
    try:
        nasa_api = NasaAPI(query)
        items = nasa_api.get_images()

        if not items:
            print("Brak wyników")
            return
        
        for item in items[:5]:
            item_data = item.get("data", [])
            title = item_data[0].get("title", "Brak tytułu") if item_data else "Brak tytułu"

            links = item.get("links", []) 
            href = links[0].get("href", "Brak linku") if links else "Brak linku"

            print(f"Tytuł: {title}")
            print(f"Link: {href}")
            print("-" * 40)
    
    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":  
    main()