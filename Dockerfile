FROM python:3.11
WORKDIR /NoSQL
COPY requirements.txt /NoSQL
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 5001
CMD ["python", "run.py"]
