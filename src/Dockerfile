FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src/ /app/src/

#CMD ["sleep", "10000"]
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "80"]
