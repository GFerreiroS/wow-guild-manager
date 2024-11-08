import React, { useState, useContext, useEffect } from "react";
import { Context } from "../store/appContext"; // Ensure the context path is correct

const userWizard = ({ onClose }) => {
  const { actions } = useContext(Context);
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleNext = () => setStep(step + 1);
  const handlePrev = () => setStep(step - 1);

  const handleSubmit = async () => {
    try {
      const result = await actions.signup({ email, password });
      if (result) {
        onClose(); // Close the wizard on successful user creation
        window.location.reload(); // Reload to refresh app state
      } else {
        setError("Failed to create user. Please try again.");
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
    }
  };

  return (
    <div
      className="modal show d-block"
      style={{ backgroundColor: "rgba(0, 0, 0, 0.5)" }}
    >
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Setup Wizard</h5>
            <button
              type="button"
              className="btn-close"
              aria-label="Close"
              onClick={onClose}
            ></button>
          </div>
          <div className="modal-body">
            {step === 1 && (
              <div>
                <h5>Welcome to the Setup Wizard</h5>
                <p>
                  This setup will guide you through creating the first user.
                </p>
                <button className="btn btn-primary mt-3" onClick={handleNext}>
                  Get Started
                </button>
              </div>
            )}
            {step === 2 && (
              <div>
                <h5>Enter Your Information</h5>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <button className="btn btn-secondary me-2" onClick={handlePrev}>
                  Back
                </button>
                <button className="btn btn-primary" onClick={handleNext}>
                  Next
                </button>
              </div>
            )}
            {step === 3 && (
              <div>
                <h5>Confirm Your Details</h5>
                <p>Email: {email}</p>
                <p>Password: {password.replace(/./g, "*")}</p>
                {error && <div className="alert alert-danger">{error}</div>}
                <button className="btn btn-secondary me-2" onClick={handlePrev}>
                  Back
                </button>
                <button className="btn btn-success" onClick={handleSubmit}>
                  Create User
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default userWizard;
