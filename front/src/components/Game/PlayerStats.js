import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./PlayerStats.css";

export default function PlayerStatsDashboard() {
    const navigate = useNavigate();
    const { username } = useParams();            // username from /player_stats/:username
    const [stats, setStats] = useState(null);    // player statistics
    const [matches, setMatches] = useState([]);  // last 3 finished matches
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const handleGoToDashboard = () => {
        navigate('/dashboard');
    }

    /** Fetch player stats */
    const fetchStats = async (token) => {
        const res = await fetch(`/api/player_stats/${username}`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Failed to fetch player stats");
        return res.json();
    };

    /** Fetch last done matches */
    const fetchMatches = async (token) => {
        const res = await fetch("/api/matches/done", {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Failed to fetch matches");
        const all = await res.json();
        return all.slice(0, 3); // only last 3
    };

    useEffect(() => {
        async function loadData() {
            setLoading(true);
            setError(null);

            const token = localStorage.getItem("access_token");
            if (!token) {
                setError("توکن یافت نشد، لطفاً دوباره وارد شوید.");
                setLoading(false);
                return;
            }

            try {
                const [statsData, matchesData] = await Promise.all([
                    fetchStats(token),
                    fetchMatches(token),
                ]);
                setStats(statsData);
                setMatches(matchesData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        loadData();
    }, [username]);

    if (loading) return <div className="dashboard">در حال بارگذاری آمار...</div>;
    if (error) return <div className="dashboard error">خطا: {error}</div>;

    /** Helper to label result */
    const matchResult = (m) => {
        if (!stats) return "-";
        if (m.winner_id == null) return "مساوی";
        return m.winner_id === stats.player_id ? "برد" : "باخت";
    };

    /** Helper to get opponent username */
    const opponentName = (m) =>
        m.player1_username === username ? m.player2_username : m.player1_username;

    return (
        <div className="dashboard">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>📊 آمار بازیکن</h1>
                    <button onClick={handleGoToDashboard} className="logout-button">برگشت به داشبورد</button>
                </div>
            </header>

            <h2>آمار بازیکن: {username}</h2>

            {/* Stats cards */}
            <div className="stats-cards">
                <div className="card">
                    <h3>تعداد بازی‌ها</h3>
                    <p>{stats.total_matches}</p>
                </div>
                <div className="card">
                    <h3>تعداد بردها</h3>
                    <p>{stats.wins}</p>
                </div>
                <div className="card">
                    <h3>درصد دقت</h3>
                    <p>{(stats.accuracy * 100).toFixed(2)}%</p>
                </div>
            </div>

            {/* Last 3 finished matches */}
            <h3 style={{ marginTop: "2rem" }}>آخرین ۳ مسابقه پایان‌یافته</h3>
            {matches.length === 0 ? (
                <p>هنوز هیچ مسابقه‌ای به پایان نرسیده است.</p>
            ) : (
                <ul className="last-matches">
                    {matches.map((m) => (
                        <li key={m.match_id} className="match-row">
                            <span>شناسه: {m.match_id}</span>
                            <span>حریف: {opponentName(m)}</span>
                            <span>نتیجه: {matchResult(m)}</span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
