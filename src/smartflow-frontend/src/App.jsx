import { useState, useEffect } from 'react';
import './App.css';

// --- Configuration ---
const API_BASE = "http://localhost:8000/api";

// --- Icons (Simple Inline SVGs) ---
const Icons = {
    Menu: () => <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>,
    Search: () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>,
    Bell: () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>,
    Bot: () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>,
    ChevronDown: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="6 9 12 15 18 9"></polyline></svg>,
    LogOut: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>,
    UserPlus: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>,
    Settings: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
};

// --- Navigation Config ---
const NAV_ITEMS = [
    { id: 'dashboard', label: 'Dashboard', icon: '🏠', desc: 'High-level snapshot of project health, active risks, upcoming deadlines, and AI recommendations.' },
    { id: 'projects', label: 'Projects', icon: '📁', desc: 'View, create, and manage projects with status, milestones, and overall progress.' },
    { id: 'timeline', label: 'Timeline Planner', icon: '🧭', desc: 'Build and visualize project timelines using network diagrams and Gantt charts (AI-assisted).', subItems: ['Project Network (AON)', 'Gantt Chart', 'What-if Simulation'] },
    { id: 'tasks', label: 'Tasks', icon: '📝', desc: 'Manage tasks, dependencies, priorities, progress, and task-level reports.', subItems: ['Task List', 'Task Dependencies', 'Task Reports'] },
    { id: 'assignments', label: 'Assignments', icon: '🎯', desc: 'Review and adjust task assignments suggested by algorithms/AI.' },
    { id: 'resources', label: 'Resources', icon: '👥', desc: 'View team members, skills, workload, and cross-project availability.', subItems: ['Resource Directory', 'Availability Calendar', 'Workload View'] },
    { id: 'monitoring', label: 'Monitoring & Progress', icon: '📊', desc: 'Track real-time progress, weighted task health, and critical path status.' },
    { id: 'prediction', label: 'Delay Prediction', icon: '⏱', desc: 'View predicted delays using PERT/CPM models and probabilistic analysis.' },
    { id: 'notifications', label: 'Notifications & Reminders', icon: '🔔', desc: 'Configure reminder rules, escalation logic, and view notification history.' },
    { id: 'reports', label: 'Reports', icon: '📄', desc: 'Access weekly, monthly, project-level, and task-level reports.', subItems: ['Weekly Reports', 'Monthly Reports', 'Project Reports', 'Task Delay Reports'] },
    { id: 'settings', label: 'Settings', icon: '⚙', desc: 'Configure skills, notification rules, thresholds, and system preferences.' },
    { id: 'help', label: 'Help & Docs', icon: '❓', desc: 'User guides, system explanations, and AI decision transparency.' },
];

function App() {
    const [isSidebarOpen, setSidebarOpen] = useState(false);
    const [activePage, setActivePage] = useState('dashboard');
    const [expandedMenus, setExpandedMenus] = useState({});

    // Data State
    const [projectList, setProjectList] = useState([]);
    const [currentProject, setCurrentProject] = useState(null); // {id, name}
    const [dashboardData, setDashboardData] = useState(null);

    // UI State
    const [isProjectMenuOpen, setProjectMenuOpen] = useState(false);
    const [isProfileMenuOpen, setProfileMenuOpen] = useState(false);

    // 1. Fetch Projects on Load
    useEffect(() => {
        fetch(`${API_BASE}/projects/context-list/`)
            .then(res => res.json())
            .then(data => {
                setProjectList(data);
                if (data.length > 0) setCurrentProject(data[0]);
            })
            .catch(err => console.error("Error fetching projects:", err));
    }, []);

    // 2. Fetch Dashboard Data when Project Changes
    useEffect(() => {
        if (activePage === 'dashboard' && currentProject) {
            fetch(`${API_BASE}/projects/${currentProject.id}/dashboard/`)
                .then(res => res.json())
                .then(data => setDashboardData(data))
                .catch(err => console.error("Error fetching dashboard:", err));
        }
    }, [activePage, currentProject]);

    const toggleSidebar = () => setSidebarOpen(!isSidebarOpen);

    const handleNavClick = (id, hasSubItems) => {
        setActivePage(id);
        if (hasSubItems) {
            setExpandedMenus(prev => ({ ...prev, [id]: !prev[id] }));
        }
    };

    const activePageData = NAV_ITEMS.find(item => item.id === activePage) || NAV_ITEMS[0];

    return (
        <div className="app-container">

            {/* 1. Top Navigation Bar */}
            <header className="top-bar">
                <div className="top-left">
                    <button className="icon-btn" onClick={toggleSidebar} aria-label="Toggle Menu">
                        <Icons.Menu />
                    </button>

                    <div className="search-wrapper">
                        <Icons.Search />
                        <input type="text" placeholder="Search..." className="search-input" />
                    </div>
                </div>

                {/* Center: Dynamic Project Switcher */}
                <div className="top-center">
                    <div className="project-selector-wrapper">
                        {currentProject && (
                            <button
                                className={`context-pill ${isProjectMenuOpen ? 'active' : ''}`}
                                onClick={() => {
                                    setProjectMenuOpen(!isProjectMenuOpen);
                                    setProfileMenuOpen(false);
                                }}
                            >
                                📌 Project: {currentProject.name} <Icons.ChevronDown />
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

                {/* Right: Actions & Profile */}
                <div className="top-right">
                    <button className="icon-btn"><Icons.Bot /></button>
                    <button className="icon-btn"><Icons.Bell /></button>

                    <div className="profile-wrapper">
                        <div
                            className="user-profile"
                            onClick={() => {
                                setProfileMenuOpen(!isProfileMenuOpen);
                                setProjectMenuOpen(false);
                            }}
                        >
                            JS
                        </div>

                        {isProfileMenuOpen && (
                            <div className="profile-dropdown-card">
                                <div className="profile-header">
                                    <span className="profile-email">john.smith@smartflow.com</span>
                                    <div className="profile-avatar-large">JS</div>
                                    <div className="profile-greeting">Hi, John!</div>
                                    <button className="manage-account-btn">Manage your Account</button>
                                </div>
                                <div className="profile-actions-row">
                                    <button className="action-btn-block"><Icons.UserPlus /> Add account</button>
                                    <button className="action-btn-block"><Icons.LogOut /> Sign out</button>
                                </div>
                                <div className="profile-footer-links">
                                    <span>Privacy Policy</span> • <span>Terms of Service</span>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </header>

            {/* 2. Side Drawer Menu (Unchanged logic, just keeping structure) */}
            <>
                <div className={`drawer-overlay ${isSidebarOpen ? 'open' : ''}`} onClick={() => setSidebarOpen(false)}></div>
                <nav className={`side-menu ${isSidebarOpen ? 'open' : ''}`}>
                    <div className="menu-header">Smartflow</div>
                    <ul className="menu-list">
                        {NAV_ITEMS.map((item) => (
                            <li key={item.id}>
                                <div className={`menu-item ${activePage === item.id ? 'active' : ''}`} onClick={() => handleNavClick(item.id, !!item.subItems)}>
                                    <span className="menu-icon">{item.icon}</span><span>{item.label}</span>
                                </div>
                                {item.subItems && expandedMenus[item.id] && (
                                    <ul className="sub-menu">
                                        {item.subItems.map((sub, idx) => <li key={idx} className="sub-item">• {sub}</li>)}
                                    </ul>
                                )}
                            </li>
                        ))}
                    </ul>
                </nav>
            </>

            {/* Main Content Area */}
            <main className="main-content">
                <div className="page-header">
                    <h1 className="page-title">{activePageData.icon} {activePageData.label}</h1>
                    <p className="page-description">{activePageData.desc}</p>
                </div>

                {/* Dynamic Dashboard Content */}
                {activePage === 'dashboard' && dashboardData ? (
                    <div className="dashboard-grid">
                        {/* 1. Health Card */}
                        <div className="kpi-card">
                            <h3>Project Health</h3>
                            <div className={`health-score ${dashboardData.snapshot.health_score < 70 ? 'risk' : 'good'}`}>
                                {dashboardData.snapshot.health_score}%
                            </div>
                            <p className="kpi-sub">Status: {dashboardData.snapshot.status}</p>
                        </div>

                        {/* 2. Active Risks */}
                        <div className="kpi-card wide">
                            <h3>⚠️ Active Risks (High Probability)</h3>
                            <ul className="risk-list">
                                {dashboardData.active_risks.length === 0 ? (
                                    <li className="empty-state">No active risks detected.</li>
                                ) : (
                                    dashboardData.active_risks.map(risk => (
                                        <li key={risk.task_id} className="risk-item">
                                            <span className="risk-prob">{(risk.delay_prob * 100).toFixed(0)}% Delay</span>
                                            <span className="risk-title">{risk.task_title}</span>
                                        </li>
                                    ))
                                )}
                            </ul>
                        </div>

                        {/* 3. Upcoming Deadlines */}
                        <div className="kpi-card">
                            <h3>📅 Next 7 Days</h3>
                            <ul className="deadline-list">
                                {dashboardData.upcoming_deadlines.length === 0 ? (
                                    <li className="empty-state">No upcoming deadlines.</li>
                                ) : (
                                    dashboardData.upcoming_deadlines.map(m => (
                                        <li key={m.id} className="deadline-item">
                                            <span className="deadline-date">{m.due_date}</span>
                                            <span>{m.name}</span>
                                        </li>
                                    ))
                                )}
                            </ul>
                        </div>
                    </div>
                ) : (
                    <div className="placeholder-card">
                        <p>Select a project to view {activePageData.label}.</p>
                    </div>
                )}
            </main>

        </div>
    );
}

export default App;