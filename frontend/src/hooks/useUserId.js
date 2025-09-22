import { useState, useEffect } from "react";

const useUserId = () => {
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeUser = async () => {
      try {
        // Check if we already have a validated user ID
        let storedUserId = localStorage.getItem("validatedUserId");

        if (!storedUserId) {
          // Create a new user via backend
          const response = await fetch("/api/users", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          });

          if (!response.ok) {
            throw new Error("Failed to create user");
          }

          const data = await response.json();
          storedUserId = data.user_id;
          localStorage.setItem("validatedUserId", storedUserId);
        }

        setUserId(storedUserId);
      } catch (error) {
        console.error("Failed to initialize user:", error);
        // Fallback: try to use old user ID if it exists, but mark as unvalidated
        const oldUserId = localStorage.getItem("anonymousUserId");
        if (oldUserId) {
          console.warn("Using unvalidated user ID from legacy storage");
          setUserId(oldUserId);
        }
      } finally {
        setLoading(false);
      }
    };

    initializeUser();
  }, []);

  return { userId, loading };
};

export default useUserId;
