// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDp-1qFDNYI7mJJKtV_W7ZxCk62lcR2mnA",
  authDomain: "ai-interview-coach-d606f.firebaseapp.com",
  projectId: "ai-interview-coach-d606f",
  storageBucket: "ai-interview-coach-d606f.firebasestorage.app",
  messagingSenderId: "1031670077614",
  appId: "1:1031670077614:web:98e9fecb05274f0823753f",
  measurementId: "G-N0T2RXJKZH"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export const auth = getAuth(app);