import { loginUser, loginWithGoogle, observeAuthState } from "../modules/auth-service.js";

// Get DOM elements
const loginForm = document.getElementById("login-form");
const loginEmail = document.getElementById("login-email");
const loginPassword = document.getElementById("login-password");
const loginMessageDiv = document.getElementById("login-message");

// Check if user is already logged in
observeAuthState((user) => {
    if (user) {
        // Redirect to home page if already logged in
        window.location.href = "index.html";
    }
});

// Add form submit handler
loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    // Clear previous messages
    loginMessageDiv.textContent = "";
    loginMessageDiv.className = "message";
    
    try {
        const email = loginEmail.value;
        const password = loginPassword.value;
        
        await loginUser(email, password);
        // Auth state observer will handle redirect
    } catch (error) {
        loginMessageDiv.textContent = error.message;
        loginMessageDiv.classList.add("error-message");
    }
});

// Add Google sign-in button handler
const googleSignInButton = document.getElementById('google-signin');
googleSignInButton.addEventListener('click', async () => {
    try {
        loginMessageDiv.textContent = '';
        loginMessageDiv.className = 'message';
        await loginWithGoogle();
        // onAuthStateChanged will handle the redirect
    } catch (error) {
        loginMessageDiv.textContent = error.message;
        loginMessageDiv.classList.add('error-message');
    }
}); 