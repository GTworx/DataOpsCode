FROM python:3.8-slim-buster

RUN python3 -m pip install --upgrade pip && python3 -m pip install pandas==1.3.5

COPY my_app.py my_app.py

CMD ["python3", "my_app.py"]