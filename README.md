# Real Estate Automation System

A comprehensive real estate automation system built with FastAPI, React, and Docker. This system automates various real estate tasks including lead management, property tracking, and appointment scheduling.

## 🚀 Features

- **Lead Management**
  - Automated lead capture from Facebook Marketplace
  - Lead scoring and prioritization
  - Follow-up automation
  - Lead tracking dashboard

- **Property Management**
  - Property listing automation
  - MLS integration
  - Property tracking and updates
  - Automated property matching

- **Appointment Scheduling**
  - Calendly integration
  - Automated scheduling
  - Calendar management
  - Follow-up reminders

- **AI Integration**
  - GPT-powered lead responses
  - Automated property descriptions
  - Smart lead qualification
  - Natural language processing

## 🛠️ Tech Stack

- **Backend**
  - FastAPI
  - PostgreSQL
  - Redis
  - SQLAlchemy
  - Alembic

- **Frontend**
  - React
  - Material-UI
  - Redux
  - Axios

- **Infrastructure**
  - Docker
  - Docker Compose
  - Nginx
  - GitHub Actions

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 16+
- Git

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/pincheleee/realestate-automation.git
   cd realestate-automation
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the development environment**
   ```bash
   ./scripts/docker.sh start
   ```

4. **Access the application**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## 🏗️ Development

### Backend Development
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

```bash
# Run backend tests
pytest

# Run frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Production Deployment
```bash
# Build and start production environment
./scripts/docker.sh prod-up

# Stop production environment
./scripts/docker.sh prod-down
```

## 🔒 Security

- JWT authentication
- Rate limiting
- CORS protection
- Input validation
- SQL injection prevention
- XSS protection

## 📝 API Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Robert Monterroso - Initial work

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- React team for the frontend library
- All contributors and maintainers 