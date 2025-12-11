import React from "react";

function RatingStars({ rating, count }) {
    if (!rating) return null;
    const rounded = Math.round(rating * 10) / 10;

    return (
        <div className="rating">
            <span className="rating-value">{rounded}</span>
            <span className="rating-stars">★</span>
            {typeof count === "number" && (
                <span className="rating-count">({count})</span>
            )}
        </div>
    );
}

export default RatingStars;
