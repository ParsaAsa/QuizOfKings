import React, { useEffect, useState } from "react";
import { useParams } from 'react-router-dom';
import "./PlayerStats.css";

export default function PlayerStatsDashboard() {
    const { username } = useParams();  // ✅ Get username from URL
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchStats() {
            setLoading(true);
            setError(null);
            try {
                const token = localStorage.getItem("access_token"); // assuming JWT stored here
                const res = await fetch(`/api/player_stats/${username}`, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                if (!res.ok) {
                    throw new Error("Failed to fetch player stats");
                }
                const data = await res.json();
                setStats(data);
            } catch (e) {
                setError(e.message);
            } finally {
                setLoading(false);
            }
        }
        fetchStats();
    }, [username]);

    if (loading) return <div className="dashboard">در حال بارگذاری آمار...</div>;
    if (error) return <div className="dashboard error">خطا: {error}</div>;

    return (
        <div className="dashboard">
            <h2>آمار بازیکن: {username}</h2>
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
        </div>
    );
}