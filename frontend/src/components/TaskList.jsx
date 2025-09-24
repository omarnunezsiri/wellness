import { useState } from "react";
import TaskItem from "./TaskItem";
import SyncModal from "./SyncModal";

const TaskList = ({ tasks, onToggleComplete, onDelete, onAddTask }) => {
  const [showInput, setShowInput] = useState(false);
  const [newTaskText, setNewTaskText] = useState("");
  const [showSyncModal, setShowSyncModal] = useState(false);

  const handleSaveTask = () => {
    if (newTaskText.trim()) {
      onAddTask(newTaskText.trim());
      setNewTaskText("");
      setShowInput(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSaveTask();
    } else if (e.key === "Escape") {
      setShowInput(false);
      setNewTaskText("");
    }
  };

  const calculateProgress = () => {
    if (tasks.length === 0) return { percentage: 0, completed: 0, total: 0 };
    const completed = tasks.filter((task) => task.completed).length;
    const percentage = Math.round((completed / tasks.length) * 100);
    return { percentage, completed, total: tasks.length };
  };

  const progress = calculateProgress();

  return (
    <div className="task-list-container">
      {/* Tasks Header with inline Add Task button */}
      <div className="tasks-header">
        <h3>Today's Tasks</h3>
        <div className="header-buttons">
          {!showInput && (
            <button
              className="btn add-task-btn"
              onClick={() => setShowInput(true)}
            >
              + Add Task
            </button>
          )}
          <button
            className="btn sync-btn"
            onClick={() => setShowSyncModal(true)}
            title="Sync tasks across devices"
          >
            ☁️
          </button>
        </div>
      </div>

      {/* Task Input Area (when active) */}
      {showInput && (
        <div className="task-input-area">
          <input
            type="text"
            value={newTaskText}
            onChange={(e) => setNewTaskText(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="What would you like to accomplish?"
            autoFocus
          />
          <div className="task-input-buttons">
            <button className="btn save-task-btn" onClick={handleSaveTask}>
              Save Task
            </button>
            <button
              className="btn cancel-task-btn"
              onClick={() => {
                setShowInput(false);
                setNewTaskText("");
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Task List */}
      <div className="task-list">
        {tasks.length === 0 ? (
          <div className="empty-tasks">
            No tasks yet. Add one to get started! 🍂
          </div>
        ) : (
          <ul>
            {tasks.map((task) => (
              <li key={task.id}>
                <TaskItem
                  task={task}
                  onToggleComplete={onToggleComplete}
                  onDelete={onDelete}
                />
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Progress Circle - AFTER tasks like in original */}
      <div className="task-progress-summary">
        <div
          className="progress-circle"
          style={{
            background: `conic-gradient(var(--soft-orange) 0deg ${(progress.percentage / 100) * 360}deg, rgba(232, 168, 124, 0.2) ${(progress.percentage / 100) * 360}deg 360deg)`,
          }}
        >
          <div className="progress-text">{progress.percentage}%</div>
        </div>
        <p>
          {progress.completed} of {progress.total} tasks completed
        </p>
      </div>

      <SyncModal
        show={showSyncModal}
        onClose={() => setShowSyncModal(false)}
      />
    </div>
  );
};

export default TaskList;
