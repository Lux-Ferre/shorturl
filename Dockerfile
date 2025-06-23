FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8005

CMD ["gunicorn", "--bind", "0.0.0.0:8005", "--workers=1", "app:create_app()"]
