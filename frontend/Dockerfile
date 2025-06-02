# Etap 1 – build Vite
FROM node:20 AS build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Etap 2 – produkcja z NGINX
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80