import { useState } from "react";
import "./styles/global.css";
import useUserId from "./hooks/useUserId";
import FallingLeaves from "./components/FallingLeaves";
import LandingPage from "./pages/LandingPage";
import DailyPlanner from "./pages/DailyPlanner";

function App() {
  const [view, setView] = useState("landing");
  const { userId, loading } = useUserId();

  // Don't render anything until we have a user ID
  if (loading || !userId) {
    return (
      <div id="root">
        <FallingLeaves />
        <div className="container">
          <div className="main-card">
            <p>Initializing your wellness space...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div id="root">
      <FallingLeaves />
      <div className="container">
        <div className="main-card">
          {view === "landing" ? (
            <LandingPage onStartDay={() => setView("planner")} />
          ) : (
            <DailyPlanner
              userId={userId}
              onBackToLanding={() => setView("landing")}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
