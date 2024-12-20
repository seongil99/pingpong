FROM nginx:1.27.2

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY index.html /usr/share/nginx/html/index.html
COPY favicon.ico /usr/share/nginx/html/favicon.ico
COPY ./src /usr/share/nginx/html/src

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
