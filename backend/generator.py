def generate_dockerfile(language):
    language = language.lower()

    dockerfiles = {
        "python": """FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
""",

        "node": """FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
""",

        "java": """FROM eclipse-temurin:21-jdk

WORKDIR /app

COPY . .

RUN ./mvnw clean package

EXPOSE 8080

CMD ["java","-jar","target/app.jar"]
"""
    }

    return dockerfiles.get(language, "Language not supported.")