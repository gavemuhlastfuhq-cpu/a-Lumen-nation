import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
import { getFunctions } from "firebase/functions";

/**
 * Replace the placeholders below with your Firebase Web config:
 * (From Firebase Console -> Project settings -> General -> Your apps -> SDK setup)
 */
const firebaseConfig = {
  apiKey: "REPLACE_WITH_YOUR_APIKEY",
  authDomain: "REPLACE_WITH_YOUR_AUTHDOMAIN",
  projectId: "REPLACE_WITH_YOUR_PROJECTID",
  storageBucket: "REPLACE_WITH_YOUR_STORAGEBUCKET",
  messagingSenderId: "REPLACE_WITH_YOUR_MESSAGING_SENDER_ID",
  appId: "REPLACE_WITH_YOUR_APPID"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
export const functions = getFunctions(app);
export default app;
