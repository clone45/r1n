import React, { useEffect, useState } from 'react';
import '../App.css'; // Import the CSS file

function AgentTools() {

  
  return (
    <div className="channel-list">
      {agents.map((agent, index) => (
        <div 
          key={agent.queue} 
          className={`card mb-2 ${agent.queue === selectedAgent?.queue ? 'text-dark selected' : 'unselected'}`}
          onClick={() => handleSelectAgent(agent)}
        >
          <div className="card-body">
            {agent.profile.name} [{agent.queue}]
          </div>
        </div>
      ))}
    </div>
  );
}

export default AgentTools;