FROM tiangolo/uvicorn-gunicorn:python3.7

WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt




COPY ./app /app
COPY ./gunicorn_conf.py /
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8050
CMD /start.sh