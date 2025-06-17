import googlemaps
import os

API_KEY = os.getenv("Maps_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

def get_directions(origin: str, destination: str):
    """
    Busca rotas entre uma origem e um destino.
    """
    try:
        directions_result = gmaps.directions(origin, destination, mode="transit")
        return directions_result
    except Exception as e:
        print(f"Google Maps Directions Error: {e}")
        return None

def find_nearby_places(location: str, keyword: str, radius: int = 1500):
    """
    Encontra lugares próximos (ex: 'restaurantes') de um dado endereço.
    """
    try:
        geocode_result = gmaps.geocode(location)
        if not geocode_result:
            return None
        
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        
        places_result = gmaps.places_nearby(location=(lat, lng), radius=radius, keyword=keyword)
        return places_result
    except Exception as e:
        print(f"Google Maps Places Error: {e}")
        return None