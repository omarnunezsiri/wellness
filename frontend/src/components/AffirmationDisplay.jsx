const AffirmationDisplay = ({ text, onRefresh, showRefreshButton = false }) => {
  return (
    <div className="affirmation-container">
      <div className="affirmation-text">"{text}"</div>
      {showRefreshButton && (
        <button
          type="button"
          className="btn refresh-btn"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            if (onRefresh) {
              onRefresh();
            }
          }}
        >
          🧡 New Affirmation
        </button>
      )}
    </div>
  );
};

export default AffirmationDisplay;
