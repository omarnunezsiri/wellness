import { useState } from "react";

const SyncModal = ({ show, onClose }) => {
  const [mode, setMode] = useState("choose"); // "choose", "generate", "enter"
  const [syncCode, setSyncCode] = useState("");
  const [generatedCode, setGeneratedCode] = useState("");
  const [inputCode, setInputCode] = useState("");

  if (!show) return null;

  const handleGenerateCode = () => {
    // Generate a mock SHA256-like hash for now (64 hex characters)
    const code = Array.from({length: 64}, () => Math.floor(Math.random() * 16).toString(16)).join('').toUpperCase();
    setGeneratedCode(code);
    setMode("generate");
  };

  const handleEnterCode = () => {
    setMode("enter");
  };

  const handleSubmitCode = () => {
    console.log("Syncing with code:", inputCode);
    // Here you'll implement the actual sync logic
    onClose();
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(generatedCode);
    // You could add a toast notification here
  };

  const resetModal = () => {
    setMode("choose");
    setGeneratedCode("");
    setInputCode("");
  };

  const handleClose = () => {
    resetModal();
    onClose();
  };

  return (
    <div className="sync-modal-overlay" onClick={handleClose}>
      <div className="sync-modal" onClick={(e) => e.stopPropagation()}>
        <button className="sync-modal-close" onClick={handleClose}>
          ×
        </button>

        {mode === "choose" && (
          <>
            <div className="sync-modal-header">
              <h3>Sync Your Tasks</h3>
              <p>Keep your tasks synchronized across all your devices</p>
            </div>

            <div className="sync-options">
              <button className="sync-option-btn generate-btn" onClick={handleGenerateCode}>
                <div className="sync-option-icon">📱</div>
                <div className="sync-option-content">
                  <h4>Generate Sync Code</h4>
                  <p>Create a code to sync this device with others</p>
                </div>
              </button>

              <button className="sync-option-btn enter-btn" onClick={handleEnterCode}>
                <div className="sync-option-icon">💻</div>
                <div className="sync-option-content">
                  <h4>Enter Sync Code</h4>
                  <p>Connect to an existing device using a sync code</p>
                </div>
              </button>
            </div>
          </>
        )}

        {mode === "generate" && (
          <>
            <div className="sync-modal-header">
              <h3>Your Sync Code</h3>
              <p>Share this code with your other devices</p>
            </div>

            <div className="sync-code-display">
              <div className="sync-code">{generatedCode}</div>
              <button className="btn copy-btn" onClick={handleCopyCode}>
                📋 Copy Code
              </button>
            </div>

            <div className="sync-instructions">
              <p><strong>How to use:</strong></p>
              <ol>
                <li>Open the wellness app on your other device</li>
                <li>Click the sync button and select "Enter Sync Code"</li>
                <li>Enter the code above to sync your tasks</li>
              </ol>
            </div>

            <button className="btn back-btn" onClick={resetModal}>
              ← Back to Options
            </button>
          </>
        )}

        {mode === "enter" && (
          <>
            <div className="sync-modal-header">
              <h3>Enter Sync Code</h3>
              <p>Enter the code from your other device</p>
            </div>

            <div className="sync-code-input">
              <textarea
                value={inputCode}
                onChange={(e) => setInputCode(e.target.value.toUpperCase())}
                placeholder="PASTE SYNC CODE HERE"
                maxLength="64"
                rows="3"
                autoFocus
              />
              <button
                className="btn sync-connect-btn"
                onClick={handleSubmitCode}
                disabled={inputCode.length !== 64}
              >
                🔗 Connect Devices
              </button>
            </div>

            <div className="sync-instructions">
              <p><strong>Need help?</strong></p>
              <p>Make sure the other device is generating a sync code and paste the full code exactly as shown.</p>
            </div>

            <button className="btn back-btn" onClick={resetModal}>
              ← Back to Options
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default SyncModal;
