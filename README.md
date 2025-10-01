# Daily Wellness Tracker

[![CI](https://github.com/omarnunezsiri/wellness/actions/workflows/ci.yml/badge.svg)](https://github.com/omarnunezsiri/wellness/actions/workflows/ci.yml)

A mindful productivity app that combines daily task planning with positive affirmations, featuring a cozy autumn aesthetic. Built with FastAPI, React, and designed to promote both productivity and mental wellness.

## ✨ Features

- **Daily Affirmations**: Beautiful, randomly-selected motivational messages to start your day
- **Task Management**: Create, complete, and organize daily tasks with intuitive interface
- **Device Sync**: Seamlessly sync tasks across multiple devices using secure OTP codes
- **AI Celebrations**: Personalized celebration messages powered by Google Gemini AI
- **Autumn Theme**: Warm, cozy design with glassmorphism effects and falling leaves animation
- **Progress Tracking**: Visual progress circles and completion statistics
- **Date Navigation**: Browse tasks from any day with elegant date controls

## 🚀 Quick Start

### Option 1: Local Development

#### Prerequisites
- Python 3.12+
- Node.js 20+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

#### 1. Clone and Setup
```bash
git clone https://github.com/omarnunezsiri/wellness.git
cd wellness
```

#### 2. Environment Configuration
Create environment files from examples:
```bash
# Backend environment
cp .env.example .env

# Frontend environment
cp frontend/.env.example frontend/.env
```

Edit `.env` with your configuration:
```env
# Database
DATABASE_URL=sqlite:///./affirmations.db

# Server
HOST=127.0.0.1
PORT=8000
DEBUG=True

# CORS (JSON array or comma-separated)
CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]

# Security (CHANGE THESE!)
SECRET_KEY=your-secret-key-change-in-production
GEMINI_API_KEY=your-google-gemini-api-key

# Default user
DEFAULT_USER_ID=default_user
```

#### 3. Backend Setup
```bash
# Install Python dependencies
uv sync

# Run database migrations (automatic on first run)
# Run the backend server
uv run python -m backend.main
```
Backend will be available at `http://127.0.0.1:8000`

#### 4. Frontend Setup
```bash
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```
Frontend will be available at `http://localhost:5173`

### Option 2: Docker Development

#### Prerequisites
- Docker and Docker Compose

#### 1. Environment Setup
```bash
# Copy environment files
cp .env.example .env
cp frontend/.env.example frontend/.env

# Edit .env with your configuration (same as above)
```

#### 2. Build and Run
```bash
# Build Docker images
docker build -t wellness-backend:dev -f backend/Dockerfile .
docker build -t wellness-frontend:dev -f frontend/Dockerfile ./frontend

# Start services
docker compose up

# Stop services
docker compose down
```

Services will be available at:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

### Option 3: Production with Nginx + Tailscale

For remote access and production deployment:

#### 1. Nginx Reverse Proxy
Install [Nginx](https://nginx.org/) system-wide using your package manager. The included `nginx.conf` provides:
- Rate limiting on AI celebration endpoint
- Proxy configuration for both frontend and backend
- Security headers
- Gzip compression

Use the provided `nginx.conf` file with your system-wide Nginx installation.

#### 2. Tailscale Integration
For secure remote access:

```bash
# Install Tailscale on your server
curl -fsSL https://tailscale.com/install.sh | sh

# Connect to your Tailscale network
sudo tailscale up

# Get your Tailscale IP
tailscale ip -4
```

Update your environment files:
```env
# Frontend .env
TAILSCALE_HOST=your-tailscale-hostname
```

#### 3. Expose with Tailscale
To make your app accessible via Tailscale:

**Option A: Private access (Tailscale network only)**
```bash
# Start Nginx (serving on port 3000)
mkdir temp logs
sudo nginx -c nginx.conf -p .

# Expose port 3000 within Tailscale network in background
tailscale serve --bg 3000
```

**Option B: Public access (internet via HTTPS)**
```bash
# Start Nginx (serving on port 3000)
mkdir temp logs
sudo nginx -c nginx.conf -p .

# Expose port 3000 to public internet via Tailscale Funnel
tailscale funnel --bg 3000
```

Your app will be accessible at:
```
https://<hostname>-<tailnet>.ts.net
```

## 🧪 Testing

### Run Tests Locally
```bash
# All tests with coverage
uv run python run_tests.py --coverage

# Unit tests only
uv run python run_tests.py unit

# Integration tests only
uv run python run_tests.py integration

# Or use pytest directly
uv run python -m pytest tests/ -v
```

### Test Coverage
Coverage reports are generated in `htmlcov/` directory. Open `htmlcov/index.html` in your browser to view detailed coverage information.

### Linting
```bash
# Check code formatting
uv run ruff check .
uv run ruff format --check .

# Auto-fix issues
uv run ruff check . --fix
uv run ruff format .
```

## 📋 API Documentation

Once the backend is running, visit `http://127.0.0.1:8000/docs` for interactive API documentation (Swagger UI).

### Key Endpoints

- **Affirmations**
  - `GET /api/affirmations` - Get random affirmation

- **Tasks**
  - `GET /api/daily-data?date=YYYY-MM-DD&user_id=uuid` - Get daily data
  - `POST /api/tasks` - Create new task
  - `PUT /api/tasks/{id}` - Update task completion
  - `DELETE /api/tasks/{id}` - Delete task

- **Sync**
  - `POST /api/sync/generate-code` - Generate sync code
  - `POST /api/sync/validate-code` - Validate sync code

- **AI Features**
  - `POST /api/celebrate-task` - Get AI celebration message

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./affirmations.db` |
| `HOST` | Server host address | `127.0.0.1` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Enable debug mode | `True` |
| `CORS_ORIGINS` | Allowed frontend origins | `["http://localhost:5173"]` |
| `SECRET_KEY` | Application secret key | `your-secret-key` |
| `GEMINI_API_KEY` | Google Gemini API key | `your-api-key` |
| `DEFAULT_USER_ID` | Default user identifier | `default_user` |

### Frontend Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000` |
| `TAILSCALE_HOST` | Tailscale hostname | `your-hostname` |

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **Pydantic**: Data validation
- **APScheduler**: Background task scheduling
- **Google Gemini**: AI-powered celebrations

### Frontend Stack
- **React**: UI framework
- **Vite**: Build tool and dev server
- **Modern CSS**: Custom properties, animations
- **Glassmorphism**: Translucent UI design

### Key Features
- **Device Sync**: SHA256-based OTP system with 15-minute expiry
- **Background Cleanup**: Automatic OTP cleanup every minute
- **AI Integration**: Contextual task celebration messages
- **Responsive Design**: Desktop and Tablet design
- **Accessibility**: Semantic HTML and keyboard navigation

## 🎨 Design System

### Color Palette
- **Warm Cream**: `#FFF8E7` - Background tones
- **Soft Orange**: `#E8A87C` - Primary accent
- **Deep Rust**: `#C38D5A` - Secondary accent
- **Coffee Brown**: `#8B5E3C` - Text and borders
- **Golden Yellow**: `#DAB370` - Highlights

### Typography
- **Headings**: Crimson Text (serif)
- **Body**: Lora (serif)
- **Monospace**: Courier New (for sync codes)

### Animations
- Falling leaves background animation
- Gentle hover transitions
- Celebration modal effects
- Progress circle updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `uv run python run_tests.py`
5. Commit changes: `git commit -m "Add feature"`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

### Code Style
- Python: Follow PEP 8, use ruff for formatting
- JavaScript: Use ESLint and Prettier
- CSS: Use custom properties for theming
- Commits: Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Codédex September 2025 Challenge**: Inspiration for the autumn theme
- **Google Gemini**: AI-powered celebration messages
- **React Community**: Excellent documentation and ecosystem
- **FastAPI Team**: Outstanding Python web framework
- **GitHub Copilot**: Development assistance and pair programming

---

*Built with ❤️ for wellness and productivity*
