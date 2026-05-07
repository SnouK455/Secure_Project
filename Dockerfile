FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup -S appgroup && adduser -S -G appgroup appuser

COPY requirements.txt .
RUN apk add --no-cache --upgrade xz-libs \
    && pip install --no-cache-dir --upgrade "pip>=26.1" \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
