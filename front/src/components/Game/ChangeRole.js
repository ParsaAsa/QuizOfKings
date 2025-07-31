import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChangeRole.css';          // optional extra styling

const ChangeRole = () => {
    const navigate = useNavigate();
    const token = localStorage.getItem('access_token');

    const [targetUsername, setTargetUsername] = useState('');
    const [newRole, setNewRole] = useState('admin');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');
        setError('');

        try {
            const res = await fetch(`/api/players/${targetUsername}/role`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ player_role: newRole }),
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'خطا در تغییر نقش');

            setMessage(data.message);
            setTargetUsername('');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>👤 تغییر نقش بازیکن</h1>
                    <button onClick={() => navigate('/dashboard')} className="logout-button">
                        بازگشت
                    </button>
                </div>
            </header>

            <main className="dashboard-main">
                <div className="option-card" style={{ maxWidth: '450px', margin: '0 auto' }}>
                    <h3>تعیین نقش جدید</h3>
                    <p>نام کاربری بازیکن را وارد کرده و نقش جدید را انتخاب کنید.</p>

                    {message && <div className="success-message">{message}</div>}
                    {error && <div className="error-message">{error}</div>}

                    <form onSubmit={handleSubmit} className="role-form">
                        <input
                            type="text"
                            placeholder="نام کاربری"
                            value={targetUsername}
                            onChange={(e) => setTargetUsername(e.target.value)}
                            required
                            disabled={loading}
                        />

                        <select
                            value={newRole}
                            onChange={(e) => setNewRole(e.target.value)}
                            disabled={loading}
                        >
                            <option value="admin">admin</option>
                            <option value="manager">manager</option>
                            <option value="normal">normal</option>
                        </select>

                        <button type="submit" className="option-button" disabled={loading}>
                            {loading ? 'در حال ثبت...' : 'ذخیره تغییر'}
                        </button>
                    </form>
                </div>
            </main>
        </div>
    );
};

export default ChangeRole;
