import { useState, useEffect } from "react";
import useAffirmations from "../hooks/useAffirmations";
import useTasks from "../hooks/useTasks";
import DateNavigation from "../components/DateNavigation";
import AffirmationDisplay from "../components/AffirmationDisplay";
import TaskList from "../components/TaskList";
import CelebrationModal from "../components/CelebrationModal";
import config from "../config/config";

const DailyPlanner = ({ userId, onBackToLanding }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [showCelebration, setShowCelebration] = useState(false);
  const [celebrationMessage, setCelebrationMessage] = useState("");

  const { affirmation, refreshAffirmation } = useAffirmations();
  const { tasks, loading, loadDailyData, addTask, toggleTask, deleteTask } =
    useTasks(userId);

  useEffect(() => {
    if (userId) {
      loadDailyData(currentDate);
    }
  }, [currentDate, userId, loadDailyData]);

  const handlePreviousDay = () => {
    const newDate = new Date(currentDate);
    newDate.setDate(newDate.getDate() - 1);
    setCurrentDate(newDate);
  };

  const handleNextDay = () => {
    const newDate = new Date(currentDate);
    newDate.setDate(newDate.getDate() + 1);
    setCurrentDate(newDate);
  };

  const handleAddTask = async (taskText) => {
    try {
      await addTask(taskText, currentDate);
    } catch (error) {
      console.error("Failed to add task:", error);
    }
  };

  const handleToggleTask = async (taskId, completed) => {
    // Find the task BEFORE the toggle operation to avoid race condition
    const taskToToggle = tasks.find((task) => task.id === taskId);

    try {
      await toggleTask(taskId, completed);
    } catch (error) {
      console.error("Failed to toggle task:", error);
      return;
    }

    // Show celebration if task was completed
    if (completed && taskToToggle) {
      try {
        console.log("Attempting to fetch AI celebration...");
        console.log("Completed task:", taskToToggle);
        console.log("All tasks:", tasks);

  const response = await fetch(config.API_ENDPOINTS.CELEBRATE_TASK, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            completed_task:
              taskToToggle?.text || taskToToggle?.description || "Unknown task",
          }),
        });

        console.log("Response status:", response.status);

        if (response.ok) {
          const data = await response.json();
          console.log("AI response:", data);
          setCelebrationMessage(
            data.message || "Wonderful! You completed a task! 🎉",
          );
        } else {
          console.error(
            "Failed to fetch celebration message:",
            response.status,
            response.statusText,
          );
          setCelebrationMessage("Wonderful! You completed a task! 🎉");
        }
      } catch (celebrationError) {
        console.error("Error fetching AI celebration:", celebrationError);
        setCelebrationMessage("Wonderful! You completed a task! 🎉");
      }

      setShowCelebration(true);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await deleteTask(taskId);
    } catch (error) {
      console.error("Failed to delete task:", error);
    }
  };

  return (
    <div className="daily-planner">
      <div className="back-section">
        <button className="btn home-btn" onClick={onBackToLanding} title="Back to Home">
        </button>
      </div>

      <DateNavigation
        currentDate={currentDate}
        onPreviousDay={handlePreviousDay}
        onNextDay={handleNextDay}
      />

      <div className="affirmation-section">
        <AffirmationDisplay
          text={affirmation || "You are capable of amazing things."}
          onRefresh={refreshAffirmation}
          showRefreshButton={true}
        />
      </div>

      {loading ? (
        <div className="loading-section">
          <p>Loading your tasks...</p>
        </div>
      ) : (
        <div className="task-section">
          <TaskList
            tasks={tasks}
            onToggleComplete={handleToggleTask}
            onDelete={handleDeleteTask}
            onAddTask={handleAddTask}
            userId={userId}
          />
        </div>
      )}

      <CelebrationModal
        show={showCelebration}
        onClose={() => setShowCelebration(false)}
        message={celebrationMessage}
      />
    </div>
  );
};

export default DailyPlanner;
