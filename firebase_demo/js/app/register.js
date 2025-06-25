import { registerUser, observeAuthState } from "../modules/auth-service.js";

// Get DOM elements
const registerForm = document.getElementById("register-form");
const registerEmail = document.getElementById("register-email");
const registerPassword = document.getElementById("register-password");
const confirmPassword = document.getElementById("confirm-password");
const registerMessageDiv = document.getElementById("register-message");

// Check if user is already logged in
observeAuthState((user) => {
    if (user) {
        // Redirect to home page if already logged in
        window.location.href = "index.html";
    }
});

// Add form submit handler
registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    // Clear previous messages
    registerMessageDiv.textContent = "";
    registerMessageDiv.className = "message";
    
    const email = registerEmail.value;
    const password = registerPassword.value;
    const confirmedPassword = confirmPassword.value;
    
    // Check if passwords match
    if (password !== confirmedPassword) {
        registerMessageDiv.textContent = "Passwords do not match.";
        registerMessageDiv.classList.add("error-message");
        return;
    }
    
    try {
        await registerUser(email, password);
    } catch (error) {
        registerMessageDiv.textContent = error.message;
        registerMessageDiv.classList.add("error-message");
    }
}); 