import React from 'react';

function AgentContextMenu({ onShare, onDismiss, agent_name }) {
    return (
      <div className="dropdown">
        <button className="btn btn-secondary dropdown-toggle" type="button" 
          data-bs-toggle="dropdown" aria-expanded="false">
          
        </button>
        <ul className="dropdown-menu">
          <li><button className="dropdown-item" onClick={onShare}>Upload File to {agent_name}'s Library</button></li>
          <li><button className="dropdown-item">Manage {agent_name}'s Library</button></li>
        </ul>
      </div>
    );
  }

export default AgentContextMenu;
