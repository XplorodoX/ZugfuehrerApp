FROM node:16-slim

WORKDIR /user/src/app

COPY package.json ./
#COPY ./yarn.lock ./

RUN npm install

COPY . .

EXPOSE 80

CMD ["npm", "start"]

# Build step #1: build the React front end
#FROM node:16-alpine as build-step

#ENV PATH /app/node_modules/.bin:$PATH
#COPY package.json yarn.lock ./
#COPY ./src ./src
#COPY ./public ./public
#RUN yarn install
#RUN yarn build

# Build step #2: build an nginx container
#FROM nginx:stable-alpine
#COPY --from=build-step /app/build /usr/share/nginx/html
#COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf