import { useState, useCallback } from "react";
import config from "../config/config";

const useTasks = (userId) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const formatDate = (date) => {
    return date.toISOString().split("T")[0];
  };

  const loadDailyData = useCallback(
    async (date) => {
      setLoading(true);
      setError(null);

      try {
        const dateStr = formatDate(date);
        const response = await fetch(
          `${config.API_BASE_URL}${config.API_ENDPOINTS.DAILY_DATA}?date=${dateStr}&user_id=${userId}`,
        );

        if (!response.ok) {
          throw new Error("Failed to load daily data");
        }

        const data = await response.json();
        setTasks(data.tasks || []);
        return data;
      } catch (err) {
        setError(err.message);
        console.error("Error loading daily data:", err);
        setTasks([]);
      } finally {
        setLoading(false);
      }
    },
    [userId],
  );

  const addTask = useCallback(
    async (taskText, date) => {
      setError(null);

      // Input validation
      if (!taskText || taskText.trim().length === 0) {
        throw new Error("Task text is required");
      }

      const trimmedText = taskText.trim();
      if (trimmedText.length < 3) {
        throw new Error("Task text must be at least 3 characters long");
      }

      if (trimmedText.length > 100) {
        throw new Error("Task text must be 100 characters or less");
      }

      try {
        const dateStr = formatDate(date);
        const response = await fetch(
          `${config.API_BASE_URL}${config.API_ENDPOINTS.TASKS}?date=${dateStr}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              task_text: trimmedText,
              user_id: userId,
            }),
          },
        );

        if (!response.ok) {
          throw new Error("Failed to create task");
        }

        const newTask = await response.json();
        setTasks((prev) => [...prev, newTask]);
        return newTask;
      } catch (err) {
        setError(err.message);
        console.error("Error creating task:", err);
        throw err;
      }
    },
    [userId],
  );

  const toggleTask = useCallback(async (taskId, completed) => {
    setError(null);

    try {
      const response = await fetch(
        `${config.API_BASE_URL}${config.API_ENDPOINTS.TASKS}/${taskId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            completed: completed,
          }),
        },
      );

      if (!response.ok) {
        throw new Error("Failed to update task");
      }

      const updatedTask = await response.json();
      setTasks((prev) =>
        prev.map((task) =>
          task.id === taskId ? { ...task, completed: completed } : task,
        ),
      );

      return updatedTask;
    } catch (err) {
      setError(err.message);
      console.error("Error updating task:", err);
      // Revert the UI change if the API call failed
      setTasks((prev) =>
        prev.map((task) =>
          task.id === taskId ? { ...task, completed: !completed } : task,
        ),
      );
      throw err;
    }
  }, []);

  const deleteTask = useCallback(async (taskId) => {
    setError(null);

    try {
      const response = await fetch(
        `${config.API_BASE_URL}${config.API_ENDPOINTS.TASKS}/${taskId}`,
        {
          method: "DELETE",
        },
      );

      if (!response.ok) {
        throw new Error("Failed to delete task");
      }

      setTasks((prev) => prev.filter((task) => task.id !== taskId));
    } catch (err) {
      setError(err.message);
      console.error("Error deleting task:", err);
      throw err;
    }
  }, []);

  return {
    tasks,
    loading,
    error,
    loadDailyData,
    addTask,
    toggleTask,
    deleteTask,
  };
};

export default useTasks;
