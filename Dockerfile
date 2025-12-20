# 1. version de python
FROM python:3.9-slim

# 2. creacion de la carpeta
WORKDIR /app

# 3. copiar e instalar los requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. copiar el contenido de farah_adventures al contenedor
COPY . .

# 5. ejecutar comando por defecto
CMD ["python", "src/clima_api.py"]