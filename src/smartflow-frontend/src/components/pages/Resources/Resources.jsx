import React from 'react';
import './Resources.css';

export function Resources() {
    // Sample data - normally fetched from API
    const resources = [
        { id: 1, name: 'Alice Freeman', role: 'Frontend Dev', availability: 80, skills: ['React', 'CSS'] },
        { id: 2, name: 'Bob Smith', role: 'Backend Dev', availability: 40, skills: ['Django', 'Python'] },
        { id: 3, name: 'Charlie Kim', role: 'Designer', availability: 100, skills: ['Figma', 'UI/UX'] },
    ];

    return (
        <div className="resources-container">
            <div className="resources-header-actions">
                <button className="primary-btn">+ Add Resource</button>
            </div>

            <div className="resources-grid">
                {resources.map(res => (
                    <div key={res.id} className="resource-card">
                        <div className="resource-avatar">{res.name.charAt(0)}</div>
                        <div className="resource-info">
                            <h3>{res.name}</h3>
                            <span className="role-badge">{res.role}</span>

                            <div className="availability-bar-wrapper">
                                <div className="availability-label">
                                    <span>Availability</span>
                                    <span>{res.availability}%</span>
                                </div>
                                <div className="progress-bar">
                                    <div
                                        className="progress-fill"
                                        style={{width: `${res.availability}%`, backgroundColor: res.availability < 50 ? '#ef4444' : '#10b981'}}
                                    ></div>
                                </div>
                            </div>

                            <div className="skills-list">
                                {res.skills.map(skill => (
                                    <span key={skill} className="skill-tag">{skill}</span>
                                ))}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}