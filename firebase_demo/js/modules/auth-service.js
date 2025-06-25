import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    signInWithPopup
} from "https://www.gstatic.com/firebasejs/11.8.1/firebase-auth.js";
import { auth, googleProvider } from "../config/firebase-init.js";

async function registerUser(email, password) {
    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        return userCredential;
    } catch (error) {
        console.error("Error registering user:", error);
        throw error;
    }
}

async function loginUser(email, password) {
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        return userCredential;
    } catch (error) {
        console.error("Error logging in user:", error);
        throw error;
    }
}

async function logoutUser() {
    try {
        await signOut(auth);
    } catch (error) {
        console.error("Error logging out user:", error);
        throw error;
    }
}

function observeAuthState(callback) {
    return onAuthStateChanged(auth, callback);
}

async function loginWithGoogle() {
    try {
        const result = await signInWithPopup(auth, googleProvider);
        return result;
    } catch (error) {
        console.error("Error signing in with Google:", error);
        throw error;
    }
}

export { registerUser, loginUser, logoutUser, observeAuthState, loginWithGoogle }; 