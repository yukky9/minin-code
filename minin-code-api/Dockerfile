FROM python:3.12

WORKDIR /app

EXPOSE 8082

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--config", "config/gunicorn.py", "--reload", "app:app"]
