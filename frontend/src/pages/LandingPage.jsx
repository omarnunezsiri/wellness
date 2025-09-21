import useAffirmations from "../hooks/useAffirmations";
import AffirmationDisplay from "../components/AffirmationDisplay";

const LandingPage = ({ onStartDay }) => {
  const { affirmation, refreshAffirmation } = useAffirmations();

  return (
    <div className="landing-page">
      <h1 className="title">Daily Wellness</h1>

      <AffirmationDisplay
        text={affirmation || "You are capable of amazing things."}
        onRefresh={refreshAffirmation}
        showRefreshButton={true}
      />

      <button className="btn start-day-btn" onClick={onStartDay}>
        Start Your Day 🍂
      </button>
    </div>
  );
};

export default LandingPage;
