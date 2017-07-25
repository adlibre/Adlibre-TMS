FROM panubo/python-bureaucrat:2.7

COPY . /srv/git

RUN source /srv/ve27/bin/activate && \
    export SECRET_KEY=build && \
    cd /srv/git && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENV WORKERS=4
