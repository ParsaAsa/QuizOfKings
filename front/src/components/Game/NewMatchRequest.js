import React, { useState } from 'react';
import axios from 'axios';
import './NewMatchRequest.css'; // Optional: style as needed
import { useNavigate } from 'react-router-dom';

const NewMatchRequest = () => {
    const [player2Username, setPlayer2Username] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleGoToGameOptions = () => {
        navigate('/game')
    }
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');

        const token = localStorage.getItem('access_token');

        try {
            const response = await axios.post(
                '/api/matches/request',
                { player2_username: player2Username },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );

            setSuccess(`درخواست با موفقیت ارسال شد! شناسه بازی: ${response.data.match_id}`);
            setPlayer2Username('');
        } catch (err) {
            console.error('Match request failed:', err);
            if (err.response?.data?.error) {
                setError(err.response.data.error);
            } else {
                setError('مشکلی در ارسال درخواست رخ داد.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>🆕 شروع بازی جدید</h1>
                    <button onClick={handleGoToGameOptions} className="logout-button">بازگشت</button>
                </div>
            </header>

            <main className="dashboard-main">
                <form className="new-match-form" onSubmit={handleSubmit}>
                    {error && <p className="error-text">{error}</p>}
                    {success && <p className="success-text">{success}</p>}

                    <div className="form-group">
                        <input
                            type="text"
                            placeholder="نام کاربری بازیکن مقابل"
                            value={player2Username}
                            onChange={(e) => setPlayer2Username(e.target.value)}
                            required
                            disabled={loading}
                        />
                    </div>

                    <button className="auth-button" type="submit" disabled={loading}>
                        {loading ? 'در حال ارسال...' : 'ارسال درخواست'}
                    </button>
                </form>
            </main>
        </div>
    );
};

export default NewMatchRequest;
