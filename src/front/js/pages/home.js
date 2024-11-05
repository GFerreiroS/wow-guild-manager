import React, { useContext, useEffect, useState } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import UserWizard from "../component/userWizard"; // Adjust the path if necessary

export const Home = () => {
  const { store, actions } = useContext(Context);
  const [showWizard, setShowWizard] = useState(false);

  useEffect(() => {
    const checkUserExists = async () => {
      await actions.checkUserExists(); // Check if users exist
      if (!store.userExists) {
        setShowWizard(true); // Show wizard if no users exist
      }
    };
    checkUserExists();
  }, [actions, store.userExists]);

  return (
    <div className="text-center mt-5">
      <h1>Hello Rigo!!</h1>
      <p>
        <img src={rigoImageUrl} alt="Rigo" />
      </p>
      <p>
        This boilerplate comes with lots of documentation:{" "}
        <a href="https://start.4geeksacademy.com/starters/react-flask">
          Read documentation
        </a>
      </p>

      {/* Show Wizard if no users exist */}
      {showWizard && <UserWizard onClose={() => setShowWizard(false)} />}
    </div>
  );
};
