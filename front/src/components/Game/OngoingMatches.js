import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './OngoingMatches.css'; // you can style like dashboard or customize
import { useNavigate } from 'react-router-dom';

const OngoingMatches = () => {
    const navigate = useNavigate();
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const handleGoToGameOptions = () => {
        navigate('/game');
    }
    useEffect(() => {
        const fetchOngoingMatches = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const response = await axios.get('/api/matches/ongoing', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setMatches(response.data);
            } catch (err) {
                console.error('Error fetching ongoing matches:', err);
                setError('دریافت اطلاعات با مشکل مواجه شد.');
            } finally {
                setLoading(false);
            }
        };

        fetchOngoingMatches();
    }, []);

    const handleEnterMatch = (matchId) => {
        navigate(`/game/page/${matchId}`);
    };


    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>🔄 بازی‌های در حال انجام</h1>
                    <button onClick={handleGoToGameOptions} className="logout-button">بازگشت</button>
                </div>
            </header>

            <main className="dashboard-main">
                {loading ? (
                    <p className="loading-text">در حال بارگذاری...</p>
                ) : error ? (
                    <p className="error-text">{error}</p>
                ) : matches.length === 0 ? (
                    <p className="empty-text">بازی در حال انجامی وجود ندارد.</p>
                ) : (
                    <div className="game-options">
                        {matches.map((match) => (
                            <div className="option-card" key={match.match_id}>
                                <h3>شناسه بازی: {match.match_id}</h3>
                                <p>از طرف: {match.player1_username}</p>
                                <button
                                    className="option-button"
                                    onClick={() => handleEnterMatch(match.match_id)}
                                >
                                    ورود به بازی
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
};

export default OngoingMatches;
