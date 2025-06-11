import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // import useNavigate for navigation
import "./CreateQuestion.css";

const CreateQuestion = () => {
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
  const [categories, setCategories] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate(); // hook for navigating

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const res = await fetch("/api/categories", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Failed to fetch categories");
        const data = await res.json();
        setCategories(data);
      } catch (err) {
        setError("خطا در بارگذاری دسته‌بندی‌ها");
      }
    };

    fetchCategories();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    console.log("Form Data Submitted:", formData); // Log the data before sending

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
      if (!res.ok) throw new Error(data.error || "Failed to create question");

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

  // Function to handle "back" navigation
  const handleBack = () => {
    navigate("/dashboard"); // Navigate to the dashboard
  };

  return (
    <div className="question-dashboard">
      <h2>📝 ثبت سوال جدید</h2>
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

        <div className="form-row"><label>درجه سختی:</label>
          <select name="difficulty" value={formData.difficulty} onChange={handleChange}>
            <option value="easy">آسان</option>
            <option value="medium">متوسط</option>
            <option value="hard">سخت</option>
          </select>
        </div>

        <div className="form-row">
          <label>دسته‌بندی:</label>
          <select name="category_id" value={formData.category_id} onChange={handleChange} required>
            <option value="">انتخاب کنید...</option>
            {categories.map((cat) => (
              <option key={cat.category_id} value={cat.category_id}>
                {cat.title}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" className="submit-button">ثبت سوال</button>
      </form>

      <button className="back-button" onClick={handleBack}>برگشتن</button> {/* Back button */}
    </div>
  );
};

export default CreateQuestion;