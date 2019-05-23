FROM python:3.7
MAINTAINER itswcg

COPY . /Todo-Python
WORKDIR /Todo-Python

RUN pip3 install -r requirements.txt
EXPOSE 8511

ENTRYPOINT ["gunicorn", "-w", "2", "todo.wsgi", "-e", "DJANGO_SETTINGS_MODULE=todo.settings", "-b", "0.0.0.0:8511"]
