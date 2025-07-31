import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import "./MatchPage.css";

const MatchPage = () => {
    const { matchId } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [matchStatus, setMatchStatus] = useState(null);
    const [currentUser, setCurrentUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (!token) {
            setError("لطفا وارد شوید.");
            setLoading(false);
            return;
        }

        try {
            const decoded = jwtDecode(token);
            setCurrentUser(decoded.sub || decoded.identity || decoded.username);
        } catch {
            setError("توکن نامعتبر است.");
            setLoading(false);
            return;
        }

        const fetchStatus = async () => {
            try {
                const response = await axios.get(`/api/matches/${matchId}/status`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setMatchStatus(response.data);
            } catch {
                setError("خطا در دریافت وضعیت بازی.");
            } finally {
                setLoading(false);
            }
        };

        fetchStatus();
    }, [matchId]);

    if (loading) return <div className="loading-text">در حال بارگذاری...</div>;
    if (error) return <div className="error-text">{error}</div>;
    if (!matchStatus) return <div className="error-text">وضعیتی برای این بازی یافت نشد.</div>;

    const {
        round_number,
        current_turn,  // now this is username
        category_select_time,
        score,
        player1_id,
        player2_id,
        player1_username,
        player2_username,
    } = matchStatus;

    const player1Score = score[player1_id] ?? 0;
    const player2Score = score[player2_id] ?? 0;

    const isMyTurn = currentUser === current_turn;  // compare username directly

    const handleCategorySelect = () => {
        navigate(`/game/category/${matchId}/${round_number}`);
    };

    const handlePlayTurn = () => {
        navigate(`/game/play/${matchId}/${round_number}`);
    };

    return (
        <div className="match-container">
            <h1>وضعیت بازی شماره {matchId}</h1>
            <div className="scores">
                <div>
                    {player1_username}: {player1Score}
                </div>
                <div>
                    {player2_username}: {player2Score}
                </div>
            </div>
            <p>شماره دور: {round_number}</p>

            {isMyTurn ? (
                category_select_time ? (
                    <button className="btn btn-green" onClick={handleCategorySelect}>
                        انتخاب موضوع
                    </button>
                ) : (
                    <button className="btn btn-blue" onClick={handlePlayTurn}>
                        بازی کردن نوبت
                    </button>
                )
            ) : (
                <p>منتظر نوبت خود باشید...</p>
            )}

            <button className="btn btn-back" onClick={() => navigate('/game/active')}>
                بازگشت
            </button>
        </div>
    );
};

export default MatchPage;
