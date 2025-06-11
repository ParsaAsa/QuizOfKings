import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import "./QuestionRound.css";

const QuestionRound = () => {
    const { matchId, roundNumber } = useParams();
    const navigate = useNavigate();
    const token = localStorage.getItem("access_token");

    const [questions, setQuestions] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [correctAnswer, setCorrectAnswer] = useState(null);
    const [timer, setTimer] = useState(10);
    const [isAnswered, setIsAnswered] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!matchId || !roundNumber) {
            setError("شناسه بازی یا شماره دور نامعتبر است.");
            setLoading(false);
            return;
        }

        const fetchQuestions = async () => {
            try {
                const res = await axios.get(`/api/questions/${matchId}/${roundNumber}`, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                console.log("API response:", res.data);

                // Adjust here if your API returns {questions: [...]} instead of array
                const questionsData = Array.isArray(res.data) ? res.data : res.data.questions;
                if (!questionsData || !questionsData.length) {
                    setError("سوالی یافت نشد.");
                } else {
                    setQuestions(questionsData);
                }
            } catch (err) {
                console.error(err);
                setError("خطا در دریافت سوالات.");
            } finally {
                setLoading(false);
            }
        };

        fetchQuestions();
    }, [matchId, roundNumber, token]);

    useEffect(() => {
        if (questions.length === 0 || isAnswered) return;

        if (timer <= 0) {
            submitAnswer(["A", "B", "C", "D"][Math.floor(Math.random() * 4)]);
            return;
        }

        const interval = setInterval(() => {
            setTimer((t) => t - 1);
        }, 1000);

        return () => clearInterval(interval);
    }, [timer, isAnswered, questions]);

    const submitAnswer = async (answer) => {
        if (isAnswered) return;

        const question = questions[currentIndex];
        setSelectedAnswer(answer);
        setCorrectAnswer(question.right_option);
        setIsAnswered(true);

        try {
            await axios.post(
                "/api/player_answers/submit",
                {
                    match_id: parseInt(matchId),
                    round_number: parseInt(roundNumber),
                    question_number: question.question_number,
                    answer,
                },
                { headers: { Authorization: `Bearer ${token}` } }
            );
        } catch (err) {
            console.error("خطا در ارسال پاسخ:", err);
        }

        setTimeout(() => {
            if (currentIndex < questions.length - 1) {
                setCurrentIndex(currentIndex + 1);
                setSelectedAnswer(null);
                setCorrectAnswer(null);
                setIsAnswered(false);
                setTimer(10);
            } else {
                navigate(`/game/page/${matchId}`);
            }
        }, 2000);
    };

    if (loading) return <p className="loading-text">در حال بارگذاری سوالات...</p>;
    if (error) return <p className="error-text">{error}</p>;
    if (!questions.length) return <p className="error-text">سوالی یافت نشد.</p>;

    const currentQ = questions[currentIndex];
    // console.log("Current Question Data:", currentQ); // optional debug

    return (
        <div className="question-container">
            <h2>سوال {currentIndex + 1} / {questions.length}</h2>
            <p className="question-text">{currentQ.question_text}</p>
            <p>⏱️ زمان باقی‌مانده: {timer} ثانیه</p>

            <div className="options">
                {["A", "B", "C", "D"].map((opt) => {
                    // support both uppercase and lowercase keys
                    const value = currentQ[`option_${opt}`] || currentQ[`option_${opt.toLowerCase()}`];
                    if (!value) return null;

                    let bgColor = "#eee";
                    if (isAnswered) {
                        if (opt === correctAnswer) bgColor = "green";
                        else if (opt === selectedAnswer) bgColor = "red";
                        else bgColor = "#ccc";
                    }

                    return (
                        <div
                            key={opt}
                            className="option"
                            style={{
                                backgroundColor: bgColor,
                                color: isAnswered ? "white" : "black",
                                cursor: isAnswered ? "default" : "pointer",
                            }}
                            onClick={() => !isAnswered && submitAnswer(opt)}
                        >
                            <strong>{opt}:</strong> {value}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default QuestionRound;