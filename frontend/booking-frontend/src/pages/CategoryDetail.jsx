import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiGet } from "../api";
import ServiceCard from "../components/ServiceCard";

function CategoryDetail() {
    const { categoryId } = useParams();
    const [category, setCategory] = useState(null);
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function load() {
            try {
                setLoading(true);
                const [c, s] = await Promise.all([
                    apiGet(`/categories/${categoryId}`),
                    apiGet(`/categories/${categoryId}/services`),
                ]);
                setCategory(c);
                setServices(s);
            } catch (err) {
                setError(err.message || "Failed to load category");
            } finally {
                setLoading(false);
            }
        }
        load();
    }, [categoryId]);

    if (loading) return <div className="page"><p>Loading...</p></div>;
    if (error) return <div className="page"><p className="error">{error}</p></div>;
    if (!category) return <div className="page"><p>Category not found</p></div>;

    return (
        <div className="page">
            <header className="page-header">
                <h1>{category.name}</h1>
                <p>{category.description}</p>
            </header>

            <section className="section">
                <h2>Services in this category</h2>
                {services.length === 0 && <p>No services.</p>}
                <div className="grid">
                    {services.map((s) => (
                        <ServiceCard key={s.id} service={s} />
                    ))}
                </div>
            </section>
        </div>
    );
}

export default CategoryDetail;
