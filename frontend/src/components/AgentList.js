import React, { useEffect, useState, useRef } from 'react';
import AgentContextMenu from './AgentContextMenu';
import '../App.css';

function AgentList({ agents, onSelectAgent, loadingCount, apiBaseUrl }) {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [hoveredAgent, setHoveredAgent] = useState(null);
  const fileInputRef = useRef(null);

  const handleSelectAgent = (agent) => {
    setSelectedAgent(agent);
    onSelectAgent(agent);
  };

  /*
  useEffect(() => {
      // Check if there are agents and select the last one
      if (agents.length > 0) {
          const newAgent = agents[agents.length - 1];
          setSelectedAgent(newAgent);
          onSelectAgent(newAgent);
      }
  }, [agents, agents.length, onSelectAgent]);
  */

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file && selectedAgent) {  // Ensure there is a file and an agent selected
      console.log('File selected:', file.name);
      const formData = new FormData();
      formData.append('file', file);
      formData.append('context', 'agent_list');
      formData.append('agent_uuid', selectedAgent.instance_uuid);
      formData.append('agent_name', selectedAgent.profile.name);
      formData.append('agent_queue', selectedAgent.queue);
      try {

        console.log('Posting to ' + apiBaseUrl + '/upload')
        
        const response = await fetch(apiBaseUrl + '/upload', {
          method: 'POST',
          body: formData,
        });
  
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`File upload failed: ${errorText}`);
        }
  
        const result = await response.json();
        console.log('File uploaded successfully:', result);
        alert('File uploaded successfully!');
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('Error uploading file: ' + error.message);
      }
    } else {
      alert('Please select a file and ensure an agent is selected.');
    }
  };
  

  const handleShareFile = () => {
    fileInputRef.current.click(); // Simulate click on the file input
  };

  const handleDismissAgent = () => {
    console.log('Dismissing agent');
    // Future implementation for dismissing an agent
  };

  return (
    <div className="channel-list">
      {agents.map((agent, index) => (
          <div 
            key={agent.queue} 
            className={`card mb-2 ${agent.instance_uuid === selectedAgent?.instance_uuid ? 'text-dark selected' : 'unselected'}`}
            onClick={() => handleSelectAgent(agent)}
            onMouseEnter={() => setHoveredAgent(agent.instance_uuid)}
            onMouseLeave={() => setHoveredAgent(null)}
          >

              <div className="card-icon">
                <img src={`/img/profiles/${agent.profile.avatar}`} alt="A" width="40px" height="40px" />
                {agent.isThinking && <div className="ring"></div>}
              </div>

              <div className="card-body">
                {agent.profile.name} 
                <div className="role-name">[{agent.role.name}]</div>
              </div>

              {((hoveredAgent === agent.instance_uuid) || (agent.instance_uuid === selectedAgent?.instance_uuid)) && (
                <div className="agent-context-menu">
                  <AgentContextMenu onShare={handleShareFile} onDismiss={handleDismissAgent} agent_name={agent.profile.name} />
                </div>
              )}

        </div>
      ))}
      
      <input type="file" style={{ display: 'none' }} ref={fileInputRef} onChange={handleFileChange} />
      
      {Array.from({ length: loadingCount }).map((_, index) => (
        <div key={`skeleton-${index}`} className="card mb-2 skeleton">
          <div className="card-icon skeleton-image"></div>
          <div className="card-body skeleton-text"></div>
        </div>
      ))}
    </div>
  );
}

export default AgentList;
