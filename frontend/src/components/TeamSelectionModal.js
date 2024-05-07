import React from 'react';
import { Modal, Card, Button, Container, Row, Col } from 'react-bootstrap';

const TeamSelectionModal = ({ teams, showModal, onClose, onLoadTeam }) => {
  return (
    <Modal show={showModal} onHide={onClose} size="lg" scrollable>
      <Modal.Header closeButton>
        <Modal.Title>Select a Team</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container>
          {/* Placeholder for search input */}
          <Row className="mb-3">
            <Col>
              <input className="form-control" placeholder="Search for teams..." disabled />
            </Col>
          </Row>
          {/* Scrollable container for team cards */}
          <div style={{ maxHeight: 'calc(100vh - 210px)', overflowY: 'auto' }}>
            {teams.map((team, index) => (
              <Card key={index} className="mb-3">
                <Card.Body>
                  <Row className="align-items-center">
                    <Col xs={12}>
                      <Row>
                        <Col xs={3} className="d-flex align-items-center justify-content-center">
                          <img src={`/img/team-logos/${team.logo}`} alt="Team Icon" style={{ width: '100px', height: '100px' }} />
                        </Col>
                        <Col>
                          <Card.Title>{team.name}</Card.Title>
                          {team.description && <Card.Subtitle>{team.description}</Card.Subtitle>}
                          <Row className="mt-2">
                            <Col xs={12} className="d-flex align-items-center justify-content-between">
                              {/* Container for profile images */}
                              <div className="profile-images-container">
                                {team.profiles.map((profile, index) => (
                                  <img key={index} src={`/img/profiles/${profile.avatar}`} alt={`Profile ${index}`} style={{ width: '40px', height: '40px', marginRight: '5px' }} />
                                ))}
                              </div>
                              <Button variant="primary" onClick={() => onLoadTeam(team.uuid, team.profiles.length)}>Load</Button>
                            </Col>
                          </Row>
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                </Card.Body>
              </Card>
            ))}
          </div>
        </Container>
      </Modal.Body>
    </Modal>
  );
};

export default TeamSelectionModal;