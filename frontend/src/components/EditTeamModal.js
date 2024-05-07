import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import ProfileMultiSelect from './ProfileMultiSelect';
import ImageDropdown from './ImageDropdown';

function EditTeamModal({ show, team, isNewTeam, onHide, onSave, onDelete, profiles }) {
    const [teamName, setTeamName] = useState('');
    const [teamDescription, setTeamDescription] = useState('');
    const [teamLogo, setTeamLogo] = useState('');
    const [selectedProfileUuids, setSelectedProfileUuids] = useState([]);

    const logoOptions = [
        { value: 'team-logo-1.png', imgSrc: '/img/team-logos/team-logo-1.png' },
        { value: 'team-logo-2.png', imgSrc: '/img/team-logos/team-logo-2.png' },
        { value: 'team-logo-3.png', imgSrc: '/img/team-logos/team-logo-3.png' },
        { value: 'team-logo-4.png', imgSrc: '/img/team-logos/team-logo-4.png' },
        { value: 'team-logo-5.png', imgSrc: '/img/team-logos/team-logo-5.png' },
        { value: 'team-logo-6.png', imgSrc: '/img/team-logos/team-logo-6.png' },
        { value: 'team-logo-7.png', imgSrc: '/img/team-logos/team-logo-7.png' },
        { value: 'team-logo-8.png', imgSrc: '/img/team-logos/team-logo-8.png' },
    ];

    useEffect(() => {
        if (isNewTeam) {
            // Reset states for new team
            setTeamName('');
            setTeamDescription('');
            setTeamLogo('');
            setSelectedProfileUuids([]);
        } else if (team) {
            // Set states for editing existing team
            setTeamName(team.name);
            setTeamDescription(team.description || '');
            setTeamLogo(team.logo);
            setSelectedProfileUuids(team.profile_uuids || []);
        }
    }, [team, isNewTeam]);

    const handleProfileToggle = (profileUuid) => {
        setSelectedProfileUuids(current =>
            current.includes(profileUuid)
            ? current.filter(uuid => uuid !== profileUuid)
            : [...current, profileUuid]
        );
    };

    const handleLogoChange = newLogo => {
        setTeamLogo(newLogo);
    };

    return (
        <Modal show={show} onHide={onHide}>
            <Modal.Header closeButton>
                <Modal.Title>{isNewTeam ? "Add New Team" : "Edit Team"}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3" controlId="teamName">
                        <Form.Label>Team Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter team name"
                            value={teamName}
                            onChange={(e) => setTeamName(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="teamDescription">
                        <Form.Label>Team Description</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={3}
                            placeholder="Enter team description"
                            value={teamDescription}
                            onChange={(e) => setTeamDescription(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>Team Logo</Form.Label>
                        <ImageDropdown
                            options={logoOptions}
                            onChange={handleLogoChange}
                            initialSelectedImage={teamLogo ? `/img/team-logos/${teamLogo}` : ''}
                        />
                    </Form.Group>

                    <Form.Label>Team Members</Form.Label>
                    <div style={{ maxHeight: '250px', overflowY: 'auto', paddingRight: '15px' }}>
                        <ProfileMultiSelect
                            profiles={profiles}
                            selectedProfileUuids={selectedProfileUuids}
                            onProfileToggle={handleProfileToggle}
                        />
                    </div>
                </Form>
            </Modal.Body>
            <Modal.Footer className="justify-content-start">
                {isNewTeam ? (
                    <Button variant="primary" onClick={() => onSave(null, teamName, teamDescription, teamLogo, selectedProfileUuids)}>
                        Add Team
                    </Button>
                ) : (
                    <>
                        <Button variant="danger" onClick={() => onDelete(team)}>
                            Delete Team
                        </Button>
                        <div className="ms-auto">
                            <Button variant="secondary" onClick={onHide} className="me-2">
                                Close
                            </Button>
                            <Button variant="primary" onClick={() => onSave(team, teamName, teamDescription, teamLogo, selectedProfileUuids)}>
                                Save Changes
                            </Button>
                        </div>
                    </>
                )}
            </Modal.Footer>
        </Modal>
    );
}

export default EditTeamModal;
