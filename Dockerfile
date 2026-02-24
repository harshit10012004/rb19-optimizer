# Multi-stage build = Production optimized
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY . .
EXPOSE 8080
CMD ["streamlit", "run", "src/dashboard.py", "--server.port=8080", "--server.address=0.0.0.0"]
