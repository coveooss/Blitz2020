FROM python

COPY localsetup localsetup/

COPY server/blitz2020 server/blitz2020
COPY server/requirements.txt server/requirements.txt

WORKDIR /server
RUN pip install -r requirements.txt
RUN pip install pyinstaller
RUN pyinstaller --onefile -n blitz2020  blitz2020/__main__.py

RUN chmod +x dist/blitz2020

WORKDIR /localsetup
RUN pip install -r requirements.txt

WORKDIR /
RUN cp server/dist/blitz2020 blitz2020
RUN rm -rf server

COPY ui/dist/ ui/dist/
COPY server/game_presets server/game_presets/

RUN mkdir /replays
VOLUME [ "/replays" ]

# This is not perfect, but that should prevent at least some poeple from exec'ing into
# the running container
RUN rm /bin/*

EXPOSE 8765 8080

ENTRYPOINT ["python", "-m", "localsetup"]
