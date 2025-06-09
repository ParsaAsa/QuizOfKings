import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './MatchRequests.css';

const MatchRequests = () => {
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [actionLoading, setActionLoading] = useState(false);

    const token = localStorage.getItem('access_token');

    // Fetch pending requests
    useEffect(() => {
        const fetchRequests = async () => {
            try {
                const response = await axios.get('/api/matches/pending_requests', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setRequests(response.data);
            } catch (error) {
                console.error('خطا در دریافت درخواست‌ها:', error);
                setError('دریافت اطلاعات با مشکل مواجه شد.');
            } finally {
                setLoading(false);
            }
        };

        fetchRequests();
    }, [token]);

    // Accept or reject match request
    const handleMatchDecision = async (matchId, accept) => {
        setActionLoading(true);
        setError('');
        try {
            const response = await axios.post(
                '/api/matches/accept',
                { match_id: matchId, accept: accept },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );
            // Optionally show success message or remove the handled request from list
            setRequests((prev) => prev.filter((req) => req.match_id !== matchId));
        } catch (error) {
            console.error('خطا در ارسال پاسخ درخواست:', error);
            setError('ارسال پاسخ درخواست با مشکل مواجه شد.');
        } finally {
            setActionLoading(false);
        }
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>🎮 درخواست‌های بازی</h1>
                </div>
            </header>

            <main className="dashboard-main">
                {loading ? (
                    <p className="loading-text">در حال بارگذاری...</p>
                ) : error ? (
                    <p className="error-text">{error}</p>
                ) : requests.length === 0 ? (
                    <p className="empty-text">درخواستی یافت نشد.</p>
                ) : (
                    <div className="game-options">
                        {requests.map((req) => (
                            <div className="option-card" key={req.match_id}>
                                <h3>از طرف: {req.player1_username}</h3>
                                <p>شناسه بازی: {req.match_id}</p>
                                <button
                                    className="option-button accept-button"
                                    onClick={() => handleMatchDecision(req.match_id, true)}
                                    disabled={actionLoading}
                                >
                                    پیوستن به بازی
                                </button>
                                <button
                                    className="option-button reject-button"
                                    onClick={() => handleMatchDecision(req.match_id, false)}
                                    disabled={actionLoading}
                                >
                                    رد کردن درخواست
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
};

export default MatchRequests;
