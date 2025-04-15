import React from "react";
import { Link } from "react-router-dom";
import "./Dashboard.css";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

const chartData = {
  labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"],
  datasets: [
    {
      label: "Sales ($)",
      data: [1200, 1500, 1300, 1600, 2000, 1700, 1800],
      fill: false,
      borderColor: "#007bff",
      tension: 0.1,
    },
  ],
};

const Dashboard = () => {
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard Overview</h2>
        <p>Quickly see your store's performance.</p>
      </div>

      <div className="dashboard-cards">
        <div className="card">
          <h3>Total Sales</h3>
          <p>$12,500</p>
        </div>
        <div className="card">
          <h3>Total Products</h3>
          <p>150</p>
        </div>
        <div className="card">
          <h3>Inventory Status</h3>
          <p>80% Stocked</p>
        </div>
      </div>

      <div className="chart-section">
        <h3>Sales Overview (Last 7 Days)</h3>
        {/* Use a chart library like Chart.js or Recharts here */}
        <div className="chart">
          {/* Placeholder for the chart */}
          <p>Chart Will Be Here (Use a charting library like Chart.js)</p>
        </div>
      </div>

      <div className="recent-activity">
        <h3>Recent Sales</h3>
        <ul>
          <li>
            <Link to="/sales">Sale #1: $200</Link>
          </li>
          <li>
            <Link to="/sales">Sale #2: $350</Link>
          </li>
          <li>
            <Link to="/sales">Sale #3: $450</Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
