import React from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/auth';
import './Dashboard.css';

const Dashboard = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        authService.logout();
        navigate('/login');
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>🏆 Quiz of Kings</h1>
                    <button onClick={handleLogout} className="logout-button">خروج</button>
                </div>
            </header>

            <main className="dashboard-main">
                <div className="welcome-section">
                    <h2>به Quiz of Kings خوش آمدید!</h2>
                    <p>آماده برای شروع بازی هستید؟</p>
                </div>

                <div className="game-options">
                    <div className="option-card">
                        <h3>🎮 بازی</h3>
                        <p>یک بازی شروع کنید یا ادامه دهید</p>
                        <button className="option-button" onClick={() => navigate('/game')}>بازی</button>
                    </div>

                    <div className="option-card">
                        <h3>📊 آمار بازی</h3>
                        <p>نتایج و آمار بازی‌های قبلی</p>
                        <button
                            className="option-button"
                            onClick={() => {
                                const username = localStorage.getItem('username');
                                if (username) {
                                    navigate(`/player_stats/${username}`);
                                }
                            }}
                        >
                            مشاهده آمار
                        </button>
                    </div>

                    <div className="option-card">
                        <h3>❓ مدیریت سوالات</h3>
                        <p>مشاهده و مدیریت سوالات</p>
                        <button className="option-button" onClick={() => navigate('/question')}>سوالات</button>
                    </div>

                    <div className="option-card">
                        <h3>🏆 رتبه‌بندی</h3>
                        <p>جدول رتبه‌بندی بازیکنان</p>
                        <button className="option-button" onClick={() => navigate('/leaderboard')}>رتبه‌بندی</button>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
