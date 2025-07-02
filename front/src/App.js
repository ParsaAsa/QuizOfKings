import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import Dashboard from './components/Dashboard/Dashboard';
import MatchRequests from './components/Game/MatchRequests';
import CategorySelection from './components/Game/CategorySelection';
import QuestionRound from './components/Game/QuestionRound';
import { authService } from './services/auth';
import GameStartOptions from './components/Game/GameStartOptions';
import './App.css';
import NewMatchRequest from './components/Game/NewMatchRequest';
import OngoingMatches from './components/Game/OngoingMatches';
import MatchPage from './components/Game/MatchPage';
import PlayerStats from './components/Game/PlayerStats'
import CreateQuestion from './components/Game/CreateQuestion';
import TopPlayers from './components/Game/TopPlayers';
import AcceptQuestions from './components/Game/AcceptQuestions';
import ChangeRole from './components/Game/ChangeRole';
// Protected Route Component
const ProtectedRoute = ({ children }) => {
  return authService.isAuthenticated() ? children : <Navigate to="/login" />;
};

// Public Route Component (redirect if already logged in)
const PublicRoute = ({ children }) => {
  return !authService.isAuthenticated() ? children : <Navigate to="/dashboard" />;
};

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public Routes */}
          <Route
            path="/login"
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            }
          />
          <Route
            path="/signup"
            element={
              <PublicRoute>
                <Signup />
              </PublicRoute>
            }
          />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/game/requests"
            element={
              <ProtectedRoute>
                <MatchRequests />
              </ProtectedRoute>
            }
          />

          <Route
            path="/game/category/:matchId/:roundNumber"
            element={
              <ProtectedRoute>
                <CategorySelection />
              </ProtectedRoute>
            }
          />

          <Route
            path="/game/play/:matchId/:roundNumber"
            element={
              <ProtectedRoute>
                <QuestionRound />
              </ProtectedRoute>
            }
          />


          <Route
            path="/leaderboard"
            element={
              <ProtectedRoute>
                <TopPlayers />
              </ProtectedRoute>
            }
          />

          {/* Default Routes */}
          <Route
            path="/"
            element={
              authService.isAuthenticated() ?
                <Navigate to="/dashboard" /> :
                <Navigate to="/login" />
            }
          />
          <Route path="/game/new" element={<ProtectedRoute>
            <NewMatchRequest />
          </ProtectedRoute>} />

          <Route path="/game/active" element={<ProtectedRoute>
            <OngoingMatches />
          </ProtectedRoute>} />

          <Route path="/game/page/:matchId" element={<MatchPage />} />
          <Route
            path="/question_accepting"
            element={
              <ProtectedRoute>
                <AcceptQuestions />
              </ProtectedRoute>
            }
          />
          <Route
            path="/role_update"
            element={
              <ProtectedRoute>
                <ChangeRole />
              </ProtectedRoute>
            }
          />

          <Route path="/game/page/:matchId/round_number" element={<QuestionRound />} />
          <Route path="/game/page/:matchId/roundNumber" element={<CategorySelection />} />
          <Route path="/player_stats/:username" element={<PlayerStats />} />
          <Route path="/game" element={<GameStartOptions />} />
          <Route path="/question" element={<CreateQuestion />} />
          {/* 404 Route */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;