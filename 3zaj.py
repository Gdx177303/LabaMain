import requests
import json
import tkinter as tk
from PIL import Image, ImageTk
import requests
import io

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
class GaleriaNASA:
    def __init__(self, root):
        self.root = root
        self.root.title("Galeria NASA")
        self.root.geometry("900x600")
        self.root.configure(bg="black")
        self.image_refs = []

        self.lewy_panel = tk.Frame(self.root, bg="black", width=200)
        self.lewy_panel.pack(side="left", fill="y")

        self.prawy_panel = tk.Frame(self.root, bg="black")
        self.prawy_panel.pack(side="right", fill="both", expand=True)

        self.gora_panel = tk.Frame(self.lewy_panel, bg="black")
        self.gora_panel.pack(pady=10)

        self.entry = tk.Entry(self.gora_panel, fg="green", bg="black", insertbackground="green")
        self.entry.pack(side="left")

        self.search_btn = tk.Button(self.gora_panel, text="Szukaj", command=self.wyszukaj, bg="black", fg="green")
        self.search_btn.pack(side="left", padx=5)

        self.podglad = tk.Canvas(self.prawy_panel, bg="black")
        self.podglad.pack(fill="both", expand=True)

    def wyszukaj(self):
        for widget in self.lewy_panel.winfo_children():
            if widget != self.gora_panel:
                widget.destroy()
        self.image_refs.clear()

        zapytanie = self.entry.get()
        if not zapytanie:
            return

        try:
            api = NasaAPI(zapytanie)
            obrazy = api.get_images()

            if not obrazy:
                etykieta = tk.Label(self.lewy_panel, text="Brak wyników", fg="green", bg="black")
                etykieta.pack()
                return

            for item in obrazy[:10]:
                links = item.get("links", [])
                if not links:
                    continue

                href = links[0].get("href")
                if not href:
                    continue

                response = requests.get(href)
                img_data = response.content
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(img)

                etykieta = tk.Label(self.lewy_panel, image=photo, bg="black")
                etykieta.image = photo
                etykieta.pack(pady=5)
                etykieta.bind("<Button-1>", lambda e, url=href: self.pokaz_obraz(url))

                self.image_refs.append(etykieta)

        except Exception as e:
            blad = tk.Label(self.lewy_panel, text=f"Błąd: {e}", fg="red", bg="black")
            blad.pack()

    def pokaz_obraz(self, url):
        response = requests.get(url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((600, 600))
        photo = ImageTk.PhotoImage(img)

        self.podglad.delete("all")
        self.podglad.create_image(300, 300, image=photo)
        self.podglad.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = GaleriaNASA(root)
    root.mainloop()
