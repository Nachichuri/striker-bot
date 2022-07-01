FROM python:3.10.5-slim

WORKDIR /bot
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]