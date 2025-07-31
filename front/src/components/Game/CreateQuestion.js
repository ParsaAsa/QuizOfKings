import React, { useState, useEffect } from "react";
import "./CreateQuestion.css";
import { useNavigate } from 'react-router-dom';

const CreateQuestion = () => {

    const navigate = useNavigate();

    const handleGoToDashboard = () => {
        navigate('/dashboard');
    }
    const [formData, setFormData] = useState({
        question_text: "",
        option_A: "",
        option_B: "",
        option_C: "",
        option_D: "",
        right_option: "A",
        difficulty: "easy",
        category_id: "",
    });
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        async function fetchCategories() {
            try {
                const token = localStorage.getItem("access_token");
                const res = await fetch("/api/categories", {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.error || "Failed to fetch categories");
                }
                setCategories(data);  // Assuming API returns an array of categories
            } catch (err) {
                setError(err.message);
            }
        }
        fetchCategories();
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage("");
        setError("");

        try {
            const token = localStorage.getItem("access_token");
            const res = await fetch("/api/questions", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
            });

            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.error || "Failed to create question");
            }

            setMessage("سوال با موفقیت ثبت شد!");
            setFormData({
                question_text: "",
                option_A: "",
                option_B: "",
                option_C: "",
                option_D: "",
                right_option: "A",
                difficulty: "easy",
                category_id: "",
            });
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="question-dashboard">
            <header className="dashboard-header">
                <div className="header-content">
                    <h1>❓ ثبت سوال جدید</h1>
                    <button onClick={handleGoToDashboard} className="logout-button">برگشت به داشبورد</button>
                </div>
            </header>

            <form onSubmit={handleSubmit} className="question-form">
                {message && <div className="success-message">{message}</div>}
                {error && <div className="error-message">{error}</div>}

                <textarea
                    name="question_text"
                    placeholder="متن سوال"
                    value={formData.question_text}
                    onChange={handleChange}
                    required
                />

                {["A", "B", "C", "D"].map((opt) => (
                    <input
                        key={opt}
                        type="text"
                        name={`option_${opt}`}
                        placeholder={`گزینه ${opt}`}
                        value={formData[`option_${opt}`]}
                        onChange={handleChange}
                        required
                    />
                ))}

                <div className="form-row">
                    <label>گزینه صحیح:</label>
                    <select name="right_option" value={formData.right_option} onChange={handleChange}>
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                    </select>
                </div>

                <div className="form-row">
                    <label>درجه سختی:</label>
                    <select name="difficulty" value={formData.difficulty} onChange={handleChange}>
                        <option value="easy">آسان</option>
                        <option value="medium">متوسط</option>
                        <option value="hard">سخت</option>
                    </select>
                </div>

                <div className="form-row">
                    <label>دسته‌بندی سوال:</label>
                    <select
                        name="category_id"
                        value={formData.category_id}
                        onChange={handleChange}
                        required
                    >
                        <option value="">انتخاب دسته‌بندی</option>
                        {categories.map((category) => (
                            <option key={category.category_id} value={category.category_id}>
                                {category.title}
                            </option>
                        ))}
                    </select>
                </div>

                <button type="submit" className="submit-button">ثبت سوال</button>
            </form>
        </div>
    );
};

export default CreateQuestion;