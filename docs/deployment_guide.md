# Deployment Guide

## Introduction

This guide provides instructions for deploying the Kurdistan Calendar API to production environments. It covers several deployment options and best practices for ensuring reliability, performance, and security.

## Deployment Options

The Kurdistan Calendar API can be deployed in several ways, depending on your requirements and infrastructure:

1. **Docker Containers**: Recommended for most deployments
2. **Platform as a Service (PaaS)**: Simple deployment with minimal configuration
3. **Virtual Private Server (VPS)**: Traditional deployment with full control
4. **Serverless**: For minimal maintenance and automatic scaling

## Prerequisites

Before deploying, ensure you have:

- The latest stable version of the codebase
- Access to your hosting environment
- Domain name (optional but recommended)
- SSL certificate (recommended for production)

## Docker Deployment (Recommended)

### 1. Build the Docker Image

The repository includes a Dockerfile for containerizing the application:

```bash
# Build the Docker image
docker build -t kurdistan-calendar-api:latest .
```

### 2. Run the Container

```bash
# Run the container
docker run -d -p 80:8000 --name kurdistan-calendar-api kurdistan-calendar-api:latest
```

### 3. Docker Compose (Optional)

For more complex setups, use Docker Compose:

```yaml
# docker-compose.yml
version: '3'

services:
  api:
    build: .
    ports:
      - "80:8000"
    environment:
      - MAX_WORKERS=4
      - LOG_LEVEL=info
      - ALLOWED_ORIGINS=https://example.com,https://www.example.com
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## PaaS Deployment (Heroku, Railway, etc.)

### Heroku Deployment

1. **Create a Heroku app**:

```bash
heroku create kurdistan-calendar-api
```

2. **Add the Heroku-specific files**:

Create a `Procfile` in the root directory:

```
web: uvicorn api.main:app --host=0.0.0.0 --port=${PORT:-8000}
```

3. **Deploy to Heroku**:

```bash
git push heroku main
```

### Railway Deployment

1. Create a new project in Railway
2. Connect your GitHub repository
3. Railway will automatically detect the Python environment and deploy

## VPS Deployment

For deployment on a VPS (like DigitalOcean, AWS EC2, or Linode):

### 1. Set up the server

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx
```

### 2. Clone the repository

```bash
git clone https://github.com/kurdistan-calendar-api/kurdistan-calendar-api.git
cd kurdistan-calendar-api
```

### 3. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Set up Gunicorn

```bash
pip install gunicorn
```

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/kurdistan-calendar-api.service
```

Add the following content:

```
[Unit]
Description=Kurdistan Calendar API
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/path/to/kurdistan-calendar-api
Environment="PATH=/path/to/kurdistan-calendar-api/venv/bin"
ExecStart=/path/to/kurdistan-calendar-api/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl start kurdistan-calendar-api
sudo systemctl enable kurdistan-calendar-api
```

### 5. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/kurdistan-calendar-api
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name api.kurdistancalendar.org;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/kurdistan-calendar-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Set up SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.kurdistancalendar.org
```

## Serverless Deployment

### AWS Lambda with Mangum

1. **Install Mangum**:

```bash
pip install mangum
```

2. **Modify `main.py`**:

```python
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# ... your API routes ...

# Add this at the end of the file
handler = Mangum(app)
```

3. **Package the application**:

```bash
pip install -r requirements.txt -t ./package
cp -r api ./package/
```

4. **Create a ZIP file**:

```bash
cd package
zip -r ../lambda_function.zip .
```

5. **Deploy to AWS Lambda**:
   - Create a new Lambda function in the AWS Console
   - Upload the ZIP file
   - Set the handler to `api.main.handler`
   - Configure API Gateway as a trigger

## Environment Variables

Configure the following environment variables in your deployment environment:

| Variable | Description | Default |
|----------|-------------|---------|
| `MAX_WORKERS` | Number of worker processes | `1` |
| `LOG_LEVEL` | Logging level (debug, info, warning, error) | `info` |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | `*` |
| `RATE_LIMIT_PER_MINUTE` | Rate limit requests per minute | `100` |
| `RATE_LIMIT_PER_DAY` | Rate limit requests per day | `5000` |

## Production Best Practices

### 1. Security

- Always use HTTPS in production
- Set up proper CORS headers
- Implement rate limiting
- Keep dependencies updated

### 2. Performance

- Use a CDN for high-traffic scenarios
- Enable Gzip compression
- Consider caching strategies
- Monitor and optimize database access

### 3. Monitoring

- Set up logging to a central service
- Implement health check endpoints
- Use monitoring tools (e.g., Prometheus, Grafana, Datadog)
- Set up alerts for critical issues

### 4. CI/CD

- Implement continuous integration tests
- Set up automated deployments
- Use environment-specific configurations
- Implement blue-green deployments for zero downtime

### 5. Backup and Recovery

- Regularly back up the `holidays.json` file
- Document the recovery process
- Test the recovery process periodically

## Scaling Considerations

The Kurdistan Calendar API is designed to be lightweight and efficient. For most use cases, a single instance should be sufficient. However, if you need to scale:

- Use a load balancer to distribute traffic among multiple instances
- Implement a caching layer (e.g., Redis) for frequently accessed data
- Consider CDN caching for static responses

## Troubleshooting

### Common Issues

1. **API not responding**:
   - Check the application logs
   - Verify the service is running
   - Check network configurations

2. **High memory usage**:
   - Adjust the number of workers
   - Check for memory leaks
   - Consider using a larger instance

3. **Slow response times**:
   - Implement caching
   - Optimize database queries
   - Use performance profiling tools

## Updating the Deployed API

To update the API with new code:

1. **Pull the latest changes**:
   ```bash
   git pull origin main
   ```

2. **Rebuild (if using Docker)**:
   ```bash
   docker build -t kurdistan-calendar-api:latest .
   docker stop kurdistan-calendar-api
   docker rm kurdistan-calendar-api
   docker run -d -p 80:8000 --name kurdistan-calendar-api kurdistan-calendar-api:latest
   ```

3. **Restart the service (if using systemd)**:
   ```bash
   sudo systemctl restart kurdistan-calendar-api
   ```

## Support

If you encounter issues during deployment:

1. Check the [GitHub repository](https://github.com/kurdistan-calendar-api/kurdistan-calendar-api) for known issues
2. Open a new issue with details about your deployment environment and the problem
3. Contact the maintainers for urgent issues 