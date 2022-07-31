FROM nginx/unit:1.27.0-python3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /usr/src/craft

WORKDIR /usr/src/craft

COPY requirements.txt /usr/src/craft/

RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r requirements.txt                                       \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

COPY . /usr/src/craft/

RUN python manage.py collectstatic --noinput

EXPOSE 80

ENTRYPOINT ["/usr/src/craft/entrypoint.sh"]
