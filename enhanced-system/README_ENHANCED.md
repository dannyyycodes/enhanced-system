# 🎬 Video Automation System - Enhanced Edition

**Your AI-Powered Workflow Management Platform**

Build unlimited automation workflows by simply chatting with AI. No coding required!

---

## ✨ What's New in Enhanced Edition

### 🤖 **Lovable.ai-Style Chat Interface**
- Chat with AI to create and manage workflows
- AI remembers everything about your project
- Natural language commands

### ⚡ **Unlimited Workflows**
- Create as many workflows as you want
- Each workflow runs independently
- Easy pause/resume/delete

### 🔐 **Secure Credential Management**
- Enter API keys once in chat
- Stored encrypted in database
- Never shown in plain text again

### 📊 **Beautiful Dashboard**
- Modern, clean interface
- Real-time statistics
- Mobile responsive

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Setup

```bash
python setup.py
```

This will:
- ✅ Store your API keys securely
- ✅ Initialize database
- ✅ Create default workflow
- ✅ Test connections

### 3. Start the System

```bash
python app_enhanced.py
```

### 4. Open Your Browser

Go to: **http://localhost:5000**

---

## 💬 Using the Chat Interface

The chat interface is your main control center. Just talk to it naturally:

### Creating Workflows

```
You: "Create videos about puppies playing in the snow, 
      post 6 times a day to TikTok and Instagram"

AI: "Got it! Creating workflow 'puppy-snow-videos'...
     ✅ Configured for TikTok & Instagram
     ✅ Schedule: Every 4 hours
     ✅ Using Sora for video generation
     Should I start it now?"

You: "Yes!"

AI: "✅ Workflow started! First video generating now..."
```

### Managing Workflows

```
You: "Show me all my workflows"

AI: "You have 3 active workflows:
     1. 🐕 Puppy Videos (4x/day) - Running
     2. 🐱 Kitten Play (6x/day) - Running  
     3. 🐐 Baby Goats (3x/day) - Paused"

You: "Resume the baby goats one"

AI: "✅ Resumed 'Baby Goats' workflow"
```

### Modifying Settings

```
You: "Change puppy videos to only post on weekends"

AI: "✅ Updated schedule: Puppies now post only Sat-Sun"

You: "Add YouTube to the platforms"

AI: "✅ Added YouTube. Now posting to TikTok, Instagram, YouTube"
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────┐
│     Beautiful Web Interface          │
│  (Dashboard, Chat, Workflows)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   AI Assistant (OpenRouter)          │
│  - Understands commands              │
│  - Creates workflows                 │
│  - Remembers everything              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Workflow Manager                   │
│  - Stores unlimited workflows        │
│  - Executes on schedule              │
│  - Tracks performance                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   External APIs                      │
│  - Kie.ai (Sora videos)             │
│  - Blotato (Social posting)          │
│  - OpenRouter (AI)                   │
└─────────────────────────────────────┘
```

---

## 📁 File Structure

```
video-automation-system/
├── app_enhanced.py          # Main web application (NEW)
├── workflow_manager.py      # Unlimited workflow engine (NEW)
├── workflow_executor.py     # Dynamic execution system (NEW)
├── credential_manager.py    # Secure API key storage (NEW)
├── ai_client.py            # Enhanced AI chat (NEW)
├── setup.py                # One-click setup (NEW)
│
├── api_clients.py          # API wrappers
├── database.py             # SQLite database
├── ideas.py                # Video ideas bank
├── scheduler.py            # Scheduling system
│
├── requirements.txt        # Dependencies
└── README.md              # This file
```

---

## 🎯 Example Workflows You Can Create

### Video Creation Workflows
- Pet videos (puppies, kittens, baby animals)
- Cooking demonstrations
- Product reviews
- How-to tutorials
- Nature footage
- Art time-lapses

### Engagement Workflows (Coming Soon)
- Auto-reply to comments
- Welcome messages to new followers
- Like and comment on trending posts
- Send DMs to engaged users

### Analytics Workflows (Coming Soon)
- Track follower growth
- Monitor engagement rates
- Identify best posting times
- Generate performance reports

### Marketing Workflows (Coming Soon)
- Find trending content
- Repurpose videos across platforms
- Schedule promotional campaigns
- Track competitor activity

---

## 🔑 API Keys You Need

### Required

1. **Kie.ai** (Sora video generation)
   - Get it: https://kie.ai/api-key
   - Cost: ~$5-10 per video

2. **Blotato** (Social media posting)
   - Get it: https://blotato.com → Settings → API
   - Cost: Varies by plan

3. **OpenRouter** (AI chat & script generation)
   - Get it: https://openrouter.ai/
   - Cost: ~$0.001-0.01 per request
   - **Cheapest option!**

### Optional

4. **Anthropic Claude** (Alternative to OpenRouter)
   - Get it: https://console.anthropic.com/
   - Cost: ~$0.008 per request

---

## 💰 Cost Estimate

**Per Video:**
- Video generation (Sora): $5-10
- AI script: $0.001-0.01
- Social posting: Free (Blotato)
- **Total: ~$5-10 per video**

**Per Month (4 videos/day):**
- ~120 videos = $600-1,200/month
- Suitable for serious content creators

**Pro Tip:** Start with 1-2 videos/day to test, then scale up!

---

## 🚢 Deploying to Railway

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Video automation system"
git push
```

### 2. Connect to Railway

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repository

### 3. Add Environment Variables

In Railway dashboard, add:

```
KIE_API_KEY=your-key
BLOTATO_API_KEY=your-key
OPENROUTER_API_KEY=your-key
SECRET_KEY=random-secret-string
```

### 4. Deploy

Railway will automatically:
- Install dependencies
- Run setup
- Start the app
- Give you a URL

Access your dashboard at: `https://your-app.up.railway.app`

---

## 🔧 Advanced Features

### Custom Workflows

Create completely custom workflows:

```
You: "Create a workflow that scrapes trending hashtags,
      generates related video ideas, creates videos,
      and posts them with those hashtags"

AI: "I'll create a custom workflow with these steps:
     1. Scrape Twitter/Instagram for trending tags
     2. Generate 10 video ideas per tag
     3. Create videos with Sora
     4. Post with trending hashtags
     Should I proceed?"
```

### Workflow Chaining

Chain multiple workflows together:

```
You: "After creating a video, analyze its performance,
      and if engagement is high, create 3 similar videos"

AI: "Creating a chained workflow:
     Workflow A: Create video
     Workflow B: Analyze performance (triggered after A)
     Workflow C: Create similar videos (triggered if B shows high engagement)
     ✅ Set up!"
```

### Conditional Logic

Add conditions to workflows:

```
You: "Only post puppy videos when engagement rate is above 5%"

AI: "✅ Added condition: Puppy videos only post if 
     previous video had >5% engagement"
```

---

## 🐛 Troubleshooting

### "AI client not configured"
→ Run `python setup.py` again
→ Check if OpenRouter API key is correct

### "Workflow execution failed"
→ Check logs in dashboard
→ Ask AI in chat: "Why did the last workflow fail?"
→ AI will debug and suggest fixes

### Videos not posting
→ Verify Blotato account IDs in first workflow config
→ Check if accounts are connected in Blotato dashboard

### Can't access chat
→ Make sure setup.py ran successfully
→ Check if OpenRouter key has credits

---

## 🎓 Tips & Best Practices

### 1. Start Small
- Begin with 1-2 workflows
- Test thoroughly before scaling
- Monitor costs closely

### 2. Use the Chat
- Chat is your main interface
- Ask questions freely
- AI remembers everything

### 3. Monitor Performance
- Check dashboard daily
- Review video engagement
- Adjust based on results

### 4. Iterate Quickly
- Try different content types
- Test various posting times
- Let AI optimize for you

---

## 🔮 Coming Soon

### Phase 2: Social Growth Tools
- Auto-reply to comments
- Welcome new followers
- Engagement automation
- Growth analytics

### Phase 3: Advanced Marketing
- Trend hijacking
- Competitor analysis
- Cross-platform optimization
- Viral prediction

### Phase 4: Monetization
- Affiliate link integration
- Sponsor outreach
- Product campaigns
- Revenue tracking

---

## 📞 Support

### In-App Support
Use the chat interface:
```
You: "I need help with X"
AI: [Provides detailed help and solutions]
```

### Documentation
- Check DEPLOYMENT.md for deployment guides
- Check QUICKSTART.md for quick reference

### Community
- GitHub Issues for bugs
- Discussions for feature requests

---

## 📜 License

MIT License - Do whatever you want with this!

---

## 🙏 Credits

Built with:
- Flask (Web framework)
- OpenRouter (AI)
- Kie.ai (Sora videos)
- Blotato (Social posting)
- SQLite (Database)

---

**Made to save you from n8n headaches! 🎉**

Now go build something amazing! 🚀
