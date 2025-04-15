import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx"; // Make sure this points to the right component
import "./index.css"; // Optional: If you have any global CSS

const root = ReactDOM.createRoot(document.getElementById("app"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
