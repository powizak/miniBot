# Dockerfile for frontend miniBot (React)

FROM node:20-alpine AS build

WORKDIR /app
COPY . .

# Install dependencies and run tests if TEST=true (for CI/CD)
ARG TEST=false
RUN npm install
RUN if [ "$TEST" = "true" ]; then npm test; fi

# Build static files
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

ENV FRONTEND_PORT=3000
EXPOSE ${FRONTEND_PORT}
CMD ["nginx", "-g", "daemon off;"]