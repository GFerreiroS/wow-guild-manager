import React, { useContext, useEffect, useState } from "react"; // Import useStateimport { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import Context from "../store/appContext";
import "../../styles/home.css";
import Signup from "../component/signup";

export const Home = () => {
  const { store, actions } = useContext(Context);
  const [showSignup, setShowSignup] = useState(false);

  useEffect(() => {
    const fetchUserExists = async () => {
      await actions.checkUserExists(); // Check if users exist
      if (!store.userExists) {
        setShowSignup(true); // Show signup modal if no users exist
      }
    };
    fetchUserExists();
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

      {/* Signup Modal */}
      {showSignup && <Signup onClose={() => setShowSignup(false)} />}
    </div>
  );
};
