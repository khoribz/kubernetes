FROM python:3.11-slim

WORKDIR /opt

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "main.py"]