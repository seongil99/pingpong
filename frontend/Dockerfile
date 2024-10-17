FROM nginx:1.27.2

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY index.html /usr/share/nginx/html/index.html
COPY ./src /usr/share/nginx/html/src
COPY cert.crt /etc/ssl/cert.crt
COPY cert.key /etc/ssl/cert.key

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]