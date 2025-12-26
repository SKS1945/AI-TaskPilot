import { useState, useEffect } from 'react';
import './App.css';

// Components
import { TopBar } from './components/navigation/TopBar';
import { SideMenu } from './components/navigation/SideMenu'; // Remove NAV_ITEMS from here
import { NAV_ITEMS } from './components/navigation/navConfig'; // <--- Add this import
import { Dashboard } from './components/pages/Dashboard/Dashboard';
import { Tasks } from './components/pages/Tasks/Tasks';
import { Resources } from './components/pages/Resources/Resources';
import { Assignments } from './components/pages/Assignments/Assignments';
import { Settings } from './components/pages/Settings/Settings';
import { Placeholder } from './components/pages/Placeholders/Placeholder';

const API_BASE = "http://localhost:8000/api";

function App() {
    const [isSidebarOpen, setSidebarOpen] = useState(false);
    const [activePage, setActivePage] = useState('dashboard');

    // Data State
    const [projectList, setProjectList] = useState([]);
    const [currentProject, setCurrentProject] = useState(null);
    const [dashboardData, setDashboardData] = useState(null);
    const [tasks, setTasks] = useState([]);
    const [draggedTaskId, setDraggedTaskId] = useState(null);
    const [isProjectMenuOpen, setProjectMenuOpen] = useState(false);

    // Initial Load
    useEffect(() => {
        fetch(`${API_BASE}/projects/context-list/`)
            .then(res => res.json())
            .then(data => {
                setProjectList(data);
                if (data.length > 0) setCurrentProject(data[0]);
            })
            .catch(err => console.error("API Error:", err));
    }, []);

    // Fetch Data on Change
    useEffect(() => {
        if (!currentProject) return;

        if (activePage === 'dashboard') {
            fetch(`${API_BASE}/projects/${currentProject.id}/dashboard/`)
                .then(res => res.json())
                .then(data => setDashboardData(data));
        }
        else if (activePage === 'tasks') {
            fetch(`${API_BASE}/tasks/project/${currentProject.id}/`)
                .then(res => res.json())
                .then(data => setTasks(data));
        }
    }, [activePage, currentProject]);

    const handleNavClick = (id) => {
        setActivePage(id);
        setSidebarOpen(false);
    };

    // Drag Handlers
    const onDragStart = (e, taskId) => { setDraggedTaskId(taskId); e.dataTransfer.effectAllowed = "move"; };
    const onDragOver = (e) => e.preventDefault();
    const onDrop = (e, newStatus) => {
        e.preventDefault();
        if (!draggedTaskId) return;
        const updatedTasks = tasks.map(t => t.id === draggedTaskId ? { ...t, status: newStatus } : t);
        setTasks(updatedTasks);
        fetch(`${API_BASE}/tasks/${draggedTaskId}/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        }).catch(err => console.error("Update failed", err));
        setDraggedTaskId(null);
    };

    const activePageData = NAV_ITEMS.find(item => item.id === activePage) || NAV_ITEMS[0];

    return (
        <div className="app-container">
            <TopBar
                onToggleSidebar={() => setSidebarOpen(!isSidebarOpen)}
                projectList={projectList}
                currentProject={currentProject}
                setCurrentProject={setCurrentProject}
                isProjectMenuOpen={isProjectMenuOpen}
                setProjectMenuOpen={setProjectMenuOpen}
            />

            <SideMenu
                isOpen={isSidebarOpen}
                onClose={() => setSidebarOpen(false)}
                activePage={activePage}
                onNavigate={handleNavClick}
            />

            <main className="main-content">
                <div className="page-header">
                    <h1 className="page-title">{activePageData.icon} {activePageData.label}</h1>
                    <p className="page-description">{activePageData.desc}</p>
                </div>

                {activePage === 'dashboard' && <Dashboard data={dashboardData} />}
                {activePage === 'tasks' && <Tasks tasks={tasks} onDragStart={onDragStart} onDragOver={onDragOver} onDrop={onDrop} />}
                {activePage === 'resources' && <Resources />}
                {activePage === 'assignments' && <Assignments />}
                {activePage === 'settings' && <Settings />}

                {/* Fallback for pages not yet created */}
                {!['dashboard', 'tasks', 'resources', 'assignments', 'settings'].includes(activePage) && (
                    <Placeholder pageName={activePageData.label} />
                )}
            </main>
        </div>
    );
}

export default App;