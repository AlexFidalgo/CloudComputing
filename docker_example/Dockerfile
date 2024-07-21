# Use the official Nginx base image from the Docker Hub
FROM nginx:latest

# Copy the static HTML file to the Nginx web server directory
COPY index.html /usr/share/nginx/html/

# Expose port 80 to the host
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
