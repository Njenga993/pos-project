import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar/Sidebar";
import ProductList from "./components/ProductList/Productlist";
import Sales from "./components/Sales/Sales";
import Reports from "./components/Reports/Reports";
import Inventory from "./components/Inventory/Inventory";
import Dashboard from "./components/Dashboard/Dashboard";
import Layout from "./components/Layout/Layout";
import "./App.css";

const App = () => {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <div className="main-content">
          <Routes>
            <Route
              path="/"
              element={
                <Layout>
                  <ProductList />
                </Layout>
              }
            />
            <Route
              path="/products"
              element={
                <Layout>
                  <ProductList />
                </Layout>
              }
            />
            <Route
              path="/sales"
              element={
                <Layout>
                  <Sales />
                </Layout>
              }
            />
            <Route
              path="/reports"
              element={
                <Layout>
                  <Reports />
                </Layout>
              }
            />
            <Route
              path="/inventory"
              element={
                <Layout>
                  <Inventory />
                </Layout>
              }
            />
            <Route
              path="/dashboard"
              element={
                <Layout>
                  <Dashboard />
                </Layout>
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
