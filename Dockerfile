FROM python:3.11
WORKDIR /app
COPY requirements.txt code
RUN pip install -r requirements.txt --no-cache-dir
COPY ./app /app
EXPOSE 5000
CMD python run.py