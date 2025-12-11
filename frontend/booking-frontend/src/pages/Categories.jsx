import React, { useEffect, useState } from "react";
import { apiGet } from "../api";
import { Link } from "react-router-dom";

function Categories() {
    const [categories, setCategories] = useState([]);
    const [tree, setTree] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function load() {
            try {
                setLoading(true);
                const [flat, t] = await Promise.all([
                    apiGet("/categories/"),
                    apiGet("/categories/tree"),
                ]);
                setCategories(flat);
                setTree(t);
            } catch (err) {
                setError(err.message || "Failed to load categories");
            } finally {
                setLoading(false);
            }
        }
        load();
    }, []);

    const renderTree = (nodes) => (
        <ul className="tree">
            {nodes.map((c) => (
                <li key={c.id}>
                    <Link to={`/categories/${c.id}`}>{c.name}</Link>
                    {c.children && c.children.length > 0 && renderTree(c.children)}
                </li>
            ))}
        </ul>
    );

    return (
        <div className="page">
            <header className="page-header">
                <h1>Categories</h1>
                <p>Browse services through categories.</p>
            </header>

            {loading && <p>Loading...</p>}
            {error && <p className="error">{error}</p>}

            <section className="section">
                <h2>Category tree</h2>
                {tree.length === 0 ? <p>No categories yet.</p> : renderTree(tree)}
            </section>
        </div>
    );
}

export default Categories;
