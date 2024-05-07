import React, { useState } from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import EditTeamModal from './EditTeamModal';

function ManageTeams({ teams, apiBaseUrl, setTeams, profiles }) {
    const [showModal, setShowModal] = useState(false);
    const [selectedTeam, setSelectedTeam] = useState(null);
    const [isNewTeam, setIsNewTeam] = useState(false);  // Track if the modal is for a new team


    const handleShowModal = (team) => {
        setSelectedTeam(team);
        setIsNewTeam(false);  // Not a new team
        setShowModal(true);
    };

    const handleShowAddNewModal = () => {
        setSelectedTeam(null);
        setIsNewTeam(true);  // This is for adding a new team
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setSelectedTeam(null);
        setIsNewTeam(false);  // Reset this state on modal close
    };

    const handleSaveChanges = async (team, name, description, logo, profileUuids) => {
    
        const teamData = {
            name: name,
            description: description,
            logo: logo,
            profile_uuids: profileUuids
        };
    
        try {
            let response;
            if (team) {
                // Update existing team
                response = await fetch(`${apiBaseUrl}/api/teams/${team.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(teamData)
                });
            } else {
                // Create new team
                response = await fetch(`${apiBaseUrl}/api/teams`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(teamData)
                });
            }
    
            if (response.ok) {
                const data = await response.json(); // Assuming the response includes the full team data
                console.log("Operation successful!", data);
                handleCloseModal();  // Close the modal on successful operation
    
                if (team) {
                    // Update the local teams array with the updated team
                    const updatedTeams = teams.map(t => t.id === team.id ? { ...t, ...data } : t);
                    setTeams(updatedTeams);
                } else {
                    // Add the new team to the local teams array
                    setTeams(prevTeams => [...prevTeams, data]);
                }
            } else {
                throw new Error('Failed to perform the operation');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleDelete = async (team) => {
        if (!team) {
            console.log('No team selected for deletion.');
            return;  // Exit if there's no team selected
        }

        const confirmDelete = window.confirm('Are you sure you want to delete this team?');
        if (confirmDelete) {
            const response = await fetch(`${apiBaseUrl}/api/teams/${team.id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                console.log("Team deleted successfully!");
                handleCloseModal();  // Close the modal on successful deletion

                // Update the local teams array
                const updatedTeams = teams.filter(t => t.id !== team.id);
                setTeams(updatedTeams); // Update the state with the new teams array
            } else {
                throw new Error('Failed to delete the team');
            }
        }
    };

    // JSX remains mostly unchanged except the modal part
    return (
        <div className="lowered-content page-manage-teams">
            <Container className="mt-4">
            <Row className="mb-3">
                <Col xs={6}>
                    <input className="form-control" placeholder="Search for teams..." style={{ width: '100%' }} />
                </Col>
                <Col xs={6} className="d-flex justify-content-end">
                    <Button variant="primary" className="btn-sm" onClick={handleShowAddNewModal}>Add New</Button>
                </Col>
            </Row>
            <div style={{ maxHeight: '80vh', overflowY: 'auto' }} className="editable-card-list">
                {teams.map((team, index) => (
                    <Card key={index} className="mb-3 team-card" onClick={() => handleShowModal(team)}>
                    <Card.Body>
                        <Row className="align-items-center">
                            {/* Image column */}
                            <Col xs={2} className="text-center">
                                <img src={`/img/team-logos/${team.logo}`} alt="Team Icon" style={{ width: '80px', height: '80px' }} />
                            </Col>
                            
                            {/* Content column */}
                            <Col xs={9}>
                                <Card.Title>{team.name}</Card.Title>
                                {team.description && <Card.Subtitle>{team.description}</Card.Subtitle>}
                                <Row className="mt-2">
                                    <Col xs={12} className="d-flex align-items-center">
                                        <div className="profile-images-container">
                                            {team.profiles.map((profile, index) => (
                                                <img key={index} src={`/img/profiles/${profile.avatar}`} alt={`Profile ${index}`} style={{ width: '40px', height: '40px', marginRight: '5px' }} />
                                            ))}
                                        </div>
                                    </Col>
                                </Row>
                            </Col>

                            {/* Edit icon column */}
                            <Col xs={1} className="text-right">
                                <div className="edit-icon" style={{ position: 'absolute', top: '50%', transform: 'translateY(-50%)' }}>
                                    <i className="fas fa-pencil-alt"></i>
                                </div>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>
                ))}
            </div>
            </Container>
            <EditTeamModal
                show={showModal}
                team={selectedTeam}
                isNewTeam={isNewTeam}
                onHide={handleCloseModal}
                onSave={handleSaveChanges}
                onDelete={handleDelete}
                profiles={profiles}
            />
        </div>
    );
}

export default ManageTeams;
