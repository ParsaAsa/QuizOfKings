import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../Dashboard/Dashboard.css'; // reuse dashboard theme

const GameStartOptions = () => {
    const navigate = useNavigate();

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>🎮 شروع بازی</h1>
                </div>
            </header>

            <main className="dashboard-main">
                <div className="welcome-section">
                    <h2>چه کاری می‌خواهید انجام دهید؟</h2>
                </div>

                <div className="game-options">
                    <div className="option-card">
                        <h3>📨 درخواست‌های بازی</h3>
                        <p>درخواست‌های بازی دریافتی یا ارسالی</p>
                        <button className="option-button" onClick={() => navigate('/game/requests')}>
                            مشاهده درخواست‌ها
                        </button>
                    </div>

                    <div className="option-card">
                        <h3>🆕 شروع بازی جدید</h3>
                        <p>با بازیکن جدیدی بازی را آغاز کنید</p>
                        <button className="option-button" onClick={() => navigate('/game/new')}>
                            شروع بازی جدید
                        </button>
                    </div>

                    <div className="option-card">
                        <h3>🔄 ادامه بازی‌های قبلی</h3>
                        <p>مسابقات نیمه‌تمام خود را ادامه دهید</p>
                        <button className="option-button" onClick={() => navigate('/game/active')}>
                            ادامه بازی
                        </button>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default GameStartOptions;
