# Farah Adventures

Un juego infinito de estilo "Dino Chrome" protagonizado por Farah, desplegado con Docker.

## 1. Descripción
Farah Adventures es un videojuego de navegador donde controlas a un gato que corre automáticamente por los pasillos del ITAM. El objetivo es sobrevivir el mayor tiempo posible esquivando obstáculos académicos y distracciones.

El proyecto está contenerizado para garantizar que funcione en cualquier entorno sin necesidad de instalar dependencias locales.

## 2. Cómo Jugar
El juego es simple y adictivo:

Objetivo: Evitar chocar con los obstáculos (Libros, Personas, Cuarenteadas).

Controles:

Flecha Arriba : Saltar.

Flecha Abajo : Agacharse.

Game Over: Si tocas un obstáculo, el juego termina y se muestra tu puntuación final.

## 3. API de clima

El proyecto consume la API pública de OpenWeatherMap. Esto permite que el entorno del juego (o la aplicación) reaccione a las condiciones climáticas actuales de la Ciudad de México.
Del objeto JSON masivo que retorna la API, realizamos un proceso de filtrado para extraer únicamente las variables funcionales para nuestro sistema:

-> Campo: tipo

  Tipo de Dato: String
  
  Descripción: Condición principal del clima (ej. "Rain", "Clear", "Clouds").
  
  Fuente Original: weather[0]['main']

-> Campo: temp

  Tipo de Dato: Float
  
  Descripción: Temperatura actual en grados Celsius.
  
  Fuente Original: main['temp']

-> Campo: dia

  Tipo de Dato: Boolean
  
  Descripción: Indica si es de día (True) o de noche (False).
  
  Fuente Original: Derivado del análisis del string en weather[0]['icon']

-> Campo: status

  Tipo de Dato: String
  
  Descripción: Variable de control de flujo para saber si la petición fue exitosa ("ok") o fallida ("error").

Fuente Original: Código de estado HTTP
### Lógica de Extracción e Ingesta
El script de Python (weather_service.py) implementa un pipeline de extracción robusto con las siguientes características:

Petición HTTP: Utilizamos la librería requests para consultar el endpoint api.openweathermap.org/data/2.5/weather, enviando parámetros de autenticación (appid) y unidades métricas (units='metric').

Parsing Inteligente:

Detección Día/Noche: En lugar de calcular la hora local vs. la puesta de sol, analizamos el nombre del icono proporcionado por la API (ej. 01d vs 01n). Si contiene la letra 'd', determinamos que es de día.

Fail-Safe (Tolerancia a Fallos):

Implementamos un bloque try/except para manejar errores de conexión o caídas del servicio.

Fallback: Si la API no responde o no hay internet, el sistema no colapsa. En su lugar, inyecta datos "dummy" (Clima despejado, 20°C) para garantizar que la aplicación siga funcionando sin interrupciones.
