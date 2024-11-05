const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      message: null,
      demo: [
        {
          title: "FIRST",
          background: "white",
          initial: "white",
        },
        {
          title: "SECOND",
          background: "white",
          initial: "white",
        },
      ],
      userExists: false, // Track if any user exists
      showSignup: false, // Manage visibility of signup modal
      userCheckCompleted: false, // Track if the user check has already run
    },
    actions: {
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },

      checkUserExists: async () => {
        const store = getStore();

        // Prevent re-checking if it's already done
        if (store.userCheckCompleted) return;

        try {
          const resp = await fetch(
            process.env.BACKEND_URL + "/api/check-users"
          );
          const data = await resp.json();
          setStore({ userExists: data.exists, userCheckCompleted: true });

          // Show signup if no user exists
          if (!data.exists) {
            setStore({ showSignup: true });
          }
        } catch (error) {
          console.error("Error checking user existence:", error);
        }
      },

      signup: async (userInfo) => {
        try {
          const response = await fetch(
            process.env.BACKEND_URL + "/api/signup",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(userInfo),
            }
          );
          if (response.ok) {
            const data = await response.json();
            console.log("Signup successful:", data);

            // Set userExists to true and hide the signup modal after successful signup
            setStore({ userExists: true, showSignup: false });
            // Reload the page to reset the state (optional)
            window.location.reload();
          } else {
            console.error("Signup failed:", response.statusText);
          }
        } catch (error) {
          console.error("Error during signup:", error);
        }
      },

      changeColor: (index, color) => {
        const store = getStore();
        const demo = store.demo.map((elm, i) => {
          if (i === index) elm.background = color;
          return elm;
        });
        setStore({ demo: demo });
      },
    },
  };
};

export default getState;
