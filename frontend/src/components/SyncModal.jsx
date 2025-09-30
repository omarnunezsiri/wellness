import { useState } from "react";
import config from "../config/config";

const SyncModal = ({ show, onClose, userId }) => {
  const [mode, setMode] = useState("choose"); // "choose", "generate", "enter"
  const [syncCode, setSyncCode] = useState("");
  const [generatedCode, setGeneratedCode] = useState("");
  const [inputCode, setInputCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showCopied, setShowCopied] = useState(false);

  if (!show) return null;

  const handleGenerateCode = async () => {
    setIsLoading(true);
    setError("");

    try {
  const response = await fetch(config.API_ENDPOINTS.SYNC_GENERATE_CODE, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          uuid: userId,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate sync code");
      }

      const data = await response.json();
      setGeneratedCode(data.sync_code);
      setMode("generate");
    } catch (err) {
      setError("Failed to generate sync code. Please try again.");
      console.error("Error generating sync code:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnterCode = () => {
    setMode("enter");
  };

  const handleSubmitCode = async () => {
    setIsLoading(true);
    setError("");

    try {
  const response = await fetch(config.API_ENDPOINTS.SYNC_VALIDATE_CODE, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sync_code: inputCode,
          current_uuid: userId,
        }),
      });

      if (!response.ok) {
        throw new Error("Invalid or expired sync code");
      }

      const data = await response.json();

      // Update localStorage with the new UUID
      localStorage.setItem('validatedUserId', data.uuid);

      // Close modal and reload the page to use the new UUID
      onClose();
      window.location.reload();

    } catch (err) {
      setError("Invalid or expired sync code. Please check and try again.");
      console.error("Error validating sync code:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(generatedCode);
    setShowCopied(true);
    setTimeout(() => setShowCopied(false), 2000); // Hide after 2 seconds
  };

  const resetModal = () => {
    setMode("choose");
    setGeneratedCode("");
    setInputCode("");
    setError("");
    setIsLoading(false);
    setShowCopied(false);
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

            {error && (
              <div className="sync-error">
                {error}
              </div>
            )}

            <div className="sync-options">
              <button
                className="sync-option-btn generate-btn"
                onClick={handleGenerateCode}
                disabled={isLoading}
              >
                <div className="sync-option-icon">
                  {isLoading ? "⏳" : "📱"}
                </div>
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
              <button className={`btn copy-btn ${showCopied ? 'copied' : ''}`} onClick={handleCopyCode}>
                {showCopied ? "✨ Copied!" : "📋 Copy Code"}
              </button>
            </div>

            <div className="sync-instructions">
              <p><strong>How to use:</strong></p>
              <ol>
                <li>Open the wellness app on your other device</li>
                <li>Click the sync button and select "Enter Sync Code"</li>
                <li>Paste the code above to access the same tasks</li>
              </ol>
              <p><em>Note: This will switch your device to use the same task data.</em></p>
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

            {error && (
              <div className="sync-error">
                {error}
              </div>
            )}

            <div className="sync-code-input">
              <textarea
                value={inputCode}
                onChange={(e) => setInputCode(e.target.value.toLowerCase())}
                placeholder="paste sync code here"
                maxLength="64"
                rows="3"
                autoFocus
                disabled={isLoading}
              />
              <button
                className="btn sync-connect-btn"
                onClick={handleSubmitCode}
                disabled={inputCode.length !== 64 || isLoading}
              >
                {isLoading ? "⏳ Connecting..." : "🔗 Connect Devices"}
              </button>
            </div>

            <div className="sync-instructions">
              <p><strong>Need help?</strong></p>
              <p>Make sure the other device is generating a sync code and paste the full code exactly as shown.</p>
              <p><em>This will switch your device to access the same tasks as the other device.</em></p>
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
