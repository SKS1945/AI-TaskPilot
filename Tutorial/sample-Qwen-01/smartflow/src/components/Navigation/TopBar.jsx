import { useState } from 'react';

const TopBar = ({ onMenuToggle, currentProject, onProjectChange }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [aiCount] = useState(3);
    const [notificationCount] = useState(5);

    const handleProjectChange = (e) => {
        onProjectChange(e.target.value);
    };

    return (
        <header className="top-bar">
            <div className="top-bar-left">
                <button
                    className="menu-toggle"
                    onClick={onMenuToggle}
                    aria-label="Toggle navigation menu"
                >
                    ☰
                </button>

                <div className="search-container">
                    <input
                        type="text"
                        placeholder="Search projects, tasks, resources..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="search-input"
                    />
                    <span className="search-icon">🔍</span>
                </div>
            </div>

            <div className="top-bar-center">
                <div className="project-context">
                    <span className="context-label">Project:</span>
                    <select
                        value={currentProject}
                        onChange={handleProjectChange}
                        className="project-selector"
                    >
                        <option>Smartflow Migration</option>
                        <option>Cloud Infrastructure Upgrade</option>
                        <option>Data Platform Revamp</option>
                        <option>Mobile App Launch</option>
                    </select>
                </div>
            </div>

            <div className="top-bar-right">
                <button className="ai-button" aria-label="AI Suggestions">
                    <span className="button-icon">🤖</span>
                    {aiCount > 0 && <span className="badge">{aiCount}</span>}
                </button>

                <button className="notification-button" aria-label="Notifications">
                    <span className="button-icon">🔔</span>
                    {notificationCount > 0 && <span className="badge">{notificationCount}</span>}
                </button>

                <div className="user-profile">
                    <span className="user-initial">UD</span>
                </div>
            </div>
        </header>
    );
};

export default TopBar;