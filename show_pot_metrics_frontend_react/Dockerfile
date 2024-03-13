# Use the official Node.js 18 Alpine image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /show_pot_metrics_frontend_react/

# Copy package.json and package-lock.json (if available)
COPY public/ /show_pot_metrics_frontend_react/public
COPY src/ /show_pot_metrics_frontend_react/src
COPY package.json /show_pot_metrics_frontend_react/

# Install dependencies
RUN npm install --only=production

# Copy the rest of the application code

# Build the React app
RUN npm run build

# Install a lightweight web server
RUN npm install -g serve

# Expose the port the app runs on
#EXPOSE 5000

# Serve the built app with the lightweight server
CMD ["serve", "-s", "build"]