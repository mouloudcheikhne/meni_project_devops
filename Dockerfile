FROM python:3.13-slim

WORKDIR /app

# COPY requirements.txt /app
RUN pip install -r flask

COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]

