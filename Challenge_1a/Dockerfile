FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

COPY extract_outline.py /app/extract_outline.py
COPY utils.py /app/utils.py

RUN pip install --no-cache-dir pdfminer.six

CMD ["python", "extract_outline.py"]
