const DateNavigation = ({ currentDate, onPreviousDay, onNextDay }) => {
  const formatDate = (date) => {
    const options = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    return date.toLocaleDateString("en-US", options);
  };

  const getDateTitle = (date) => {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return "Today's Focus";
    } else if (date.toDateString() === tomorrow.toDateString()) {
      return "Tomorrow's Focus";
    } else if (date.toDateString() === yesterday.toDateString()) {
      return "Yesterday's Focus";
    } else {
      return "Daily Focus";
    }
  };

  return (
    <div className="date-navigation">
      <h1 className="title">{getDateTitle(currentDate)}</h1>
      <div className="date-controls">
        <button className="btn date-btn" onClick={onPreviousDay}>
          ← Previous Day
        </button>
        <span className="current-date">{formatDate(currentDate)}</span>
        <button className="btn date-btn" onClick={onNextDay}>
          Next Day →
        </button>
      </div>
    </div>
  );
};

export default DateNavigation;
