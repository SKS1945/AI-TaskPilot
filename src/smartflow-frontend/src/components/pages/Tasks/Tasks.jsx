import React from 'react';
import { Icons } from '../../common/Icons';
import './Tasks.css';

export function Tasks({ tasks, onDragStart, onDragOver, onDrop }) {

    const renderColumn = (status, title, cssClass) => (
        <div
            className="kanban-column"
            onDragOver={onDragOver}
            onDrop={(e) => onDrop(e, status)}
        >
            <div className={`column-header ${cssClass}`}>
                {title} <span className="count">{tasks.filter(t => t.status === status).length}</span>
            </div>
            <div className="column-content">
                {tasks.filter(t => t.status === status).map(task => (
                    <div
                        key={task.id}
                        className={`task-card ${status === 'completed' ? 'completed' : ''}`}
                        draggable
                        onDragStart={(e) => onDragStart(e, task.id)}
                    >
                        <div className="task-title">{task.title}</div>
                        <div className="task-meta">
                            <span className={`priority-badge p-${task.weight || 1}`}>P{task.weight || 1}</span>
                            {task.planned_finish && (
                                <span className="task-date"><Icons.Clock /> {task.planned_finish}</span>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );

    return (
        <div className="kanban-board">
            {renderColumn('pending', 'Todo', 'status-pending')}
            {renderColumn('in_progress', 'In Progress', 'status-progress')}
            {renderColumn('completed', 'Done', 'status-done')}
        </div>
    );
}