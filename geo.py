from geopy.geocoders import Nominatim
import time
import pandas as pd
geolocator = Nominatim(user_agent="senegal_mapper")

def geocode_location(location):
    if not location or pd.isna(location):
        return None, None

    try:
        loc = geolocator.geocode(location + ", Sénégal", timeout=10)
        time.sleep(1)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None
    except Exception as e:
        print("Geocoding error:", e)
        return None, None
    

geo_map = {
    # Villes principales
    "Dakar, Sénégal": (14.7167, -17.4677),
    "Thies, Sénégal": (14.7833, -16.9167),
    "Mbour, Sénégal": (14.4194, -16.9633),
    "Rufisque, Sénégal": (14.7167, -17.2737),
    "Saint Louis, Sénégal": (16.0439, -16.4896),
    "Diamniadio, Sénégal": (14.7266, -17.1897),
    "Niaga, Sénégal": (14.8353, -17.2376),

    # Zones touristiques / hors Dakar
    "Saly, Sénégal": (14.4416, -17.0069),
    "Lac rose, Sénégal": (14.8434, -17.2324),

    # Banlieues & grandes communes
    "Pikine, Sénégal": (14.7646, -17.3907),
    "Keur Massar, Sénégal": (14.7846, -17.3222),

    # Quartiers de Dakar
    "Almadies, Dakar, Sénégal": (14.7461, -17.5198),
    "Almadies 2, Dakar, Sénégal": (14.7450, -17.5175),
    "Guediawaye, Dakar, Sénégal": (14.7736, -17.3994),
    "Mbao, Dakar, Sénégal": (14.7156, -17.3186),
    "Sicap Liberté, Dakar, Sénégal": (14.7085, -17.4566),
    "Sicap foire, Dakar, Sénégal": (14.7312, -17.4516),
    "Dieuppeul-Derklé, Dakar, Sénégal": (14.7128, -17.4487),
    "Mariste, Dakar, Sénégal": (14.7072, -17.4260),
    "Hann Bel-Air, Dakar, Sénégal": (14.7223, -17.4266),
    "Sacré-Coeur, Dakar, Sénégal": (14.7044, -17.4586),
    "Mermoz-Sacré Coeur, Dakar, Sénégal": (14.6971, -17.4954),
    "Ouakam, Dakar, Sénégal": (14.7472, -17.4936),
    "Mamelles, Dakar, Sénégal": (14.7494, -17.5108),
    "Fann, Dakar, Sénégal": (14.7000, -17.4667),
    "Point E, Dakar, Sénégal": (14.6932, -17.4691),
    "Dakar Plateau, Dakar, Sénégal": (14.6708, -17.4370),
    "HLM, Dakar, Sénégal": (14.7066, -17.4467),
    "Ouest Foire, Dakar, Sénégal": (14.7369, -17.4582),
    
    
     # DAKAR - QUARTIERS
    "Mariste, Dakar, Sénégal": (14.7072, -17.4260),
    "Cambérène, Dakar, Sénégal": (14.7468, -17.4559),
    "Point E, Dakar, Sénégal": (14.6958, -17.4660),
    "Mbao, Dakar, Sénégal": (14.7156, -17.3186),
    "Mermoz-Sacré Coeur, Dakar, Sénégal": (14.6940, -17.4800),
    "Parcelle Assainies, Dakar, Sénégal": (14.7475, -17.4370),
    "Dieuppeul-Derklé, Dakar, Sénégal": (14.7128, -17.4487),
    "Sipres, Dakar, Sénégal": (14.7200, -17.4300),
    "Grand Dakar, Dakar, Sénégal": (14.7030, -17.4440),
    "Grand Yoff, Dakar, Sénégal": (14.7430, -17.4550),
    "Yoff, Dakar, Sénégal": (14.7565, -17.4735),
    "Hann Bel-Air, Dakar, Sénégal": (14.7223, -17.4266),
    "HLM, Dakar, Sénégal": (14.7250, -17.4400),
    "Ouakam, Dakar, Sénégal": (14.7219, -17.4936),
    "Ouest Foire, Dakar, Sénégal": (14.7400, -17.4850),
    "Diamalaye 1, Dakar, Sénégal": (14.7470, -17.4700),
    "Sicap Liberté, Dakar, Sénégal": (14.7085, -17.4566),
    "Dakar Plateau, Dakar, Sénégal": (14.6700, -17.4300),
    "Guediawaye, Dakar, Sénégal": (14.7736, -17.3994),

    # BANLIEUE
    "Keur Massar, Sénégal": (14.7861, -17.3222),
}
