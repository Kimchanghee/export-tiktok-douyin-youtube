# Video Downloader - Deployment Guide

## 🚀 Google Cloud Run Deployment

### Prerequisites

1. **Google Cloud Account**
   - Create account at https://cloud.google.com
   - Enable billing

2. **Install Google Cloud SDK**
   ```bash
   # Download from: https://cloud.google.com/sdk/docs/install
   gcloud init
   gcloud auth login
   ```

3. **Enable Required APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

### Deployment Steps

#### 1. Set Project Variables

```bash
export PROJECT_ID="your-project-id"
export SERVICE_NAME="video-downloader"
export REGION="us-central1"  # or your preferred region

gcloud config set project $PROJECT_ID
```

#### 2. Build and Push Docker Image

**Option A: Using Cloud Build (Recommended)**

```bash
# Build in Cloud
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Or with specific Dockerfile
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME -f Dockerfile .
```

**Option B: Local Build and Push**

```bash
# Build locally
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .

# Configure Docker for GCR
gcloud auth configure-docker

# Push to Google Container Registry
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME
```

#### 3. Deploy to Cloud Run

```bash
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars "FLASK_ENV=production" \
  --set-env-vars "SECRET_KEY=$(openssl rand -base64 32)"
```

#### 4. Get Service URL

```bash
gcloud run services describe $SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --format 'value(status.url)'
```

Your service will be available at: `https://video-downloader-XXXXX-uc.a.run.app`

---

## 🐳 Local Development with Docker

### Build and Run Locally

```bash
# Build image
docker build -t video-downloader .

# Run container
docker run -p 8080:8080 \
  -e FLASK_ENV=development \
  -e SECRET_KEY=dev-secret-key \
  video-downloader

# Or use docker-compose
docker-compose up --build
```

Access at: http://localhost:8080

### Stop and Clean Up

```bash
# Stop container
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker rmi video-downloader
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8080` |
| `FLASK_ENV` | Environment (development/production) | `production` |
| `SECRET_KEY` | Flask secret key | Required in production |
| `MAX_CONTENT_LENGTH` | Max upload size | `500MB` |

### Cloud Run Settings

**Recommended Settings:**
- **Memory**: 2 GiB (for video processing)
- **CPU**: 2 vCPU
- **Timeout**: 300 seconds (5 minutes)
- **Max instances**: 10 (adjust based on traffic)
- **Min instances**: 0 (to save costs)

---

## 📊 Monitoring

### View Logs

```bash
# Stream logs
gcloud run services logs tail $SERVICE_NAME \
  --platform managed \
  --region $REGION

# View logs in Cloud Console
gcloud run services logs read $SERVICE_NAME
```

### Health Check

```bash
# Check service health
curl https://your-service-url/api/health

# Expected response:
# {"status":"healthy","service":"video-downloader"}
```

---

## 🔒 Security

### Enable Authentication (Optional)

```bash
# Deploy with authentication required
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --no-allow-unauthenticated
```

### Access Authenticated Service

```bash
# Get auth token
gcloud auth print-identity-token

# Make authenticated request
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  https://your-service-url/api/health
```

---

## 💰 Cost Optimization

### Cloud Run Pricing (as of 2024)

- **Free Tier**: 2 million requests/month
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million requests

### Tips to Reduce Costs

1. **Set Min Instances to 0**
   ```bash
   --min-instances 0
   ```

2. **Use Auto-scaling**
   ```bash
   --max-instances 10
   ```

3. **Optimize Timeout**
   ```bash
   --timeout 300  # 5 minutes max
   ```

4. **Clean Up Old Revisions**
   ```bash
   gcloud run revisions list
   gcloud run revisions delete REVISION_NAME
   ```

---

## 🐛 Troubleshooting

### Common Issues

**1. Build Fails**
```bash
# Check build logs
gcloud builds log --stream

# Verify Dockerfile syntax
docker build -t test .
```

**2. Service Won't Start**
```bash
# Check service logs
gcloud run services logs tail $SERVICE_NAME

# Verify environment variables
gcloud run services describe $SERVICE_NAME
```

**3. Timeout Errors**
```bash
# Increase timeout
gcloud run services update $SERVICE_NAME --timeout 600
```

**4. Out of Memory**
```bash
# Increase memory
gcloud run services update $SERVICE_NAME --memory 4Gi
```

---

## 🔄 Update Deployment

### Update Service

```bash
# Rebuild and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION
```

### Rollback

```bash
# List revisions
gcloud run revisions list

# Rollback to previous revision
gcloud run services update-traffic $SERVICE_NAME \
  --to-revisions REVISION_NAME=100
```

---

## 📝 CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Setup Cloud SDK
      uses: google-github-actions/setup-gcloud@v0
      with:
        project_id: ${{ secrets.GCP_PROJECT_ID }}
        service_account_key: ${{ secrets.GCP_SA_KEY }}

    - name: Build and Push
      run: |
        gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/video-downloader

    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy video-downloader \
          --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/video-downloader \
          --platform managed \
          --region us-central1 \
          --allow-unauthenticated
```

---

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)

---

Made by WITHYM
