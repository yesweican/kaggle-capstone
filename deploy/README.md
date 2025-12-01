# ============================================================================
# deploy/README.md
# ============================================================================
"""
# Deploying MarketReportAgent to Vertex AI Agent Engine

This guide walks you through deploying your MarketReportAgent to Google Cloud's Vertex AI Agent Engine.

## Prerequisites

1. **Google Cloud Project**
   - Active GCP project with billing enabled
   - Project ID noted for deployment

2. **Required APIs**
   Enable these APIs in your project:
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable run.googleapis.com
   ```

3. **Authentication**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth application-default login
   ```

4. **IAM Permissions**
   Your account needs these roles:
   - Vertex AI Administrator
   - Service Account User
   - Cloud Functions Developer (if using Cloud Functions)

## Deployment Steps

### Step 1: Update Configuration

Edit `agent_engine_config.yaml` with your project details:
- `project_id`: Your GCP project ID
- `location`: Your preferred region (e.g., us-central1)
- `agent_engine_id`: Unique identifier for your agent

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
pip install google-cloud-aiplatform
```

### Step 3: Run Deployment Script

```bash
# From the project root directory
python deploy/deploy.py
```

Or deploy manually:

```bash
# Set environment variables
export PROJECT_ID="your-project-id"
export LOCATION="us-central1"
export AGENT_ENGINE_ID="market-report-agent"

# Deploy using gcloud (if available)
gcloud ai agents deploy \
  --project=$PROJECT_ID \
  --location=$LOCATION \
  --agent-id=$AGENT_ENGINE_ID \
  --config=deploy/agent_engine_config.yaml
```

### Step 4: Verify Deployment

```bash
# List deployed agents
gcloud ai agents list --project=$PROJECT_ID --location=$LOCATION

# Test the deployed agent
python deploy/test_deployed_agent.py
```

## Configuration Options

### Environment Variables for Production

Set these in Agent Engine:
```yaml
GOOGLE_GENAI_USE_VERTEXAI: "TRUE"
GOOGLE_CLOUD_PROJECT: "your-project-id"
GOOGLE_CLOUD_LOCATION: "us-central1"
```

### Scaling Configuration

Adjust in `agent_engine_config.yaml`:
- `min_instances`: Minimum number of instances (default: 1)
- `max_instances`: Maximum number of instances (default: 10)
- `concurrency`: Requests per instance (default: 80)

## Monitoring and Logs

View logs:
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=market-report-agent" \
  --limit 50 \
  --format json
```

Monitor in Cloud Console:
- Navigate to Vertex AI > Agent Engine
- Select your agent
- View metrics, logs, and traces

## Updating Deployed Agent

After making code changes:

```bash
# Re-run deployment script
python deploy/deploy.py

# Or update manually
gcloud ai agents update $AGENT_ENGINE_ID \
  --project=$PROJECT_ID \
  --location=$LOCATION \
  --config=deploy/agent_engine_config.yaml
```

## Troubleshooting

**Issue: Authentication errors**
- Solution: Run `gcloud auth application-default login`

**Issue: API not enabled**
- Solution: Enable required APIs listed in Prerequisites

**Issue: Permission denied**
- Solution: Check IAM roles for your service account

**Issue: Agent not responding**
- Solution: Check logs with the monitoring command above

## Cost Considerations

- Vertex AI Agent Engine pricing: Pay per request + compute time
- Estimate: ~$0.50-2.00 per 1000 requests (varies by model and region)
- Monitor usage in Cloud Console > Billing

## Rollback

To rollback to a previous version:

```bash
gcloud ai agents revisions list --agent=$AGENT_ENGINE_ID
gcloud ai agents revisions deploy REVISION_ID
```

## Additional Resources

- [Vertex AI Agent Engine Documentation](https://cloud.google.com/vertex-ai/docs/agent-engine)
- [Google ADK Documentation](https://cloud.google.com/vertex-ai/docs/adk)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
"""

