import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "./CategorySelection.css";

const CategorySelection = () => {
  const { matchId, roundNumber } = useParams();
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [settingCategory, setSettingCategory] = useState(false);
  const [categoryAlreadySet, setCategoryAlreadySet] = useState(false);

  useEffect(() => {
    const fetchStatusAndCategories = async () => {
      try {
        const token = localStorage.getItem("access_token");

        // First, check if category can be selected
        const statusRes = await axios.get(`/api/matches/${matchId}/status`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const { category_select_time } = statusRes.data;

        if (!category_select_time) {
          setCategoryAlreadySet(true);
          setError("دسترسی به انتخاب موضوع ندارید یا قبلاً انتخاب شده است.");
          return;
        }

        // Then fetch random categories
        const catsRes = await axios.get(`/api/categories/random/${matchId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setCategories(catsRes.data);
      } catch (err) {
        setError("بارگذاری موضوعات با خطا مواجه شد.");
      } finally {
        setLoading(false);
      }
    };

    fetchStatusAndCategories();
  }, [matchId]);

  const handleCategoryClick = async (category) => {
    if (categoryAlreadySet || settingCategory) return;

    setSettingCategory(true);
    setError("");

    try {
      const token = localStorage.getItem("access_token");

      await axios.put(
        `/api/rounds/${matchId}/${roundNumber}/category`,
        { category_id: category.category_id },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      navigate(`/game/page/${matchId}`, {
        state: { category },
      });
    } catch (err) {
      setError("ثبت موضوع با خطا مواجه شد.");
    } finally {
      setSettingCategory(false);
    }
  };

  if (loading) return <div className="loading-text">در حال بارگذاری موضوعات...</div>;
  if (error) return <div className="error-text">{error}</div>;

  return (
    <div className="category-selection-container">
      <h2>موضوع را انتخاب کنید</h2>
      <div className="category-buttons">
        {categories.map((cat) => (
          <button
            key={cat.category_id}
            className="category-btn"
            onClick={() => handleCategoryClick(cat)}
            disabled={settingCategory || categoryAlreadySet}
          >
            {cat.title}
          </button>
        ))}
      </div>
      {settingCategory && <div className="loading-text">در حال ثبت موضوع...</div>}
    </div>
  );
};

export default CategorySelection;