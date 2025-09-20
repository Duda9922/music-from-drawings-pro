# 🎨 → 🎵 Music from Drawings Pro

**A winning software track application that converts drawings into music using advanced AI**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)


### **Architecture**
- **FastAPI Backend**: High-performance async API with automatic OpenAPI documentation
- **React Frontend**: Modern, responsive UI with advanced drawing capabilities
- **MongoDB**: Scalable NoSQL database with Beanie ODM
- **Redis**: High-performance caching and session management
- **Docker**: Complete containerization for easy deployment

### **AI Integration**
- **Google Gemini API**: Advanced image analysis with structured JSON output
- **Multiple Music APIs**: Suno AI, Beatoven, ElevenLabs integration
- **Intelligent Mapping**: Visual features → Musical parameters
- **Real-time Processing**: Background tasks with progress tracking

### **Enterprise Features**
- **Analytics Dashboard**: User insights and usage statistics
- **Prometheus + Grafana**: Comprehensive monitoring and alerting
- **Rate Limiting**: API protection and fair usage
- **Authentication**: JWT-based user management
- **File Storage**: Secure image and audio file handling

### **Advanced Drawing Tools**
- **Multi-tool Canvas**: Pen, brush, marker, eraser with different styles
- **Real-time Preview**: Live analysis and music generation
- **Color Palette**: Advanced color picker with mood mapping
- **Touch Support**: Mobile-optimized drawing experience
- **Undo/Redo**: Full drawing history management

## 🏗Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React SPA     │    │   FastAPI       │    │   MongoDB       │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   Redis Cache   │    │   File Storage  │
│   (Proxy)       │    │   (Sessions)    │    │   (Images)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│   AI Services   │
│   (Gemini API)  │
└─────────────────┘
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for development)
- Python 3.11+ (for development)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd music-from-drawings-pro
cp .env.example .env
```

### 2. Configure Environment
Edit `.env` file with your API keys:
```env
# AI APIs
GEMINI_API_KEY=your_gemini_api_key_here
SUNO_API_KEY=your_suno_api_key_here
BEATOVEN_API_KEY=your_beatoven_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Database
MONGODB_URL=mongodb://admin:password123@localhost:27017/music_from_drawings?authSource=admin
REDIS_URL=redis://localhost:6379
```

### 3. Run with Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin123)
- **Prometheus**: http://localhost:9090

## Development Setup

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

## Key Features

### **Drawing Interface**
- **Multi-tool Support**: Pen, brush, marker, eraser with different styles
- **Color Psychology**: Smart color-to-mood mapping
- **Brush Dynamics**: Variable width and opacity
- **Touch Support**: Mobile-optimized drawing experience
- **Real-time Preview**: Live visual feedback

### **AI-Powered Analysis**
- **Visual Feature Extraction**: Colors, lines, composition, mood
- **Structured Output**: JSON format for reliable processing
- **Musical Mapping**: Visual elements → Musical parameters
- **Multiple Providers**: Fallback and redundancy

### **Music Generation**
- **Multiple APIs**: Suno AI, Beatoven, ElevenLabs
- **Real-time Generation**: Background processing with progress
- **Audio Player**: Built-in music player with controls
- **Download/Share**: Export generated music

### **Analytics & Monitoring**
- **User Analytics**: Drawing patterns, music preferences
- **Performance Metrics**: API response times, success rates
- **Real-time Monitoring**: Prometheus + Grafana dashboards
- **Error Tracking**: Comprehensive logging and alerting

## API Endpoints

### Drawings
- `POST /api/v1/drawings/upload` - Upload and analyze drawing
- `GET /api/v1/drawings/{id}` - Get drawing details
- `GET /api/v1/drawings/` - List drawings with filters

### Music
- `POST /api/v1/music/generate` - Generate music from drawing
- `GET /api/v1/music/{id}` - Get music generation details
- `GET /api/v1/music/providers/available` - List available providers

### Analytics
- `GET /api/v1/analytics/stats` - Get usage statistics
- `GET /api/v1/analytics/trends` - Get usage trends

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Deployment

### Production Deployment
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale backend=3
```

### Environment Variables
- `MONGODB_URL`: MongoDB connection string
- `REDIS_URL`: Redis connection string
- `GEMINI_API_KEY`: Google Gemini API key
- `SUNO_API_KEY`: Suno AI API key
- `BEATOVEN_API_KEY`: Beatoven API key
- `ELEVENLABS_API_KEY`: ElevenLabs API key

## Why This Wins

### **Technical Excellence**
- ✅ Modern, scalable architecture
- ✅ High-performance async processing
- ✅ Comprehensive error handling
- ✅ Production-ready monitoring
- ✅ Security best practices

### **Innovation**
- ✅ Advanced AI integration
- ✅ Real-time music generation
- ✅ Intelligent visual analysis
- ✅ Multi-provider redundancy
- ✅ Mobile-optimized interface

### **User Experience**
- ✅ Intuitive drawing interface
- ✅ Real-time feedback
- ✅ Seamless music generation
- ✅ Social sharing features
- ✅ Analytics dashboard

### **Business Value**
- ✅ Scalable to millions of users
- ✅ Multiple revenue streams
- ✅ Comprehensive analytics
- ✅ Easy deployment and maintenance
- ✅ Extensible architecture

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini API for advanced image analysis
- Suno AI, Beatoven, ElevenLabs for music generation
- FastAPI, React, MongoDB communities
- All contributors and testers

---

**Built with ❤️ for the Software Track Competition**
