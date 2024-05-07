// Message.js
import React from 'react';
import '../App.css'; // Adjust the path as needed
import { FaUserAlt, FaRobot } from 'react-icons/fa';
import Markdown from 'react-markdown'

function Message({ from_name, from_queue, from_persona, to_name, to_queue, to_persona, content, message_type, timestamp, avatar }) {

  const isUser = from_queue === "user_interface"; // Update this check as necessary

  // content may have markdown in it, so we need to render it as markdown
  // the message type does not help us identify markdown, so we will just render all messages as markdown
  content = <Markdown>{content}</Markdown>

  // Choose either the profile image or the default icon
  const displayImage = avatar ? 
    <img src={`/img/profiles/${avatar}`} alt="Profile" className="message-icon" /> :
    (isUser ? <FaUserAlt /> : <FaRobot />);

  return (
    <div className="message">
      <div className="message-icon">
        {displayImage}
      </div>
      <div className="message-content">
        {!isUser && <p className="persona-label">{from_name}</p>}
        <div>{content}</div>
      </div>
    </div>
  );
}

export default Message;
