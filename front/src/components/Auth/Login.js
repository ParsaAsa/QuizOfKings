import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../../services/auth';
import './Auth.css';

const Login = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const result = await authService.login(formData.username, formData.password);

        if (result.success) {
            localStorage.setItem('username', formData.username);
            navigate('/dashboard/');
        }
        else {
            setError(result.error);
        }

        setLoading(false);
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>🏆 Quiz of Kings</h1>
                    <h2>ورود به بازی</h2>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    {error && <div className="error-message">{error}</div>}

                    <div className="form-group">
                        <input
                            type="text"
                            name="username"
                            placeholder="نام کاربری"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            disabled={loading}
                        />
                    </div>

                    <div className="form-group">
                        <input
                            type="password"
                            name="password"
                            placeholder="رمز عبور"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            disabled={loading}
                        />
                    </div>

                    <button type="submit" className="auth-button" disabled={loading}>
                        {loading ? 'در حال ورود...' : 'ورود'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>
                        حساب کاربری ندارید؟{' '}
                        <Link to="/signup" className="auth-link">
                            ثبت نام کنید
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;