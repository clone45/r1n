import React, { useState } from 'react';
import AgentList from './AgentList';
import MessageStream from './MessageStream';
import MessageForm from './MessageForm';

function Chat({ agents, selectedAgent, messages, loadingCount, apiBaseUrl, setSelectedAgent, handleOpenLoadTeamModal,  handleNewMessage}) {

    return (
        <div className="body-content">
            <div className="row main-content-row ps-0">
                <div className="col-md-3 agent-list-column">
                    <AgentList agents={agents} onSelectAgent={setSelectedAgent} loadingCount={loadingCount} apiBaseUrl={apiBaseUrl} />
                </div>
                <div className="col-md-9 content message-stream-column">
                    <MessageStream selectedAgent={selectedAgent} messages={messages} agents={agents} handleOpenLoadTeamModal={handleOpenLoadTeamModal} loadingCount={loadingCount} />
                    <MessageForm 
                        selectedAgent={selectedAgent} 
                        isAgentsAvailable={agents.length > 0}
                        apiBaseUrl={apiBaseUrl}
                        onMessageSend={handleNewMessage}
                    />
                </div>
            </div>
        </div>
    );
}

export default Chat;
