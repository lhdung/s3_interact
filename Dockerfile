FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install -no-cache-dir -r requirements.txt

EXPOSE 8000


# Run main.py when the container launches
CMD ["python", "code/main.py"]