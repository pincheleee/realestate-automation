# Real Estate Automation System

A powerful automation system for real estate agents that combines property management, lead tracking, and AI-powered features to streamline your real estate business.

## Features

### Core Automation
- Property listing management
- Lead tracking and management
- Automated appointment scheduling
- Facebook Marketplace integration
- Calendly integration for showings

### AI-Powered Features
- GPT-enhanced property descriptions
- Smart lead matching
- Personalized communication generation
- Property-lead compatibility analysis
- Automated follow-up messages

### Dashboard
- Real-time statistics and metrics
- Property management interface
- Lead tracking system
- Appointment scheduling
- Activity monitoring

## Tech Stack

### Backend
- FastAPI (Python web framework)
- OpenAI GPT-4 for AI features
- Facebook SDK for Marketplace integration
- Calendly API for scheduling
- Pydantic for data validation

### Frontend
- React.js
- Tailwind CSS for styling
- Headless UI components
- Hero Icons
- Axios for API communication

## Prerequisites

- Python 3.8+
- Node.js 14+
- OpenAI API key
- Facebook Developer account
- Calendly account
- MLS access (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd real-estate-automation
```

2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
```

5. Create a `.env` file in the root directory with your API keys:
```env
# Facebook API credentials
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret

# Calendly API credentials
CALENDLY_API_KEY=your_calendly_api_key

# MLS API credentials
MLS_API_KEY=your_mls_api_key

# FollowUpBoss API credentials
FOLLOWUPBOSS_API_KEY=your_followupboss_api_key

# OpenAI API credentials
OPENAI_API_KEY=your_openai_api_key

# Application settings
DEBUG=True
LOG_LEVEL=INFO
```

## Running the Application

1. Start the backend server:
```bash
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Access the dashboard:
- Open your browser to `http://localhost:3000`
- The dashboard will load automatically

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when the backend server is running.

### Key Endpoints

- `POST /api/properties` - Add a new property
- `POST /api/leads` - Add a new lead
- `POST /api/appointments` - Schedule a property showing
- `GET /api/dashboard/stats` - Get dashboard statistics

### API Usage Examples

#### Adding a New Property
```bash
curl -X POST "http://localhost:8000/api/properties" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Beautiful 3 Bedroom Home",
       "description": "Modern home with updated features",
       "price": 350000,
       "location": "San Francisco, CA",
       "bedrooms": 3,
       "bathrooms": 2,
       "square_feet": 1500
     }'
```

#### Adding a New Lead
```bash
curl -X POST "http://localhost:8000/api/leads" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "phone": "555-0123",
       "preferences": {
         "location": "San Francisco",
         "price_range": "300000-400000",
         "features": "3 bedrooms, modern kitchen"
       },
       "schedule_consultation": true
     }'
```

#### Scheduling an Appointment
```bash
curl -X POST "http://localhost:8000/api/appointments" \
     -H "Content-Type: application/json" \
     -d '{
       "lead_id": "123",
       "property_id": "456",
       "scheduled_time": "2024-03-20T14:00:00Z",
       "property_address": "123 Main St, San Francisco, CA"
     }'
```

#### Getting Dashboard Statistics
```bash
curl "http://localhost:8000/api/dashboard/stats"
```

## Dashboard Screenshots

### Main Dashboard
![Main Dashboard](docs/images/dashboard-main.png)
*Overview of key metrics and recent activities*

### Property Management
![Property Management](docs/images/property-management.png)
*Interface for managing property listings*

### Lead Management
![Lead Management](docs/images/lead-management.png)
*Lead tracking and management interface*

### Appointment Scheduling
![Appointment Scheduling](docs/images/appointment-scheduling.png)
*Calendar and scheduling interface*

## Troubleshooting Guide

### Common Issues and Solutions

#### Backend Issues

1. **Server Not Starting**
   - Check if port 8000 is available
   - Verify all dependencies are installed
   - Check the logs for error messages
   ```bash
   # Check if port is in use
   lsof -i :8000
   
   # View detailed logs
   uvicorn main:app --reload --log-level debug
   ```

2. **API Connection Errors**
   - Verify all API keys in `.env` file
   - Check internet connection
   - Ensure CORS settings are correct
   ```python
   # In main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Database Connection Issues**
   - Check database credentials
   - Verify database service is running
   - Check network connectivity

#### Frontend Issues

1. **Dashboard Not Loading**
   - Clear browser cache
   - Check browser console for errors
   - Verify backend server is running
   ```bash
   # Check backend health
   curl http://localhost:8000/health
   ```

2. **Forms Not Submitting**
   - Check network tab in browser dev tools
   - Verify API endpoints are correct
   - Check for validation errors

3. **Real-time Updates Not Working**
   - Check WebSocket connection
   - Verify event listeners are properly set up
   - Check browser console for errors

### Performance Optimization

1. **Slow API Responses**
   - Enable caching where appropriate
   - Optimize database queries
   - Use pagination for large datasets

2. **High Memory Usage**
   - Monitor server resources
   - Implement proper cleanup
   - Use connection pooling

3. **Frontend Performance**
   - Implement lazy loading
   - Use proper caching strategies
   - Optimize bundle size

## Features in Detail

### Property Management
- Add and manage property listings
- Automatic Facebook Marketplace posting
- GPT-enhanced property descriptions
- Property-lead matching

### Lead Management
- Track and manage leads
- Automated lead scoring
- Personalized communication
- Lead status tracking

### Appointment Scheduling
- Integration with Calendly
- Automated showing scheduling
- Confirmation emails
- Calendar management

### AI Features
- GPT-powered property descriptions
- Smart lead matching algorithm
- Personalized communication generation
- Property-lead compatibility analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- OpenAI for GPT integration
- Facebook for Marketplace API
- Calendly for scheduling API
- FastAPI team for the web framework
- React and Tailwind CSS communities 