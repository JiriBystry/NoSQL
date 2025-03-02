FROM python:3
WORKDIR /NoSQL
COPY requirements.txt /NoSQL
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
