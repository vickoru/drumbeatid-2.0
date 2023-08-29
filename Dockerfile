FROM tensorflow/tensorflow:2.10.0

# COPY taxifare/ /taxifare
# COPY requirements.txt /requirements.txt

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

WORKDIR /prod

COPY requirements_prod.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY drumbeatid drumbeatid
COPY scripts scripts
COPY setup.py setup.py
RUN pip install -e .

CMD uvicorn drumbeatid.api.api:app --host 0.0.0.0 --port $PORT
