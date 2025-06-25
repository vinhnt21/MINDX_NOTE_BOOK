import { observeAuthState, logoutUser } from "../modules/auth-service.js";

// Get DOM elements

// Observe auth state changes
observeAuthState((user) => {
  if (user) {
    handleUserLoggedIn(user);
  } else {
    handleUserLoggedOut();
  }
});

// handle if logged in
function handleUserLoggedIn(user) {
  
}

// handle if logged out
function handleUserLoggedOut() {
 
}
