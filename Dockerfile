FROM python:3.7
RUN pip install selenium
COPY ./marketingpreferences.py /app/marketingpreferences.py
ENTRYPOINT ["python", "/app/marketingpreferences.py"]
CMD []
