import React, { useState } from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import EditProfileModal from './EditProfileModal'; // This will need to be created similar to EditTeamModal

function ManageProfiles({ profiles, apiBaseUrl, setProfiles, roles }) {
    const [showModal, setShowModal] = useState(false);
    const [selectedProfile, setSelectedProfile] = useState(null);
    const [isNewProfile, setIsNewProfile] = useState(false);

    const handleShowModal = (profile) => {
        setSelectedProfile(profile);
        setIsNewProfile(false);
        setShowModal(true);
    };

    const handleShowAddNewModal = () => {
        setSelectedProfile(null);
        setIsNewProfile(true);
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setSelectedProfile(null);
        setIsNewProfile(false);
    };

    const handleSaveChanges = async (profile, data) => {

        const profileData = {
            name: data.name,
            role_uuid: data.roleUuid,
            avatar: data.avatar,
            description: data.description,
            welcome_message: data.welcomeMessage
        };

        try {
            let response;
            if (profile) {

                console.log('Updating profile:', profile);

                // Update existing profile
                response = await fetch(`${apiBaseUrl}/api/profiles/${profile.id}`, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(profileData)
                });
            } else {
                // Create new profile
                response = await fetch(`${apiBaseUrl}/api/profiles`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(profileData)
                });
            }

            if (response.ok) {
                const updatedProfile = await response.json();
                handleCloseModal();
                if (profile) {
                    const updatedProfiles = profiles.map(p => p.id === profile.id ? { ...p, ...updatedProfile } : p);
                    setProfiles(updatedProfiles);
                } else {
                    setProfiles(prev => [...prev, updatedProfile]);
                }
            } else {
                throw new Error('Failed to perform the operation');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleDelete = async (profile) => {
        if (!profile) {
            console.log('No profile selected for deletion.');
            return;
        }

        const confirmDelete = window.confirm('Are you sure you want to delete this profile?');
        if (confirmDelete) {
            const response = await fetch(`${apiBaseUrl}/api/profiles/${profile.id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                console.log("Profile deleted successfully!");
                handleCloseModal();
                setProfiles(profiles.filter(p => p.id !== profile.id));
            } else {
                throw new Error('Failed to delete the profile');
            }
        }
    };

    return (
        <div className="lowered-content page-manage-profiles">
            <Container className="mt-4">
            <Row className="mb-3">
                <Col xs={6}>
                    <input className="form-control" placeholder="Search for profiles..." style={{ width: '100%' }} />
                </Col>
                <Col xs={6} className="d-flex justify-content-end">
                    <Button variant="primary" className="btn-sm" onClick={handleShowAddNewModal}>Add New</Button>
                </Col>
            </Row>
            <div style={{ maxHeight: '80vh', overflowY: 'auto' }} className="editable-card-list">
                {profiles.map((profile, index) => {
                    const role = roles.find(role => role.uuid === profile.role_uuid);
                    return (
                        <Card key={profile.id} className="mb-3 profile-card" onClick={() => handleShowModal(profile)}>
                            <Card.Body>
                            <Row className="align-items-center">
                                <Col xs={12}>
                                <Row>
                                    <Col>
                                        <img src={`/img/profiles/${profile.avatar}`} alt="Profile Icon" style={{ width: '80px', height: '80px', float: 'left', marginRight: '20px' }} />
                                        <Card.Title>{profile.name}</Card.Title>
                                        {role && <div className="role-name">{role.name}</div>}
                                        <Card.Subtitle>{profile.description}</Card.Subtitle>
                                        <div className="edit-icon" style={{ position: 'absolute', top: '50%', right: '10px', transform: 'translateY(-50%)' }}>
                                            <i className="fas fa-pencil-alt"></i>
                                        </div>
                                    </Col>
                                </Row>
                                </Col>
                            </Row>
                            </Card.Body>
                        </Card>
                    );
                })}
            </div>
            </Container>
            <EditProfileModal
                show={showModal}
                profile={selectedProfile}
                isNewProfile={isNewProfile}
                onHide={handleCloseModal}
                onSave={handleSaveChanges}
                onDelete={handleDelete}
                roles={roles}
                // Profiles do not need the profiles prop
            />
        </div>
    );
}

export default ManageProfiles;
