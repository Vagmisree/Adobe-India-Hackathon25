FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

COPY process_documents.py /app/process_documents.py
COPY pdf_utils.py /app/pdf_utils.py
COPY nlp_utils.py /app/nlp_utils.py
COPY approach_explanation.md /app/approach_explanation.md

RUN pip install --no-cache-dir pdfminer.six sentence-transformers numpy

CMD ["python", "process_documents.py"]
