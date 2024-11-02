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
      userExists: false, // New state property to track user existence
      showSignup: false, // New state property to manage signup modal visibility
    },
    actions: {
      // Example function to change color
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },

      checkUserExists: async () => {
        try {
          const resp = await fetch(
            process.env.BACKEND_URL + "/api/check-users"
          );
          const data = await resp.json();
          setStore({ userExists: data.exists });
        } catch (error) {
          console.error("Error checking user existence:", error);
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
