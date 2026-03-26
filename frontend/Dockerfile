FROM harbor.pg.innopolis.university/docker-hub-cache/caddy:2.11-alpine

# Copy Caddyfile
COPY frontend/Caddyfile /etc/caddy/Caddyfile

# Expose ports
EXPOSE 80 443

# Run Caddy
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
