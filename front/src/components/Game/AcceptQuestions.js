import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './AcceptQuestions.css';

const AcceptQuestions = () => {
    const navigate = useNavigate();
    const token = localStorage.getItem('access_token');
    const [questions, setQuestions] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUnconfirmedQuestions = async () => {
            try {
                const response = await axios.get('/api/questions/unconfirmed', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setQuestions(response.data);
            } catch (error) {
                setError(error.response?.data?.error || 'Failed to fetch questions');
            } finally {
                setLoading(false);
            }
        };

        fetchUnconfirmedQuestions();
    }, [token]);

    const handleAccept = async (questionId, confirmed) => {
        try {
            await axios.post(`/api/questions/${questionId}/accept`, {
                confirmed: confirmed
            }, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            // Remove question from the list after accept/reject
            setQuestions(prevQuestions =>
                prevQuestions.filter(question => question.question_id !== questionId)
            );
        } catch (error) {
            setError(error.response?.data?.error || 'Failed to accept question');
        }
    };

    if (loading) return <div>در حال بارگذاری...</div>;

    return (
        <div className="accept-questions-container">
            <h2>مدیریت سوالات تایید نشده</h2>
            {error && <div className="error-message">{error}</div>}
            <div className="questions-list">
                {questions.length === 0 ? (
                    <p>هیچ سوال تایید نشده‌ای وجود ندارد</p>
                ) : (
                    questions.map((question) => (
                        <div key={question.question_id} className="question-card">
                            <h3>{question.question_text}</h3>
                            <p><strong>دسته‌بندی:</strong> {question.category_title}</p>
                            <p><strong>گزینه‌ها:</strong></p>
                            <ul>
                                <li>A: {question.option_a}</li>
                                <li>B: {question.option_b}</li>
                                <li>C: {question.option_c}</li>
                                <li>D: {question.option_d}</li>
                            </ul>
                            <p><strong>گزینه درست:</strong> {question.right_option}</p>
                            <p><strong>نویسنده:</strong> {question.author_username}</p>
                            <div className="buttons">
                                <button
                                    onClick={() => handleAccept(question.question_id, true)}
                                    className="accept-button"
                                >
                                    تایید
                                </button>
                                <button
                                    onClick={() => handleAccept(question.question_id, false)}
                                    className="reject-button"
                                >
                                    رد
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default AcceptQuestions;