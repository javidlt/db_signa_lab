import json
import requests

API_URL = "http://localhost:8000"

options = {
    "1": "Busqueda semantica tweets",
    "2": "Busqueda agrupada por sentimiento tweets"
}
sentiments = {
    "1": "1 star",
    "2": "2 stars",
    "3": "3 stars",
    "4": "4 stars",
    "5": "5 stars"
}

def main():
    while True:
        print("Selecciona una opción:")
        for key, value in options.items():
            print(f"{key}. {value}")
        selection = input("Select (default 1): ") or "1"
        
        if selection == "1":
            query = (input("Ingresa el término de búsqueda (default: 'mala situación'): ") or "mala situación").replace(" ", "%20")
            limit = input("Ingresa el límite de resultados (default 10): ") or "10"
            page = input("Ingresa el número de página (default 1): ") or "1"
            response = requests.get(f"{API_URL}/tweets/semantic?query={query}&limit={limit}&page={page}")
        elif selection == "2":
            print("Selecciona un sentimiento:")
            for key, value in sentiments.items():
                print(f"{key}. {value}")
            sentiment_selection = input("Select (default 1): ") or "1"
            sentiment = sentiments.get(sentiment_selection, "1 star")
            limit = input("Ingresa el límite de resultados (default 10): ") or "10"
            page = input("Ingresa el número de página (default 1): ") or "1"
            response = requests.get(f"{API_URL}/tweets/by_sentiment?sentiment={sentiment}&limit={limit}&page={page}")
        else:
            print("Opción no válida")
            continue

        if response.status_code == 200:
            print("Resultados:")
            print(json.dumps(response.json(), indent=4))
        else:
            print("Error en la consulta:", response.status_code)

        try:
            input("Presiona Enter para continuar o Ctrl+C para salir...")
        except KeyboardInterrupt:
            print("""\n
                Cómo ve, ¿Solido 100?
                Gracias por usar el programa de parte de Javi, Carlushe y el Saiker (Saizar) 
            """)
            break

if __name__ == "__main__":
    main()