import React from "react";
import Sidebar from "../Sidebar/Sidebar";
import "./Layout.css";

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="layout">
      <Sidebar />
      <div className="layout-content">{children}</div>
    </div>
  );
};

export default Layout;
