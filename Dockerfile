FROM python

COPY . /manufactorum
WORKDIR /manufactorum

RUN pip install --upgrade pip
RUN pip install -r /manufactorum/requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "manufactorum:app"]
