import React, { useEffect, useState } from 'react';
import "./TopPlayers.css";
const TopPlayers = () => {
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTopPlayers = async () => {
            setLoading(true);
            setError(null);
            try {
                const token = localStorage.getItem('access_token');
                const res = await fetch('/api/players/top_winners', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                if (!res.ok) throw new Error('خطا در بارگذاری بازیکنان برتر');
                const data = await res.json();
                setPlayers(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchTopPlayers();
    }, []);

    if (loading) return <div>در حال بارگذاری...</div>;
    if (error) return <div>خطا: {error}</div>;

    return (
        <div className="top-players-container">
            <h2>🏅 بازیکنان برتر</h2>
            <table>
                <thead>
                    <tr>
                        <th>نام کاربری</th>
                        <th>نقش</th>
                        <th>تعداد برد</th>
                    </tr>
                </thead>
                <tbody>
                    {players.map(player => (
                        <tr key={player.player_id}>
                            <td>{player.username}</td>
                            <td>{player.player_role}</td>
                            <td>{player.wins}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TopPlayers;