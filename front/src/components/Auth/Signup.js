import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../../services/auth';
import './Auth.css';

const Signup = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
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
        setSuccess('');

        if (formData.password !== formData.confirmPassword) {
            setError('رمز عبور و تکرار آن مطابقت ندارند');
            setLoading(false);
            return;
        }

        const result = await authService.register(
            formData.username,
            formData.email,
            formData.password
        );

        if (result.success) {
            setSuccess('ثبت نام با موفقیت انجام شد! در حال انتقال به صفحه ورود...');
            setTimeout(() => {
                navigate('/login');
            }, 2000);
        } else {
            setError(result.error);
        }

        setLoading(false);
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>🏆 Quiz of Kings</h1>
                    <h2>ثبت نام در بازی</h2>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    {error && <div className="error-message">{error}</div>}
                    {success && <div className="success-message">{success}</div>}

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
                            type="email"
                            name="email"
                            placeholder="ایمیل"
                            value={formData.email}
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
                            minLength="6"
                        />
                    </div>

                    <div className="form-group">
                        <input
                            type="password"
                            name="confirmPassword"
                            placeholder="تکرار رمز عبور"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            required
                            disabled={loading}
                        />
                    </div>

                    <button type="submit" className="auth-button" disabled={loading}>
                        {loading ? 'در حال ثبت نام...' : 'ثبت نام'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>
                        قبلاً ثبت نام کرده‌اید؟{' '}
                        <Link to="/login" className="auth-link">
                            وارد شوید
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Signup;