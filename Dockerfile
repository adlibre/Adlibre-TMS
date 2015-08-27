FROM panubo/python-bureaucrat

COPY . /srv/git

RUN source /srv/ve27/bin/activate && \
    export SECRET_KEY=build && \
    cd /srv/git && \
    pip install --upgrade pip && \
    pip install --allow-external py-dom-xpath --allow-unverified py-dom-xpath py-dom-xpath && \
    pip install -r requirements.txt
