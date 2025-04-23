FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY entrypoint.sh ./

RUN chmod +x entrypoint.sh
EXPOSE 5000 8501
ENTRYPOINT ["/app/entrypoint.sh"]