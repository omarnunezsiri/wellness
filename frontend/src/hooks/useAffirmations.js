import { useState, useCallback, useEffect } from "react";
import config from "../config/config";

const useAffirmations = () => {
  const [affirmation, setAffirmation] = useState("");
  const [error, setError] = useState(null);
  const [initialized, setInitialized] = useState(false);

  const fetchAffirmation = useCallback(async () => {
    setError(null);

    try {
      const response = await fetch(
        `${config.API_BASE_URL}${config.API_ENDPOINTS.AFFIRMATIONS}`,
      );

      if (!response.ok) {
        throw new Error("Failed to fetch affirmation");
      }

      const data = await response.json();
      setAffirmation(data.text);
    } catch (err) {
      setError(err.message);
      console.error("Error fetching affirmation:", err);
      // Fallback affirmation
      setAffirmation("You are capable of amazing things.");
    }
  }, []);

  // Auto-fetch on first use
  useEffect(() => {
    if (!initialized && !affirmation) {
      setInitialized(true);
      fetchAffirmation();
    }
  }, [initialized, affirmation, fetchAffirmation]);

  return {
    affirmation,
    error,
    fetchAffirmation,
    refreshAffirmation: fetchAffirmation,
  };
};

export default useAffirmations;
