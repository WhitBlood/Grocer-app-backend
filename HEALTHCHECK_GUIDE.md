# 🏥 Health Check Guide

Complete guide to monitoring your FreshMart backend health.

## 📊 Available Health Endpoints

### 1. `/health` - Detailed Health Check

**URL:** `http://localhost:8000/health`

**Response (Healthy):**
```json
{
  "status": "healthy",
  "service": "FreshMart API",
  "version": "1.0.0",
  "database": "connected"
}
```

**Response (Unhealthy):**
```json
{
  "status": "unhealthy",
  "service": "FreshMart API",
  "version": "1.0.0",
  "database": "disconnected: connection refused"
}
```

**Use Case:** Monitoring, debugging, detailed status

---

### 2. `/ready` - Readiness Check

**URL:** `http://localhost:8000/ready`

**Response (Ready):**
```json
{
  "status": "ready"
}
```

**Response (Not Ready):**
```
HTTP 503 Service Unavailable
{
  "detail": "Service not ready: connection refused"
}
```

**Use Case:** Kubernetes readiness probe, load balancer checks

---

### 3. `/` - Basic Status

**URL:** `http://localhost:8000/`

**Response:**
```json
{
  "message": "FreshMart API is running!",
  "version": "1.0.0",
  "status": "healthy"
}
```

**Use Case:** Quick check if API is responding

---

## 🐳 Docker Health Checks

### Check Container Health

```bash
# View health status
docker ps

# Look for "healthy" in STATUS column
# Example: Up 2 minutes (healthy)
```

**Status Indicators:**
- `starting` - Container is starting, health check not yet run
- `healthy` - All health checks passing
- `unhealthy` - Health checks failing

### View Health Check Logs

```bash
# Inspect health check details
docker inspect freshmart-backend | grep -A 10 Health

# View last 5 health check results
docker inspect --format='{{json .State.Health}}' freshmart-backend | jq
```

### Manual Health Check

```bash
# Run health check script
docker exec freshmart-backend python healthcheck.py

# Or use curl
docker exec freshmart-backend curl -f http://localhost:8000/health
```

---

## 🔍 Monitoring Commands

### 1. Quick Health Check

```bash
# Check if backend is healthy
curl http://localhost:8000/health

# Pretty print
curl -s http://localhost:8000/health | jq
```

**Expected Output:**
```json
{
  "status": "healthy",
  "service": "FreshMart API",
  "version": "1.0.0",
  "database": "connected"
}
```

---

### 2. Check All Services

```bash
# Check all Docker containers
docker-compose ps

# Should show:
# freshmart-postgres   healthy
# freshmart-backend    healthy
# freshmart-frontend   Up
```

---

### 3. Continuous Monitoring

```bash
# Watch health status (updates every 2 seconds)
watch -n 2 'curl -s http://localhost:8000/health | jq'

# Or with Docker
watch -n 2 'docker ps --filter name=freshmart'
```

---

### 4. Check Database Connection

```bash
# Test database directly
docker exec freshmart-postgres pg_isready -U freshmart

# Should output: accepting connections
```

---

## 🚨 Troubleshooting

### Issue: Container shows "unhealthy"

**Check logs:**
```bash
docker-compose logs backend
```

**Common causes:**
1. Database not ready
2. Port conflict
3. Environment variables missing
4. Database connection failed

**Solution:**
```bash
# Restart services
docker-compose restart backend

# Or rebuild
docker-compose up -d --build backend
```

---

### Issue: Health check timeout

**Increase timeout in docker-compose.yml:**
```yaml
healthcheck:
  timeout: 30s  # Increase from 10s
  start_period: 60s  # Increase from 40s
```

---

### Issue: Database not connected

**Check database health:**
```bash
# Check postgres is running
docker-compose ps postgres

# Check postgres logs
docker-compose logs postgres

# Test connection
docker exec freshmart-backend python test_db.py
```

---

## 📈 Health Check Configuration

### Docker Compose Health Check

Located in `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import requests; r = requests.get('http://localhost:8000/health'); exit(0 if r.status_code == 200 and r.json().get('database') == 'connected' else 1)"]
  interval: 30s      # Check every 30 seconds
  timeout: 10s       # Timeout after 10 seconds
  retries: 3         # Retry 3 times before marking unhealthy
  start_period: 40s  # Wait 40s before first check
```

**Adjust for your needs:**
- Increase `interval` for less frequent checks
- Increase `timeout` for slow responses
- Increase `start_period` for slow startup
- Increase `retries` for flaky connections

---

### Dockerfile Health Check

Located in `BackEnd/Dockerfile`:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; response = requests.get('http://localhost:8000/health'); exit(0 if response.status_code == 200 and response.json().get('database') == 'connected' else 1)" || exit 1
```

---

## 🎯 Production Monitoring

### 1. External Monitoring Services

**UptimeRobot (Free):**
- Monitor: `https://your-domain.com/health`
- Alert on downtime

**Pingdom:**
- HTTP check on `/health`
- Response time monitoring

**Datadog:**
- Container health metrics
- Custom health check alerts

---

### 2. Kubernetes Probes

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

### 3. Load Balancer Health Checks

**AWS ALB:**
- Health check path: `/health`
- Success codes: 200
- Interval: 30 seconds

**Nginx:**
```nginx
upstream backend {
    server backend:8000 max_fails=3 fail_timeout=30s;
}

location /health {
    proxy_pass http://backend/health;
}
```

---

## 📊 Health Check Script Usage

### Run Manually

```bash
# From BackEnd directory
python healthcheck.py

# Output:
# ✅ Health check passed: {'status': 'healthy', ...}
# Exit code: 0
```

### Use in Scripts

```bash
#!/bin/bash
# wait-for-backend.sh

echo "Waiting for backend to be healthy..."

for i in {1..30}; do
    if python healthcheck.py; then
        echo "Backend is healthy!"
        exit 0
    fi
    echo "Attempt $i/30 failed, retrying in 5s..."
    sleep 5
done

echo "Backend failed to become healthy"
exit 1
```

---

## 🔔 Alerting Examples

### Slack Webhook

```python
import requests

def check_and_alert():
    response = requests.get('http://localhost:8000/health')
    data = response.json()
    
    if data.get('status') != 'healthy':
        # Send Slack alert
        requests.post('https://hooks.slack.com/services/YOUR/WEBHOOK/URL', json={
            'text': f"🚨 Backend unhealthy: {data}"
        })
```

### Email Alert

```python
import smtplib
from email.message import EmailMessage

def send_alert(status):
    msg = EmailMessage()
    msg['Subject'] = 'FreshMart Backend Alert'
    msg['From'] = 'alerts@freshmart.com'
    msg['To'] = 'admin@freshmart.com'
    msg.set_content(f'Backend status: {status}')
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('user', 'password')
        smtp.send_message(msg)
```

---

## 📝 Health Check Checklist

When deploying, verify:

- [ ] `/health` endpoint returns 200
- [ ] Database status is "connected"
- [ ] Docker container shows "healthy"
- [ ] Health checks pass consistently
- [ ] Monitoring alerts configured
- [ ] Load balancer health checks working
- [ ] Logs show no health check errors

---

## 🎉 Quick Reference

```bash
# Check backend health
curl http://localhost:8000/health

# Check readiness
curl http://localhost:8000/ready

# Check Docker health
docker ps | grep freshmart-backend

# View health logs
docker inspect freshmart-backend | grep -A 10 Health

# Run health check script
python BackEnd/healthcheck.py

# Watch continuously
watch -n 2 'curl -s http://localhost:8000/health | jq'
```

---

Your backend now has comprehensive health monitoring! 🏥✅
