# KeralaBank - Vercel Deployment

## Project Structure

```
keralabank_vercel/
|
|-- api/
|   |-- __init__.py
|   |-- main.py          # FastAPI application
|   |-- database.py      # Database configuration
|   |-- models.py        # Data models
|   |-- crud.py          # CRUD operations
|
|-- vercel.json          # Vercel configuration
|-- requirements.txt     # Python dependencies
|-- README.md            # This file
|-- .gitignore           # Git ignore file
```

## Features

### FastAPI Backend
- **Authentication**: Employee login system
- **SMA Data**: Collection tracking and management
- **Loan Actions**: Complete loan management system
- **Messages**: Employee communication
- **Reports**: Error reporting and resolution
- **Documents**: File upload and sharing
- **Circulars**: Official circulars distribution
- **Consolidation**: Links to consolidation sheets
- **Finacle Help**: Banking system help
- **Urgent Messages**: Critical alerts

### Database
- **SQLite**: Lightweight database for Vercel
- **Auto-migration**: Database schema automatically created
- **Data Persistence**: Data stored in Vercel's tmp directory

### API Endpoints

#### Authentication
- `GET /login` - Employee login
- `POST /update-profile` - Update employee profile
- `POST /update-password` - Change password
- `POST /upload-avatar` - Upload profile picture

#### SMA Data
- `GET /sma-data/{branch_code}` - Get branch SMA data
- `GET /collections/{branch_code}/{category}` - Get collection data
- `POST /save-collection` - Save daily collection

#### Loan Actions
- `GET /loan-actions/{loan_number}` - Get loan details
- `POST /loan-actions` - Create new loan
- `PUT /loan-actions/{loan_number}` - Update loan
- `DELETE /loan-actions/{loan_number}` - Delete loan

#### Messages
- `GET /messages` - Get all messages
- `POST /messages` - Send message

#### Reports
- `GET /reports/{user_id}` - Get user reports
- `GET /reports/all` - Get all reports
- `POST /reports` - Create report
- `POST /reports/{report_id}/resolve` - Resolve report

#### Documents
- `POST /upload-doc` - Upload document

#### Circulars
- `GET /circulars` - Get circulars
- `POST /upload-circular` - Upload circular

#### Other Features
- `GET /branches` - Get all branches
- `GET /employees/{branch_id}` - Get branch staff
- `GET /consolidation-links` - Get consolidation links
- `POST /consolidation-links` - Create consolidation link
- `GET /finacle-help` - Get finacle help
- `POST /finacle-help` - Create finacle help
- `GET /urgent` - Get urgent messages
- `POST /urgent` - Create urgent message
- `POST /urgent/seen` - Mark urgent as seen

## Deployment

### Prerequisites
- GitHub account
- Vercel account (free)

### Steps

#### 1. Create GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/keralabank_vercel.git
git push -u origin main
```

#### 2. Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project"
4. Import your repository
5. Click "Deploy"

#### 3. Update Mobile App
```python
# In mobile app, change API URLs to:
"https://your-app-name.vercel.app"
```

## Mobile App Integration

### API URL Configuration
Update your mobile app to use the Vercel URL:

```python
# Change all instances of:
"http://34.160.111.145:8000"
# To:
"https://keralabank.vercel.app"
```

### Build New APK
```cmd
cd "C:\Users\admin\Desktop\athul rosh\APP"
python -m buildozer android debug
```

## Benefits of Vercel

### Performance
- **Global CDN**: Fast responses worldwide
- **Edge Computing**: Process requests near users
- **Auto-scaling**: Handle traffic spikes automatically

### Cost
- **Free Tier**: 100,000 function calls/month
- **No Credit Card**: Required for free tier
- **Transparent Pricing**: Clear upgrade path

### Features
- **Custom Domain**: `keralabank.vercel.app`
- **Free SSL**: HTTPS automatically
- **Git Integration**: Auto-deploy on push
- **Analytics**: Built-in monitoring
- **Environment Variables**: Secure configuration

## Database Considerations

### SQLite on Vercel
- **Location**: `/tmp/bank.db`
- **Persistence**: Data survives deployments
- **Backup**: Regular backups recommended

### Alternative: PostgreSQL
For production, consider Vercel Postgres:
1. Go to Vercel dashboard
2. Click "Storage" > "Create Database"
3. Add `DATABASE_URL` environment variable

## Environment Variables

### Required Variables
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)
- `SECRET_KEY`: JWT secret key (optional, defaults to secure key)

### How to Set
1. Go to Vercel dashboard
2. Click "Settings" > "Environment Variables"
3. Add your variables

## Monitoring

### Vercel Analytics
- **Function Logs**: Real-time error tracking
- **Performance**: Response time monitoring
- **Usage**: Function call statistics

### Health Check
```bash
curl https://keralabank.vercel.app/health
```

## Troubleshooting

### Common Issues

#### 1. Cold Start Delays
**Problem**: First request is slow
**Solution**: Add warming endpoint
```python
@app.get("/warm")
def warm_up():
    return {"status": "warm"}
```

#### 2. Database Connection Issues
**Problem**: Database not found
**Solution**: Check tmp directory permissions

#### 3. CORS Issues
**Problem**: Mobile app cannot connect
**Solution**: Verify CORS configuration

#### 4. Function Timeout
**Problem**: Requests timeout after 30 seconds
**Solution**: Optimize database queries

### Debugging Tips

#### Check Logs
1. Go to Vercel dashboard
2. Click "Functions" tab
3. View function logs

#### Local Testing
```bash
# Install Vercel CLI
npm i -g vercel

# Test locally
vercel dev
```

## Security

### Best Practices
- **HTTPS**: All connections encrypted
- **CORS**: Properly configured for mobile app
- **Environment Variables**: Sensitive data secured
- **Input Validation**: All inputs validated
- **Error Handling**: Proper error responses

### Recommendations
- Update dependencies regularly
- Use strong passwords
- Monitor function logs
- Implement rate limiting

## Scaling

### Free Tier Limits
- **Function Calls**: 100,000/month
- **Bandwidth**: 100GB/month
- **Build Time**: 100 hours/month
- **Storage**: 100GB

### When to Upgrade
- More than 100,000 API calls/month
- More than 100GB bandwidth/month
- Need longer function timeouts
- Want dedicated resources

## Support

### Documentation
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)

### Community
- [Vercel Discord](https://vercel.com/discord)
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
- [Stack Overflow](https://stackoverflow.com)

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**KeralaBank on Vercel - Professional banking application with world-class performance!**
