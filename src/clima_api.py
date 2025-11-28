import requests
import json


# Configuración
API_KEY = "6c4e0e4fcc96a74332ae12d6a03a00b5"
CIUDAD = "Mexico City"
URL = "http://api.openweathermap.org/data/2.5/weather"

def obtener_datos_clima():
    """
    Consulta la API y devuelve un diccionario.
    """
    print(f"Consultando clima para: {CIUDAD}...")
    
    params = {
        'q': CIUDAD,
        'appid': API_KEY,
        'units': 'metric' # Para tener grados Celsius
    }

    try:
        respuesta = requests.get(URL, params=params)
        
        # Si la respuesta es exitosa (Código 200)
        if respuesta.status_code == 200:
            data = respuesta.json()
            
            # Extracción de datos (Parsing)
            clima_principal = data['weather'][0]['main'] # Ej: Rain, Clear, Clouds
            temperatura = data['main']['temp']
            
            # Detectar si es de día o noche (usando el timestamp y sys.time)
            # si termina en 'n' es noche
            icono = data['weather'][0]['icon']
            es_de_dia = 'd' in icono

            info_procesada = {
                "status": "ok",
                "tipo": clima_principal,  # Rain, Clear, Clouds, Thunderstorm
                "temp": temperatura,
                "dia": es_de_dia
            }
            
            print("Datos recibidos correctamente.")
            return info_procesada
            
        else:
            print(f"Error en la API: {respuesta.status_code}")
            return {"status": "error", "tipo": "Clear", "temp": 20, "dia": True}

    except Exception as e:
        print(f"Error de conexión: {e}")
        # Datos default por si no hay internet (Fail-safe)
        return {"status": "error", "tipo": "Clear", "temp": 20, "dia": True}

# Bloque de prueba (solo corre si ejecutas este archivo directamente)
if __name__ == "__main__":
    resultado = obtener_datos_clima()
    print("\nREPORTE PARA FARAH ")
    print(json.dumps(resultado, indent=4))