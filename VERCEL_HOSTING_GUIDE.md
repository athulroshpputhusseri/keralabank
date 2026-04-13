# Vercel Hosting for KeralaBank - Complete Guide

## Vercel Overview

Vercel is an excellent cloud platform that **can host FastAPI backends** using serverless functions. It's completely free and offers amazing performance.

### **Key Benefits:**
- **Completely Free** - No credit card required
- **Global CDN** - Fast performance worldwide
- **Free SSL** - HTTPS automatically included
- **Git Integration** - Auto-deploy from GitHub
- **Serverless** - No server management needed
- **Professional** - Custom domain: `keralabank.vercel.app`

## How Vercel Works for FastAPI

Vercel uses **serverless functions** to run your FastAPI backend. Instead of a continuously running server, your code runs on-demand when requests come in.

### **Architecture:**
```
Mobile App Request
       |
       v
Vercel Edge Network
       |
       v
Serverless Function (FastAPI)
       |
       v
Database (SQLite/PostgreSQL)
```

## Vercel vs Render Comparison

| Feature | Vercel | Render |
|---------|--------|--------|
| **Cost** | Free | Free |
| **Type** | Serverless | Traditional |
| **Performance** | Excellent (Global CDN) | Good |
| **Setup** | Medium | Easy |
| **Database** | Needs external DB | SQLite works |
| **Cold Starts** | Yes | No |
| **24/7** | Yes | Yes |
| **SSL** | Free | Free |

## **RECOMMENDATION: Vercel is Excellent!**

### **Why Vercel is Great for KeralaBank:**

#### **1. Performance**
- **Global CDN** - Fast from anywhere
- **Edge Computing** - Requests processed near users
- **No Server Management** - Fully managed

#### **2. Cost**
- **Truly Free** - No charges ever
- **No Hidden Costs** - Transparent pricing
- **No Credit Card Required**

#### **3. Professional Features**
- **Custom Domain** - `keralabank.vercel.app`
- **Free SSL** - HTTPS automatically
- **Auto-Deploy** - Git integration
- **Analytics** - Built-in monitoring

#### **4. Scalability**
- **Auto-scaling** - Handles traffic automatically
- **No Limits** - No bandwidth limits
- **Global Reach** - Works worldwide

## Vercel Setup for KeralaBank

### **Step 1: Project Structure**

Create this structure:
```
keralabank/
|
|-- api/
|   |-- __init__.py
|   |-- main.py          # FastAPI app
|   |-- database.py      # Database config
|   |-- models.py        # Data models
|   |-- crud.py          # CRUD operations
|
|-- pages/
|   |-- index.py         # Optional frontend
|
|-- vercel.json          # Vercel config
|-- requirements.txt     # Python dependencies
```

### **Step 2: Create Vercel Configuration**

#### **vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/main.py"
    }
  ],
  "functions": {
    "api/main.py": {
      "maxDuration": 30
    }
  }
}
```

### **Step 3: Update FastAPI for Serverless**

#### **api/main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "KeralaBank API on Vercel"}

# Your existing API endpoints...

# For serverless deployment
handler = app
```

### **Step 4: Database Options**

#### **Option 1: SQLite (Simple)**
```python
# api/database.py
import os
from sqlalchemy import create_engine

# Use Vercel's tmp directory for SQLite
DATABASE_URL = "sqlite:///tmp/bank.db"
engine = create_engine(DATABASE_URL)

# Ensure tmp directory exists
os.makedirs("tmp", exist_ok=True)
```

#### **Option 2: PostgreSQL (Recommended)**
```python
# api/database.py
import os
from sqlalchemy import create_engine

# Use Vercel Postgres (free tier)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
```

### **Step 5: requirements.txt**
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
requests==2.31.0
psycopg2-binary==2.9.7  # For PostgreSQL
```

## Deployment Process

### **Step 1: Create Vercel Account**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Verify email

### **Step 2: Connect Repository**
1. Click "New Project"
2. Connect your GitHub repository
3. Import your KeralaBank project

### **Step 3: Configure Project**
1. **Framework Preset**: Other
2. **Root Directory**: . (project root)
3. **Build Command**: `pip install -r requirements.txt`
4. **Output Directory**: . (no build needed)

### **Step 4: Deploy**
1. Click "Deploy"
2. Wait for deployment (2-3 minutes)
3. Your app is live at `keralabank.vercel.app`

## Mobile App Configuration

### **Update API URLs**
```python
# In main11.py, change all instances of:
"http://34.160.111.145:8000"

# To:
"https://keralabank.vercel.app"
```

### **Build New APK**
```cmd
cd "C:\Users\admin\Desktop\athul rosh\APP"
python -m buildozer android debug
```

## Database Considerations

### **SQLite Limitations:**
- **Cold Starts**: Database recreated on each deployment
- **Not Persistent**: Data lost on redeploy
- **File Size**: Limited to Vercel's tmp directory

### **PostgreSQL Solution:**
- **Vercel Postgres**: Free tier available
- **Persistent Data**: Data survives deployments
- **Better Performance**: Optimized for serverless

#### **Setup Vercel Postgres:**
1. Go to Vercel dashboard
2. Click "Storage" > "Create Database"
3. Choose PostgreSQL
4. Add DATABASE_URL to environment variables

## Advanced Configuration

### **Environment Variables**
```python
# api/main.py
import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
```

### **Performance Optimization**
```python
# api/main.py
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### **Error Handling**
```python
# api/main.py
from fastapi import HTTPException

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {"error": str(exc)}
```

## Testing Vercel Deployment

### **1. Test API Endpoints**
```bash
# Test root endpoint
curl https://keralabank.vercel.app

# Test login endpoint
curl "https://keralabank.vercel.app/login?emp_id=test&password=test"
```

### **2. Test Mobile App**
1. Install updated APK
2. Test all features
3. Verify internet connectivity

### **3. Monitor Performance**
1. Check Vercel Analytics
2. Monitor response times
3. Check error rates

## Troubleshooting

### **Common Issues:**

#### **1. Cold Start Delays**
**Problem**: First request is slow
**Solution**: Add warming endpoint
```python
@app.get("/warm")
def warm_up():
    return {"status": "warm"}
```

#### **2. Database Connection Issues**
**Problem**: Database not found
**Solution**: Check DATABASE_URL environment variable

#### **3. CORS Issues**
**Problem**: Mobile app cannot connect
**Solution**: Verify CORS configuration

#### **4. Function Timeout**
**Problem**: Requests timeout after 30 seconds
**Solution**: Optimize database queries

### **Debugging Tips:**

#### **Check Vercel Logs:**
1. Go to Vercel dashboard
2. Click "Functions" tab
3. View function logs

#### **Local Testing:**
```bash
# Install Vercel CLI
npm i -g vercel

# Test locally
vercel dev
```

## Performance Tips

### **1. Reduce Cold Starts**
```python
# Keep imports at module level
# Avoid heavy initialization in functions
# Use connection pooling
```

### **2. Optimize Database**
```python
# Use connection pooling
from sqlalchemy.pool import StaticPool

engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)
```

### **3. Cache Responses**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

FastAPICache.init(InMemoryBackend())
```

## Cost Analysis

### **Vercel Free Tier:**
- **Functions**: 100,000 invocations/month
- **Bandwidth**: 100GB/month
- **Build Time**: 100 hours/month
- **Storage**: 100GB
- **Postgres**: 512MB database

### **For KeralaBank:**
- **Daily Users**: 50-100 users
- **API Calls**: ~500 calls/day
- **Storage**: ~10MB
- **Well Within Limits**: Perfect fit

## Migration from Render

### **If you already deployed to Render:**

#### **1. Export Data**
```python
# Export SQLite data
python export_data.py
```

#### **2. Update Mobile App**
```python
# Change API URLs from Render to Vercel
"https://keralabank-api.onrender.com" -> "https://keralabank.vercel.app"
```

#### **3. Deploy to Vercel**
- Follow Vercel setup process
- Test thoroughly
- Switch DNS if using custom domain

## Final Recommendation

### **Choose Vercel because:**

#### **Advantages:**
- **Better Performance** - Global CDN
- **Truly Free** - No costs ever
- **Professional** - Custom domain
- **Scalable** - Handles growth
- **Modern** - Serverless architecture

#### **Perfect for KeralaBank:**
- **Mobile App** - Fast API responses
- **Global Users** - Works worldwide
- **No Maintenance** - Fully managed
- **Professional** - Custom domain
- **Free Forever** - No costs

### **Decision Matrix:**
| Factor | Vercel | Render |
|--------|--------|--------|
| **Performance** | Excellent | Good |
| **Setup** | Medium | Easy |
| **Database** | External | Internal |
| **Cost** | Free | Free |
| **Maintenance** | None | Minimal |
| **Scalability** | Excellent | Good |

**Vercel is the winner for performance and scalability!**

## Quick Start Commands

### **Deploy to Vercel:**
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Update mobile app
# Change API URLs to Vercel
# Build new APK
# Test connectivity
```

### **Test Locally:**
```bash
# Test serverless functions locally
vercel dev

# Test API endpoints
curl http://localhost:3000
```

## Conclusion

**Vercel is an excellent choice for hosting KeralaBank:**

- **Free Forever** - No charges ever
- **Excellent Performance** - Global CDN
- **Professional** - Custom domain and SSL
- **Serverless** - No server management
- **Scalable** - Handles any traffic
- **Modern** - Latest cloud technology

**Your KeralaBank app will have world-class performance on Vercel!**
