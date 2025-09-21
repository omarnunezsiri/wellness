import { useState, useEffect } from "react";

const useUserId = () => {
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    // Remove any old user ID keys
    localStorage.removeItem("affirmations-user-id");

    // Get or create anonymous user ID
    let storedUserId = localStorage.getItem("anonymousUserId");

    if (!storedUserId) {
      storedUserId = self.crypto.randomUUID();
      localStorage.setItem("anonymousUserId", storedUserId);
    }

    setUserId(storedUserId);
  }, []);

  return userId;
};

export default useUserId;
