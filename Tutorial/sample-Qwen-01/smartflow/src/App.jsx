import { useState, useEffect } from 'react';
import './App.css';
import TopBar from './components/Navigation/TopBar';
import SideMenu from './components/Navigation/SideMenu';

function App() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [currentProject, setCurrentProject] = useState('Smartflow Migration');

    // Close menu when clicking outside on mobile
    useEffect(() => {
        const handleClick = (e) => {
            if (isMenuOpen && !e.target.closest('.side-menu') && !e.target.closest('.menu-toggle')) {
                setIsMenuOpen(false);
            }
        };

        document.addEventListener('click', handleClick);
        return () => document.removeEventListener('click', handleClick);
    }, [isMenuOpen]);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    const menuItems = [
        { id: 'dashboard', icon: '🏠', label: 'Dashboard' },
        { id: 'projects', icon: '📁', label: 'Projects' },
        {
            id: 'timeline',
            icon: '🧭',
            label: 'Timeline Planner',
            children: [
                { id: 'network', label: 'Project Network (AON)' },
                { id: 'gantt', label: 'Gantt Chart' },
                { id: 'simulation', label: 'What-if Simulation' }
            ]
        },
        {
            id: 'tasks',
            icon: '📝',
            label: 'Tasks',
            children: [
                { id: 'task-list', label: 'Task List' },
                { id: 'dependencies', label: 'Task Dependencies' },
                { id: 'task-reports', label: 'Task Reports' }
            ]
        },
        { id: 'assignments', icon: '🎯', label: 'Assignments' },
        {
            id: 'resources',
            icon: '👥',
            label: 'Resources',
            children: [
                { id: 'directory', label: 'Resource Directory' },
                { id: 'calendar', label: 'Availability Calendar' },
                { id: 'workload', label: 'Workload View' }
            ]
        },
        { id: 'monitoring', icon: '📊', label: 'Monitoring & Progress' },
        { id: 'delay', icon: '⏱', label: 'Delay Prediction' },
        { id: 'notifications', icon: '🔔', label: 'Notifications & Reminders' },
        {
            id: 'reports',
            icon: '📄',
            label: 'Reports',
            children: [
                { id: 'weekly', label: 'Weekly Reports' },
                { id: 'monthly', label: 'Monthly Reports' },
                { id: 'project', label: 'Project Reports' },
                { id: 'delay-reports', label: 'Task Delay Reports' }
            ]
        },
        { id: 'settings', icon: '⚙', label: 'Settings' },
        { id: 'help', icon: '❓', label: 'Help & Docs' }
    ];

    return (
        <div className="app-container">
            <TopBar
                onMenuToggle={toggleMenu}
                currentProject={currentProject}
                onProjectChange={setCurrentProject}
            />

            <div className="main-content">
                {/* Content area is empty as requested */}
            </div>

            <SideMenu
                isOpen={isMenuOpen}
                items={menuItems}
                onClose={() => setIsMenuOpen(false)}
            />

            {isMenuOpen && (
                <div className="overlay" onClick={() => setIsMenuOpen(false)}></div>
            )}
        </div>
    );
}

export default App;