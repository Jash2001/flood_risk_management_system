FROM node:18-alpine

# Install Ionic CLI
RUN npm install -g @ionic/cli

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8100

CMD ["ionic", "serve", "--host=0.0.0.0", "--port=8100", "--disable-host-check"]
