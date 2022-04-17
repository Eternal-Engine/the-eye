// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: 'AIzaSyAtTR1XbW8XkbW1daftz4vL-WFKcDCH48k',
  authDomain: 'iwitness-c14c0.firebaseapp.com',
  projectId: 'iwitness-c14c0',
  storageBucket: 'iwitness-c14c0.appspot.com',
  messagingSenderId: '671003169029',
  appId: '1:671003169029:web:d3c9e5926461e2f4bca76c',
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore();
app;
