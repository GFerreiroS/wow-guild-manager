import React, { useState } from "react";
import { Link } from "react-router-dom";
import Login from "./login"; // Adjust the import path as necessary
import Signup from "./signup"; // Adjust the import path as necessary

export const Navbar = () => {
  const [showModal, setShowModal] = useState("");

  const handleOpenModal = (type) => {
    setShowModal(type);
  };

  const handleCloseModal = () => {
    setShowModal("");
  };

  return (
    <nav className="navbar navbar-light bg-light">
      <div className="container">
        <Link to="/">
          <span className="navbar-brand mb-0 h1">React Boilerplate</span>
        </Link>
        <div className="ml-auto">
          <button
            className="btn btn-primary"
            onClick={() => handleOpenModal("login")}
          >
            Login / Signup
          </button>
        </div>
      </div>

      {showModal === "login" && (
        <Login
          onClose={handleCloseModal}
          switchToSignup={() => handleOpenModal("signup")}
        />
      )}
      {showModal === "signup" && <Signup onClose={handleCloseModal} />}
    </nav>
  );
};
