# 🚂 Railway Deployment Guide

## Quick Deploy (5 Minutes)

### Step 1: Prepare Your Code

Make sure you have these files ready:
- `app_enhanced.py` (your main app)
- `requirements.txt` (dependencies)
- `Procfile` (Railway startup command)
- All other Python files

### Step 2: Create Procfile

Create a file named `Procfile` (no extension) with this content:

```
web: python app_enhanced.py
```

### Step 3: Update requirements.txt

Make sure it includes:

```
Flask==3.0.0
requests==2.31.0
schedule==1.2.0
cryptography==41.0.7
```

### Step 4: Push to GitHub

```bash
# If not already a git repo
git init

# Add all files
git add .

# Commit
git commit -m "Enhanced automation system"

# Push to GitHub
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

### Step 5: Deploy on Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Wait for it to detect Python

### Step 6: Add Environment Variables

In Railway dashboard:

1. Click on your service
2. Go to "Variables" tab
3. Add these:

```
KIE_API_KEY=b6950bc9ee85f941ecb523ce34efb4a0
BLOTATO_API_KEY=blt_sHvjFzyhDdrJOVlCTFhV+AlHMZyeRXjE6reQL52Qxmw=
OPENROUTER_API_KEY=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
SECRET_KEY=your-random-secret-key-here-123456789
```

### Step 7: Deploy

Railway will automatically:
1. Install dependencies
2. Run your app
3. Give you a public URL

### Step 8: Access Your App

1. Click "View Logs" to see startup
2. Click the domain URL (e.g., `lively-healing.up.railway.app`)
3. Your dashboard should load!

---

## Troubleshooting

### "Application failed to start"

Check logs for errors:
```
railway logs
```

Common issues:
- Missing dependencies → Update requirements.txt
- Wrong Python version → Add runtime.txt with `python-3.11.0`
- Port issues → Railway auto-assigns port, app handles it

### "Can't connect to service"

Make sure:
- App is running: Check Railway dashboard
- No deployment errors: Check logs
- Domain is active: Click on the generated URL

### "API keys not working"

Verify in Railway:
1. Variables tab
2. Check all 4 keys are set
3. No extra spaces or quotes
4. Click "Redeploy" after adding variables

---

## Auto-Deploy Setup

Enable automatic deploys when you push to GitHub:

1. Railway → Settings
2. Find "Watch Paths"
3. Enable it
4. Now every git push automatically deploys!

---

## Custom Domain (Optional)

Want your own domain?

1. Railway → Settings → Domains
2. Click "Generate Domain" for free subdomain
3. Or add custom domain:
   - Add your domain
   - Update DNS records
   - Wait for verification

---

## Scaling

Your app will start on Railway's free tier.

To scale:
1. Railway → Settings
2. Increase resources:
   - More CPU
   - More memory
   - More instances

Cost starts at $5/month for basic plan.

---

## Monitoring

### View Logs
```
Railway dashboard → Logs tab
```

### Check Metrics
```
Railway dashboard → Metrics tab
```

Shows:
- CPU usage
- Memory usage
- Request count
- Response times

### Health Check

Your app has a health endpoint:
```
https://your-app.up.railway.app/health
```

Returns:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-21T...",
  "ai_available": true
}
```

---

## Updating Your App

### Method 1: Git Push (Recommended)

```bash
# Make changes
git add .
git commit -m "Update feature X"
git push

# Railway auto-deploys!
```

### Method 2: Manual Deploy

1. Railway dashboard
2. Click "Deploy"
3. Select "Latest commit"

---

## Environment-Specific Settings

### Development
```bash
# Run locally
python app_enhanced.py
```

### Production (Railway)
```bash
# Railway automatically runs:
python app_enhanced.py
```

Railway sets `PORT` environment variable automatically.

---

## Backup & Safety

### Database Backup

Your database is stored on Railway's filesystem.

To backup:
1. Download `automation.db` from Railway
2. Use Railway CLI:
   ```
   railway files download automation.db
   ```

### API Key Security

- Keys are stored encrypted in database
- Railway environment variables are secure
- Never commit keys to GitHub
- Always use `.gitignore` for sensitive files

---

## Cost Optimization

### Free Tier
- $5 free credit per month
- Good for testing
- Limited resources

### Starter Plan ($5/month)
- Enough for 1-2 workflows
- ~30 videos per month
- Suitable for personal use

### Pro Plan ($20/month)
- Multiple workflows
- ~120 videos per month
- For serious creators

**Pro Tip:** Video generation (Sora) costs more than Railway hosting. Focus on optimizing video count, not server resources.

---

## Quick Commands

```bash
# View logs
railway logs

# Open dashboard
railway open

# Run command
railway run python setup.py

# Connect to service
railway shell

# Download file
railway files download automation.db

# Upload file
railway files upload automation.db
```

---

## Support

### Railway Support
- https://railway.app/help
- Discord: https://discord.gg/railway

### Your App Support
- Use the chat interface
- Check logs in Railway
- GitHub issues for bugs

---

## Checklist

Before going live:

- [ ] All API keys added to Railway
- [ ] Procfile exists
- [ ] requirements.txt updated
- [ ] GitHub connected
- [ ] Auto-deploy enabled
- [ ] Tested on Railway URL
- [ ] Health check returns OK
- [ ] Chat interface works
- [ ] Can create workflows
- [ ] Videos generate successfully

---

**You're all set! 🚀**

Your automation system is now running 24/7 in the cloud!

Access it at: https://your-app.up.railway.app
