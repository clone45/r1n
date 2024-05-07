import React from 'react';
import LargeCheckbox from './LargeCheckbox';

function ProfileMultiSelect({ profiles, selectedProfileUuids, onProfileToggle }) {
  
  // Adjust handleToggle to receive the event object
  const handleToggle = (profileUuid, event) => {
    event.stopPropagation(); // Prevent the click from triggering multiple handlers
    console.log("Toggling Profile Uuid:", profileUuid);
    onProfileToggle(profileUuid);
  };

  return (
    <div className="profile-list selectable-card-list">
      {profiles.map(profile => (
        <div 
          key={profile.uuid} 
          className="card mb-2" 
          onClick={(e) => handleToggle(profile.uuid, e)}  // Add click handler to the card
        >
          <div className="card-body">
            <div className="row align-items-center mb-2">
              <div className="col-auto">
                <img src={`/img/profiles/${profile.avatar}`} alt={profile.name} className="rounded-circle" width="40" height="40" />
              </div>
              <div className="col">
                <strong>{profile.name}</strong><br />
                <span className="text-muted">{profile.role.name}</span>
                <div className="debugging_uuid">UUID: {profile.uuid}</div>
              </div>
              <div className="col-auto">
                <LargeCheckbox
                  checked={selectedProfileUuids.includes(profile.uuid)}
                  onChange={(e) => handleToggle(profile.uuid, e)}  // Adjust this to prevent default when clicking the checkbox
                />
              </div>
            </div>
            {/* Description row outside and below the profile info row */}
            <div className="row">
              <div className="col">
                <small className="text-muted">{profile.description}</small>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ProfileMultiSelect;
