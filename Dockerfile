FROM mcr.microsoft.com/playwright/python:v1.65.1-noble

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "tests", "-v"]