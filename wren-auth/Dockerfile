FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --production

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
COPY --from=builder /app/.env .env

EXPOSE 5173
ENV NODE_ENV=production
ENV PORT=5173
ENV ORIGIN=https://aux.s-c.ai
CMD ["node", "build" ]
