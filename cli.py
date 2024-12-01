import json
import requests

API_URL = "http://localhost:8000"

options = {
    "1": "Búsqueda semantica tweets",
    "2": "Búsqueda agrupada por sentimiento tweets",
    "3": "Búsqueda de tweets por fecha",
    "4": "Búsqueda de usuarios con más seguidores creados en x año",
    "5": "Filtrar tweets por tópicos",
    "6": "Filtrar tweets por usuario",
    "7": "Filtrar tweets por hashtag",
    "8": "Ver interacciones de tweets por tópicos",
    "9": "Ver interacciones de tweets por usuario",
    "10": "Ver interacciones de tweets por hashtag",
    "11": "Ver relaciones de usuarios por likes y retweets",
    "12": "Ver clasificación de respuestas a tweets"
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
        elif selection == "3":
            year = input("Ingresa el año (default: 2014) (solo hay datos de 2014): ") or "2014"
            month = input("Ingresa el mes (default: 9) (solo hay datos del mes 9): ") or "9"
            day = input("Ingresa el día (25-27), (default: 26) (solo hay datos del 25 al 27)): ") or "26"
            limit = input("Ingresa el límite de resultados (default 20): ") or "20"
            response = requests.get(f"{API_URL}/tweets-by-date?year={year}&month={month}&day={day}&limit={limit}")
        elif selection == "4":
            year = input("Ingresa el año (default: 2010): ") or "2010"
            min_followers = input("Ingresa el mínimo de seguidores (default: 0): ") or "0"
            max_followers = input("Ingresa el máximo de seguidores (default: 100000): ") or "100000"
            limit = input("Ingresa el límite de resultados (default 100): ") or "100"
            response = requests.get(f"{API_URL}/users-by-followers?year={year}&min_followers={min_followers}&max_followers={max_followers}&limit={limit}")
        elif selection == "5":
            topic = input("Ingresa el tópico: ")
            response = requests.get(f"{API_URL}/tweets/by_topic?topic={topic}")
        elif selection == "6":
            user_id = input("Ingresa el ID del usuario: ")
            response = requests.get(f"{API_URL}/tweets/by_user?user_id={user_id}")
        elif selection == "7":
            hashtag = input("Ingresa el hashtag: ")
            response = requests.get(f"{API_URL}/tweets/by_hashtag?hashtag={hashtag}")
        elif selection == "8":
            topic = input("Ingresa el tópico: ")
            response = requests.get(f"{API_URL}/interactions/by_topic?topic={topic}")
        elif selection == "9":
            user_id = input("Ingresa el ID del usuario: ")
            response = requests.get(f"{API_URL}/interactions/by_user?user_id={user_id}")
        elif selection == "10":
            hashtag = input("Ingresa el hashtag: ")
            response = requests.get(f"{API_URL}/interactions/by_hashtag?hashtag={hashtag}")
        elif selection == "11":
            response = requests.get(f"{API_URL}/user_relations")
        elif selection == "12":
            tweet_id = input("Ingresa el ID del tweet: ")
            response = requests.get(f"{API_URL}/tweet_responses?tweet_id={tweet_id}")
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