FROM python:3.11-slim

WORKDIR /srv

RUN pip install --no-cache-dir Flask

COPY app.py ./app.py

EXPOSE 8000
CMD ["python", "app.py"]
