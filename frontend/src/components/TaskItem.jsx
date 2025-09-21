const TaskItem = ({ task, onToggleComplete, onDelete }) => {
  return (
    <div className={`task-item ${task.completed ? "completed" : ""}`}>
      <input
        type="checkbox"
        id={`task-${task.id}`}
        className="custom-checkbox"
        checked={task.completed}
        onChange={(e) => onToggleComplete(task.id, e.target.checked)}
      />
      <label htmlFor={`task-${task.id}`} className="task-label">
        {task.description}
      </label>
      <button className="delete-task" onClick={() => onDelete(task.id)}>
        ×
      </button>
    </div>
  );
};

export default TaskItem;
