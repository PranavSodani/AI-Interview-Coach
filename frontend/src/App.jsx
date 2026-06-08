import { BrowserRouter, Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";

import InterviewPage from "./pages/InterviewPage";

import AnalyticsPage from "./pages/AnalyticsPage";

import HistoryPage from "./pages/HistoryPage";

import Navbar from "./components/Navbar";

import LoginPage from "./pages/LoginPage";

import DashboardPage from "./pages/DashboardPage";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<HomePage />} />

        <Route
          path="/interview"
          element={
            <ProtectedRoute>
              <InterviewPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/analytics"
          element={
            <ProtectedRoute>
              <AnalyticsPage />
            </ProtectedRoute>
          }
        />

        <Route path="/login" element={<LoginPage />} />

        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <HistoryPage />
            </ProtectedRoute>
          }
        />

        <Route path="/dashboard" element={<DashboardPage />} />

        <Route path="/" element={<LoginPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
