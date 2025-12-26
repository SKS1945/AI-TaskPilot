import React from 'react';
import './Assignments.css';

export function Assignments() {
    const suggestions = [
        { id: 101, task: "Database Schema Design", current: "Unassigned", suggested: "Bob Smith", confidence: 92 },
        { id: 102, task: "Login Page UI", current: "Unassigned", suggested: "Alice Freeman", confidence: 88 },
    ];

    return (
        <div className="assignments-container">
            <div className="ai-banner">
                <div className="ai-icon">🤖</div>
                <div className="ai-text">
                    <h3>AI Assignment Suggestions</h3>
                    <p>TaskPilot found 2 optimal assignments based on team skills and availability.</p>
                </div>
                <button className="apply-btn">Apply All</button>
            </div>

            <div className="assignments-list">
                {suggestions.map(item => (
                    <div key={item.id} className="assignment-row">
                        <div className="task-info">
                            <span className="task-name">{item.task}</span>
                            <span className="task-id">#{item.id}</span>
                        </div>
                        <div className="arrow">→</div>
                        <div className="suggestion-info">
                            <span className="suggested-user">{item.suggested}</span>
                            <span className="confidence-badge">{item.confidence}% Match</span>
                        </div>
                        <div className="actions">
                            <button className="approve-btn">✓</button>
                            <button className="reject-btn">✕</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}