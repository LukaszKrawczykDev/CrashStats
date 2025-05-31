# Etap buildowania
FROM node:20 AS build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Etap produkcyjny
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80