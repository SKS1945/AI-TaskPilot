import React from 'react';
import './Dashboard.css';

export function Dashboard({ data }) {
    if (!data) {
        return (
            <div className="placeholder-card">
                <p>Loading dashboard data...</p>
            </div>
        );
    }

    return (
        <div className="dashboard-grid">
            {/* Health Card */}
            <div className="kpi-card">
                <h3>Project Health</h3>
                <div className={`health-score ${data.snapshot.health_score < 70 ? 'risk' : 'good'}`}>
                    {data.snapshot.health_score}%
                </div>
                <p className="kpi-sub">Status: {data.snapshot.status}</p>
            </div>

            {/* Active Risks */}
            <div className="kpi-card wide">
                <h3>⚠️ Active Risks (High Probability)</h3>
                <ul className="risk-list">
                    {data.active_risks.length === 0 ? (
                        <li className="empty-state">No active risks detected.</li>
                    ) : (
                        data.active_risks.map(risk => (
                            <li key={risk.task_id} className="risk-item">
                                <span className="risk-prob">{(risk.delay_prob * 100).toFixed(0)}% Delay</span>
                                <span className="risk-title">{risk.task_title}</span>
                            </li>
                        ))
                    )}
                </ul>
            </div>

            {/* Deadlines */}
            <div className="kpi-card">
                <h3>📅 Next 7 Days</h3>
                <ul className="deadline-list">
                    {data.upcoming_deadlines.length === 0 ? (
                        <li className="empty-state">No upcoming deadlines.</li>
                    ) : (
                        data.upcoming_deadlines.map(m => (
                            <li key={m.id} className="deadline-item">
                                <span className="deadline-date">{m.due_date}</span>
                                <span>{m.name}</span>
                            </li>
                        ))
                    )}
                </ul>
            </div>
        </div>
    );
}