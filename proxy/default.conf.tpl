server {
    listen ${LISTEN_PORT};
    server_name ${SERVER_NAME};

    location /static/ {
        root /app/static/;
    }

    location /media/ {
        root /app/media/;
    }

    location / {
        proxy_pass              ${APP_HOST}:${APP_PORT};
        client_max_body_size    10M;
    }
}