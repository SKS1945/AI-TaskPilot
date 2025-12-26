import React from 'react';
import { Icons } from '../common/Icons';
import { UserProfile } from '../auth/UserProfile';
import { NotificationBell } from '../notification/NotificationBell';

export function TopBar({
                           onToggleSidebar,
                           projectList,
                           currentProject,
                           setCurrentProject,
                           isProjectMenuOpen,
                           setProjectMenuOpen
                       }) {
    return (
        <header className="top-bar">
            <div className="top-left">
                <button className="icon-btn" onClick={onToggleSidebar} aria-label="Toggle Menu">
                    <Icons.Menu />
                </button>

                <div className="search-wrapper">
                    <Icons.Search />
                    <input type="text" placeholder="Search..." className="search-input" />
                </div>
            </div>

            <div className="top-center">
                <div className="project-selector-wrapper">
                    {currentProject && (
                        <button
                            className={`context-pill ${isProjectMenuOpen ? 'active' : ''}`}
                            onClick={() => setProjectMenuOpen(!isProjectMenuOpen)}
                        >
                            📌 {currentProject.name} <Icons.ChevronDown />
                        </button>
                    )}

                    {isProjectMenuOpen && (
                        <div className="project-dropdown">
                            <div className="dropdown-header">Switch Project</div>
                            {projectList.map((project) => (
                                <button
                                    key={project.id}
                                    className={`project-option ${currentProject?.id === project.id ? 'selected' : ''}`}
                                    onClick={() => {
                                        setCurrentProject(project);
                                        setProjectMenuOpen(false);
                                    }}
                                >
                                    {project.name}
                                    {currentProject?.id === project.id && <span className="check-icon">✓</span>}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            <div className="top-right">
                <button className="icon-btn" title="AI Suggestions">
                    <Icons.Bot />
                </button>

                <NotificationBell />
                <UserProfile />
            </div>
        </header>
    );
}