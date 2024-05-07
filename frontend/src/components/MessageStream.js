import React, { useEffect, useRef } from 'react';
import Message from './Message';
import '../App.css';

function MessageStream({ selectedAgent, messages, agents, handleOpenLoadTeamModal, loadingCount }) {

  const filteredMessages = messages.filter(msg =>
    (msg.from_queue === selectedAgent?.queue || msg.to_queue === selectedAgent?.queue || 
      (msg.from_queue === "user_interface" && msg.to_queue === selectedAgent?.queue) || 
      (msg.from_queue === selectedAgent?.queue && msg.to_queue === "user_interface"))
  );

  const getSenderAvatar = (msg) => {
    const senderAgent = agents.find(agent => agent.queue === msg.from_queue);
    return senderAgent ? senderAgent.profile.avatar : null;
  };

  const endOfMessagesRef = useRef(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [filteredMessages]);

  return (
    <div className="messages">

        {filteredMessages.length > 0 ? (
          filteredMessages.map((msg, index) => (
            <Message
              key={index}
              from_name={msg.from_name}
              from_queue={msg.from_queue}
              to_name={msg.to_name}
              to_queue={msg.to_queue}
              cc_queue={msg.cc_queue}
              content={msg.content}
              message_type={msg.message_type}
              timestamp={msg.timestamp}
              avatar={getSenderAvatar(msg)}
            />
          ))
        ) : (
          <div id="intro-message">
            {
                agents.length > 0 && selectedAgent && selectedAgent.profile.avatar ? (
                    <div>
                        <img src={`/img/profiles/${selectedAgent.profile.avatar}`} alt="Agent" className="intro-image" width="200" height="200" />
                        <p className="amatic-sc-regular">{selectedAgent.profile.welcome_message}</p>
                    </div>
                ) : loadingCount > 0 ? (
                    <div>
                        <p className="amatic-sc-regular">One moment...</p>
                    </div>
                ) : (
                    <div>
                        <p className="amatic-sc-regular">Let's get started by loading a team...</p>
                        <button type="button" className="btn btn-primary" onClick={handleOpenLoadTeamModal}>Load a Team</button>
                    </div>
                )
            }
          </div>
        )}
        {/* Invisible element at the end of the messages, used for automatic scrolling */}
        <div ref={endOfMessagesRef} />
      </div>
  );
}

export default MessageStream;
