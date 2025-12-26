import React from 'react';
import { Icons } from '../common/Icons';

export const NAV_ITEMS = [
    { id: 'dashboard', label: 'Dashboard', icon: '🏠', desc: 'High-level snapshot of project health.' },
    { id: 'projects', label: 'Projects', icon: '📁', desc: 'Manage projects and milestones.' },
    { id: 'tasks', label: 'Tasks', icon: '📝', desc: 'Kanban board and task management.' },
    { id: 'timeline', label: 'Timeline', icon: '🧭', desc: 'Gantt charts and planning.' },
    { id: 'reports', label: 'Reports', icon: '📄', desc: 'Performance analytics.' },
];

export function SideMenu({ isOpen, onClose, activePage, onNavigate }) {
    return (
        <>
            <div
                className={`drawer-overlay ${isOpen ? 'open' : ''}`}
                onClick={onClose}
            ></div>

            <nav className={`side-menu ${isOpen ? 'open' : ''}`}>
                <div className="menu-header">Smartflow</div>
                <ul className="menu-list">
                    {NAV_ITEMS.map((item) => (
                        <li key={item.id}>
                            <div
                                className={`menu-item ${activePage === item.id ? 'active' : ''}`}
                                onClick={() => onNavigate(item.id)}
                            >
                                <span className="menu-icon">{item.icon}</span>
                                <span>{item.label}</span>
                            </div>
                        </li>
                    ))}
                </ul>
            </nav>
        </>
    );
}