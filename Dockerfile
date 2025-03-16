# Use multi-stage build for smaller final image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy all files
COPY . .

# Build the Next.js app
RUN npm run build

# Python stage
FROM python:3.9-slim AS python-builder

# Set working directory
WORKDIR /app

# Copy Python requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy built Next.js app from builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

# Copy Python environment
COPY --from=python-builder /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=python-builder /usr/local/bin/python /usr/local/bin/python
COPY --from=python-builder /usr/local/bin/pip /usr/local/bin/pip

# Copy Python code
COPY ml ./ml
COPY api ./api

# Install Python runtime
RUN apk add --no-cache python3

# Expose port
EXPOSE 3000

# Start both Next.js and Python API
CMD ["npm", "start"]

