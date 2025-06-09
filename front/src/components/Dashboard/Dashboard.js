import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { authService } from '../../services/auth';
import './Dashboard.css';

const Dashboard = () => {
    const [matches, setMatches] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    useEffect(() => {
        const fetchOngoingMatches = async () => {
            const token = localStorage.getItem('access_token');
            console.log('Token from localStorage:', token); // Debug log

            if (!token) {
                setError('لطفا وارد شوید.');
                setLoading(false);
                return;
            }

            try {
                const response = await axios.get('http://localhost:5000/api/matches/ongoing', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setMatches(response.data);
                setError('');
            } catch (err) {
                console.error('Error fetching ongoing matches:', err);
                setError('دریافت اطلاعات با مشکل مواجه شد.');
            } finally {
                setLoading(false);
            }
        };

        fetchOngoingMatches();
    }, []);

    const handleLogout = () => {
        authService.logout();
        navigate('/login');
    };

    const goToMatch = (match) => {
        if (match.match_state === 'not_started') {
            navigate('/game/requests');
        } else if (match.match_state === 'on_going') {
            navigate(`/game/page/${match.match_id}`); // Navigate to your MatchPage route
        } else if (match.match_state === 'done') {
            navigate('/game/history');
        }
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
                        <button className="option-button" onClick={() => navigate('/game/history')}>مشاهده آمار</button>
                    </div>

                    <div className="option-card">
                        <h3>❓ مدیریت سوالات</h3>
                        <p>مشاهده و مدیریت سوالات</p>
                        <button className="option-button" onClick={() => navigate('/admin/questions')}>سوالات</button>
                    </div>

                    <div className="option-card">
                        <h3>🏆 رتبه‌بندی</h3>
                        <p>جدول رتبه‌بندی بازیکنان</p>
                        <button className="option-button" onClick={() => navigate('/leaderboard')}>رتبه‌بندی</button>
                    </div>
                </div>

                <div className="match-list" style={{ marginTop: '3rem' }}>
                    <h2 style={{ color: 'white', marginBottom: '1rem' }}>مسابقات شما</h2>

                    {loading ? (
                        <p style={{ color: 'white' }}>در حال بارگذاری...</p>
                    ) : error ? (
                        <p style={{ color: 'red' }}>{error}</p>
                    ) : matches.length === 0 ? (
                        <p style={{ color: 'white' }}>هیچ مسابقه‌ای یافت نشد.</p>
                    ) : (
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            {matches.map((match) => (
                                <li
                                    key={match.match_id}
                                    className="match-item"
                                    onClick={() => goToMatch(match)}
                                    style={{ cursor: 'pointer' }}
                                >
                                    <div>
                                        <strong>بازیکن مقابل:</strong> {match.opponent_username} <br />
                                        <strong>وضعیت:</strong> {match.match_state}
                                    </div>
                                    <button className="option-button" style={{ marginTop: '0.5rem' }}>
                                        {match.match_state === 'not_started' && 'شروع / پاسخ'}
                                        {match.match_state === 'on_going' && 'ادامه مسابقه'}
                                        {match.match_state === 'done' && 'مشاهده نتیجه'}
                                    </button>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
