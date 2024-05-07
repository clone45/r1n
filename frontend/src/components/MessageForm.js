import React, { useState } from 'react';
import '../App.css'; // Import the CSS file
import { BsArrowUpSquareFill } from "react-icons/bs";

function MessageForm({ selectedAgent, isAgentsAvailable, apiBaseUrl, onMessageSend }) {
  const [message, setMessage] = useState('');
  const [dragging, setDragging] = useState(false);

  const handleDragOver = (event) => {
    event.preventDefault(); // Necessary to allow for a drop
    if (!dragging) {
      setDragging(true);
    }
  };

  const handleDragEnter = (event) => {
    event.preventDefault(); // Necessary to allow for a drop
    setDragging(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);
    const file = event.dataTransfer.files[0];
    handleFileUpload(file);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Prevent the default action (new line)
      handleSubmit(event); // Submit the form
    }
  };

  const handleInvalid = (event) => {
    event.target.setCustomValidity('Please enter a message.');
  };

  const handleChange = (event) => {
    setMessage(event.target.value);
    event.target.setCustomValidity('');
  };
  
  const handleFileUpload = async (file) => {
    if (!selectedAgent) {
      alert('Please select an agent first.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('context', 'thread'); // Use this to differentiate in your backend
    formData.append('agent_uuid', selectedAgent.instance_uuid);
    formData.append('agent_name', selectedAgent.profile.name);
    formData.append('agent_queue', selectedAgent.queue);
    
    try {
      const response = await fetch(apiBaseUrl + '/upload?context=thread', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        console.log('File uploaded successfully:', result);
        alert('File uploaded successfully!');
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file: ' + error.message);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!selectedAgent) {
      alert('Please select an agent first.');
      return;
    }

    var timestamp = new Date().toISOString();

    var message_json = JSON.stringify({
      from_name: "User Interface",
      from_queue: "user_interface",
      from_persona: "human (a person communicating with you)",
      to_name: selectedAgent.profile.name,
      to_queue: selectedAgent.queue,
      to_persona: "agent",
      cc_queue: "",
      content: message,
      message_type: "message",
      timestamp: timestamp
    });
  
    try {

      var url = apiBaseUrl + '/send-message';

      const response = await fetch(url, {
        method: 'POST',
        body: message_json,
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      try {
        const data = await response.json();
        console.log(data);
      } catch (parseError) {
        console.error('Error parsing response:', parseError);
      }
  
      if (response.ok) {
        onMessageSend({ 
          from_name: "You",
          from_queue: "user_interface",
          from_persona: "human (a person communicating with you)",
          to_name: selectedAgent.profile.name,
          to_queue: selectedAgent.queue,
          to_persona: "agent",
          cc_queue: "",
          content: message,
          message_type: "message",
          timestamp: timestamp
        });
        setMessage('');
      }

    } catch (networkError) {
      console.error('Error sending message:', networkError);
    }
  
    setMessage(''); // Clear message input field after sending
  };


  return (
    <div className="row">
      <div className="col">
        <div className="message-form-wrapper" onDragOver={handleDragOver} onDragEnter={handleDragEnter} onDragLeave={handleDragLeave} onDrop={handleDrop}>
          <form onSubmit={handleSubmit} className="message-form d-flex align-items-center">
            <div className="form-group flex-grow-1 me-2">
              <textarea 
                id="message-input"
                className="form-control"
                rows="1"
                placeholder="Type a message or drop a file..."
                required
                onInvalid={handleInvalid}
                onChange={handleChange}
                onKeyPress={handleKeyPress}
                value={message}
                disabled={!isAgentsAvailable || !selectedAgent}
                style={{ border: dragging ? '2px dashed #000' : '1px solid #ccc' }}  // Change border style on drag
              ></textarea>
            </div>
            <button type="submit" className="btn-submit">
              <BsArrowUpSquareFill />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
  
}

export default MessageForm;
