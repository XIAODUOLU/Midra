FROM node:20-alpine AS build
WORKDIR /app
RUN npm config set registry https://registry.npmmirror.com
COPY frontend/package.json /app/package.json
RUN npm install
COPY frontend /app
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
