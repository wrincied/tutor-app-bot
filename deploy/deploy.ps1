# One-shot deploy helper for Cloud Run (run from bot/)
param(
  [string]$Project = "tutorassis",
  [string]$Region = "europe-west4",
  [string]$Service = "simple4u-bot",
  [string]$WebhookBaseUrl = ""
)

$ErrorActionPreference = "Stop"

gcloud config set project $Project

gcloud run deploy $Service `
  --source . `
  --region $Region `
  --allow-unauthenticated `
  --memory 512Mi `
  --cpu 1 `
  --min-instances 0 `
  --max-instances 3 `
  --set-secrets "TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN:latest,BOT_API_SECRET=BOT_API_SECRET:latest,WEBHOOK_SECRET=WEBHOOK_SECRET:latest" `
  --set-env-vars "BOT_MODE=webhook,BINDING_STORE=firestore,BOT_USERNAME=simp1e4ubot,PUBLIC_SITE_URL=https://simple4u.at,BACKEND_URL=https://tutor-app-backend--tutorassis.europe-west4.hosted.app,WEBHOOK_PATH=/telegram/webhook,GCP_PROJECT=$Project$(if ($WebhookBaseUrl) { ",WEBHOOK_BASE_URL=$WebhookBaseUrl" } else { '' })"

$url = gcloud run services describe $Service --region $Region --format "value(status.url)"
Write-Host ""
Write-Host "Deployed: $url"
Write-Host "Health:   $url/health"
if (-not $WebhookBaseUrl) {
  Write-Host ""
  Write-Host "Next: set webhook base URL (once):"
  Write-Host "  .\deploy\deploy.ps1 -WebhookBaseUrl $url"
}
