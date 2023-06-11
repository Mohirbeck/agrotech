FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./run.sh /run.sh

ENV LISTEN_PORT=80
ENV APP_HOST=http://127.0.0.1
ENV APP_PORT=8000
ENV SERVER_NAME=127.0.0.1

USER root
RUN chmod +x /run.sh
COPY ./media /app/media
COPY ./static /app/static
EXPOSE 80

CMD ["/run.sh"]