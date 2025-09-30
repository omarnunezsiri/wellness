import { useState, useEffect } from "react";
import config from "../config/config";

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
          const response = await fetch(`${config.API_ENDPOINTS.USERS}`, {
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
        alert(`Error: ${error.message}`)
      } finally {
        setLoading(false);
      }
    };

    initializeUser();
  }, []);

  return { userId, loading };
};

export default useUserId;
