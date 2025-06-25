import { observeAuthState, logoutUser } from "../modules/auth-service.js";

// Get DOM elements
const userInfoDiv = document.getElementById("user-info");
const authLinksDiv = document.getElementById("auth-links");
const userActionsDiv = document.getElementById("user-actions");
const logoutButton = document.getElementById("logout-button");
const navLoginLink = document.getElementById("nav-login-link");
const navRegisterLink = document.getElementById("nav-register-link");

// Observe auth state changes
observeAuthState((user) => {
    if (user){
        handleUserLoggedIn(user);
    }else{
        handleUserLoggedOut();
    }
});


// handle if logged in
function handleUserLoggedIn(user) {
          userInfoDiv.innerHTML = `<p>Welcome, ${user.email}!</p>`;
          authLinksDiv.style.display = "none";
          userActionsDiv.style.display = "block";
          navLoginLink.style.display = "none";
          navRegisterLink.style.display = "none";
          logoutButton.addEventListener("click", async () => {
            try {
              await logoutUser();
              // Auth state observer will handle UI updates
            } catch (error) {
              console.error("Error during logout:", error);
            }
          });
}

// handle if logged out
function handleUserLoggedOut() {
          userInfoDiv.innerHTML = "";
          authLinksDiv.style.display = "block";
          userActionsDiv.style.display = "none";
          navLoginLink.style.display = "inline";
          navRegisterLink.style.display = "inline";
}
