# Ping Pong Web Game

A real-time multiplayer ping pong game built with Django, WebSockets, and vanilla JavaScript. This project features online matchmaking, tournaments, user authentication with 2FA, and comprehensive game statistics tracking.

## Features

### 🎮 Game Modes
- **1v1 Matches**: Real-time ping pong matches between two players
- **Tournament Mode**: Multi-player tournaments with bracket system
- **Spectator Mode**: Watch ongoing matches in real-time

### 👥 Social Features
- **Friend System**: Add friends, view online status, and challenge them directly
- **User Profiles**: Detailed statistics, match history, and performance tracking
- **Leaderboards**: Rankings based on wins, losses, and performance metrics

### 🔐 Authentication & Security
- **OAuth2 Integration**: Login with external providers
- **Two-Factor Authentication (2FA)**: Enhanced security with TOTP support
- **JWT Token Management**: Secure session handling
- **Multi-factor Authentication**: QR code generation for authenticator apps

### 📊 Game Analytics
- **Match History**: Complete record of all played games
- **Performance Metrics**: Win rates, average rally length, score tracking
- **Statistical Analysis**: Charts and graphs showing player progression
- **Tournament Results**: Bracket visualization and results tracking

### 🌐 Real-time Features
- **WebSocket Integration**: Real-time game updates and communication
- **Live Matchmaking**: Automatic player matching system
- **Online Status**: Real-time friend online/offline status
- **Live Game Updates**: Ball position, scores, and game state synchronization

## Technology Stack

### Backend
- **Django 5.1.2**: Web framework and API
- **Django REST Framework**: RESTful API development
- **Django Channels**: WebSocket support for real-time features
- **PostgreSQL**: Primary database
- **Socket.IO**: Real-time bidirectional communication
- **JWT Authentication**: Secure token-based authentication
- **Docker**: Containerization and deployment

### Frontend
- **Vanilla JavaScript**: Pure JS implementation without frameworks
- **CSS Modules**: Modular styling approach
- **WebSocket Client**: Real-time communication with backend
- **Responsive Design**: Mobile and desktop compatibility

### DevOps & Deployment
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and static file serving
- **SSL/TLS**: HTTPS security implementation
- **Environment Configuration**: Separate development and production settings

## Project Structure

```
pingpong/
├── backend/                 # Django backend application
│   ├── api/                # Main API endpoints
│   ├── users/              # User authentication and management
│   │   ├── accounts/       # User accounts and OAuth2
│   │   ├── friends/        # Friend system implementation
│   │   └── status/         # Online status tracking
│   ├── ingame/             # Game logic and mechanics
│   ├── matchmaking/        # Player matching system
│   ├── tournament/         # Tournament management
│   └── pingpong_history/   # Game history and statistics
├── frontend/               # Vanilla JavaScript frontend
│   ├── src/
│   │   ├── Components/     # Reusable UI components
│   │   ├── Pages/          # Application pages
│   │   ├── Controller/     # API communication logic
│   │   └── Utils/          # Utility functions
│   └── css/                # Styling and CSS modules
└── docker-compose.yml      # Container orchestration
```

## Quick Start

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pingpong
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   # Serve static files (development server needed)
   ```

### Docker Development

1. **Start all services**
   ```bash
   docker-compose -f docker-compose.develop.yml up --build
   ```

2. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - Admin Panel: `http://localhost:8000/admin`

### Production Deployment

1. **Build and deploy**
   ```bash
   docker-compose up -d --build
   ```

2. **Configure SSL certificates**
   - Place your SSL certificates as `cert.crt` and `cert.key`
   - Nginx is configured for HTTPS

## API Documentation

The project includes comprehensive API documentation:
- **Swagger UI**: Available at `/api/schema/swagger-ui/`
- **ReDoc**: Available at `/api/schema/redoc/`
- **OpenAPI Schema**: Available at `/api/schema/`

## Game Mechanics

### Real-time Ping Pong
- Physics-based ball movement and collision detection
- Paddle controls with mouse or keyboard input
- Power-ups and special ball effects
- Adjustable game settings (ball speed, paddle size, etc.)

### Matchmaking System
- Skill-based player matching
- Queue management for fair matches
- Tournament bracket generation
- Spectator room management

### Scoring System
- Traditional ping pong scoring rules
- Rally counting and statistics
- Performance metrics calculation
- Ranking system based on ELO-like algorithm

## Testing

### Backend Testing
```bash
cd backend
pytest
```

### Running Specific Tests
```bash
# Authentication tests
pytest users/accounts/two_factor_auth/tests/

# Game logic tests
pytest ingame/tests.py

# Tournament tests
pytest tournament/tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Environment Variables

Create a `.env` file in the backend directory:

```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/pingpong
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built as part of a web development learning project
- Inspired by classic ping pong arcade games
- Uses modern web technologies for real-time gaming experience
