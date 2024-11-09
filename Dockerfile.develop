FROM nginx:1.27.2

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./cert.crt /etc/nginx/cert.crt
COPY ./cert.key /etc/nginx/cert.key

CMD ["nginx", "-g", "daemon off;"]