FROM python:latest

COPY server /server
WORKDIR /server
RUN pip install -r requirements.txt

EXPOSE 8765

ENTRYPOINT ["python", "-m", "blitz2020"]
