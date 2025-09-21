import { useEffect, useState } from "react";

const CelebrationModal = ({
  show,
  onClose,
  message = "Great job! Task completed! 🎉",
}) => {
  const [sparkles, setSparkles] = useState([]);

  useEffect(() => {
    if (show) {
      // Generate sparkle positions
      const newSparkles = [];
      for (let i = 0; i < 8; i++) {
        newSparkles.push({
          id: i,
          left: Math.random() * 100,
          top: Math.random() * 100,
          delay: Math.random() * 1.5,
        });
      }
      setSparkles(newSparkles);

      // Auto-close after 5 seconds
      const timer = setTimeout(onClose, 5000);
      return () => clearTimeout(timer);
    }
  }, [show, onClose]);

  if (!show) return null;

  return (
    <div className="celebration-modal-overlay">
      <div className="celebration-modal">
        <div className="celebration-emoji">🎉</div>
        <p className="celebration-message">{message}</p>

        {/* Animated sparkles */}
        {sparkles.map((sparkle) => (
          <div
            key={sparkle.id}
            className="sparkle"
            style={{
              left: `${sparkle.left}%`,
              top: `${sparkle.top}%`,
              animationDelay: `${sparkle.delay}s`,
            }}
          >
            ✧
          </div>
        ))}
      </div>
    </div>
  );
};

export default CelebrationModal;
