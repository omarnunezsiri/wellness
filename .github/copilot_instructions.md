# Daily Affirmations & Wellness Planner - Copilot Instructions

## Project Overview
A holistic wellness productivity app that combines daily planning with positive affirmations. Built for the Codédex September 2025 challenge with cozy autumn vibes. This is a learning project to explore full-stack development.

## Core Concept
- **Affirmation-First**: The main landing page is a single, beautiful affirmation.
- **Daily/Weekly Planning**: Task management and scheduling.
- **Integrated Affirmations**: Motivational messages tied to productivity moments.
- **Focus Mode**: Pomodoro timer with wellness breaks.
- **Wellness-First**: Emotional wellbeing integrated into productivity, not an afterthought.

## Tech Stack
- **Backend**: Python + FastAPI + SQLAlchemy
- **Frontend**: **React** + **Vite**
- **Database**: SQLite
- **Package Management**: uv (for Python), npm or yarn (for Node.js)
- **Deployment**: Docker

## Architecture
- **Monorepo Structure**: `backend/` and `frontend/` folders.
- **RESTful API**: Clean separation between frontend and backend.
- **User Identification**: Simple UUID-based user identification (localStorage).

## API Endpoints
### Affirmations
- `GET /affirmations` - Random affirmation
- `GET /affirmations/daily` - Consistent daily affirmation
- `GET /affirmations/categories` - Available categories
- `GET /affirmations?category=focus` - Category-specific affirmations
- `GET /affirmations/favorites?user_id=uuid` - User's saved favorites
- `POST /affirmations/{id}/favorite` - Add to favorites

### Planning
- `GET /tasks?user_id=uuid&date=YYYY-MM-DD` - Daily tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task (mark complete, etc.)
- `DELETE /tasks/{id}` - Delete task
- `GET /focus-sessions?user_id=uuid` - Pomodoro session history
- `POST /focus-sessions` - Start/end focus session

## Design Philosophy
- **Vibes**: Warm, cozy, safe-space aesthetic with a non-jarring interface.
- **September Theme**: Autumn colors (burnt orange, amber, soft browns, cream).
- **Interactions**: Gentle animations, soft shadows, and rounded corners.
- **Accessibility**: High contrast, semantic HTML, and keyboard navigation.
- **Fonts**: Use fonts that evoke a **cutesy, warmth, and cozy vibe**, such as Lora, Crimson Text, or similar hand-drawn/serif styles.
- **Visuals**:
    - **Background**: A blurred, cozy autumn scene (e.g., `autumn-forest-bg.jpg`).
    - **UI Cards**: Use a **glassmorphism** effect (translucent, frosted glass) on all main cards and pop-ups.
    - **Decorative Motifs**: Use autumnal motifs (leaves, pumpkins, acorns, coffee) as decorative borders on cards and as subtle accents in the UI.
    - **Landing Page**: A minimalist design with a single affirmation at the center.

## Frontend Structure (React)
- **Component-Based Architecture**: Build the UI with reusable components.
- `src/components/`: Reusable UI components.
    - `AffirmationDisplay.jsx`: A single component for displaying the main affirmation.
    - `DateNavigation.jsx`: Buttons for navigating between days.
    - `TaskItem.jsx`: A single task with complete/delete functionality.
    - `CelebrationModal.jsx`: The pop-up that appears on task completion.
- `src/pages/`: Main application views.
    - `LandingPage.jsx`: The initial page with only the daily affirmation and navigation to the planner.
    - `DailyPlanner.jsx`: The full page with the task list and Pomodoro timer.
- `src/hooks/`: Custom React hooks for API calls and application logic.
    - `useAffirmations.js`: Handles fetching affirmations from the backend.
    - `useTasks.js`: Manages the state and API calls for daily tasks.
- `src/styles/`: All CSS files.
    - `theme.css`: Your custom CSS properties for consistent theming.
    - `global.css`: Base styles and animations.

## Visual Assets (Expected in `src/assets/`)
- `coffee-favicon.png`: Circular coffee cup icon for favicon and branding.
- `pumpkin-decor.png`: Stylized pumpkin for decorative accents.
- `acorns-nuts.png`: Mixed nuts and acorns cluster for decorations.
- `maple-leaf.png`: A single maple leaf for individual decorative accents.
- `autumn-forest-bg.jpg`: Golden hour forest photo.

## User Experience Flow
1.  **Affirmation Landing Page**: User first lands on a simple page with a single, powerful affirmation.
2.  **Daily Focus Transition**: User clicks a button to navigate to the full planner page when they are ready to get to work.
3.  **Task Management**: Users can add, complete, and delete tasks on the planner page.
4.  **Celebratory Moments**: A positive affirmation appears in a pop-up when a task is completed.
5.  **Date Navigation**: Simple navigation on the planner page to view past or future tasks.
6.  **Progress Tracking**: A visual percentage and task summary show daily progress on the planner page.

## Code Preferences
- **Frontend**: Use functional React components with hooks.
- **Backend**: Use modern Python practices (type hints, Pydantic models).
- **General**: Prioritize readability and user experience over technical complexity. Use CSS custom properties for consistent theming. Implement responsive design.

## Learning Goals
- Frontend development (**React**)
- Modern CSS animations and responsive layouts
- API integration and state management
- User experience design principles
- Full-stack application deployment

## AI Integration Ideas (Future)
- Personalized affirmation generation based on user's goals/mood.
- Smart task categorization and priority suggestions.
- Adaptive timing for affirmations based on user behavior.

## September Challenge Focus
- Emphasis on cozy, autumn aesthetic.
- Demonstrating creativity with AI assistance (GitHub Copilot).
- Building something genuinely useful for productivity + wellness.
- Showcasing both backend architecture skills and frontend learning.
