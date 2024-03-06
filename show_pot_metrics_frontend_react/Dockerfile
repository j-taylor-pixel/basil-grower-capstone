FROM node:18-alpine

WORKDIR /show_pot_metrics_frontend_react/

COPY public/ /show_pot_metrics_frontend_react/public
COPY src/ /show_pot_metrics_frontend_react/src
COPY package.json /show_pot_metrics_frontend_react/

RUN npm install

CMD ["npm", "start"]