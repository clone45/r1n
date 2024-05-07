// EditProfileModal.js
import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import RoleSelector from './RoleSelector';
import ImageDropdown from './ImageDropdown';


function EditProfileModal({ show, profile, isNewProfile, onHide, onSave, onDelete, roles }) {
    const [name, setName] = useState('');
    const [roleUuid, setRoleUuid] = useState('');
    const [avatar, setAvatar] = useState('');
    const [description, setDescription] = useState('');
    const [welcomeMessage, setWelcomeMessage] = useState('');

    const avatarOptions = [
        { value: 'haiku_female_1.png', text: 'Female 1', imgSrc: '/img/profiles/haiku_female_1.png' },
        { value: 'haiku_female_2.png', text: 'Female 2', imgSrc: '/img/profiles/haiku_female_2.png' },
        { value: 'haiku_female_3.png', text: 'Female 3', imgSrc: '/img/profiles/haiku_female_3.png' },
        { value: 'haiku_female_4.png', text: 'Female 4', imgSrc: '/img/profiles/haiku_female_4.png' },
        { value: 'haiku_female_5.png', text: 'Female 5', imgSrc: '/img/profiles/haiku_female_5.png' },
        { value: 'haiku_female_6.png', text: 'Female 6', imgSrc: '/img/profiles/haiku_female_6.png' },
        { value: 'haiku_female_7.png', text: 'Female 7', imgSrc: '/img/profiles/haiku_female_7.png' },
        { value: 'haiku_female_8.png', text: 'Female 8', imgSrc: '/img/profiles/haiku_female_8.png' },
        { value: 'haiku_female_9.png', text: 'Female 9', imgSrc: '/img/profiles/haiku_female_9.png' },
        { value: 'haiku_female_10.png', text: 'Female 10', imgSrc: '/img/profiles/haiku_female_10.png' },
        { value: 'haiku_female_11.png', text: 'Female 11', imgSrc: '/img/profiles/haiku_female_11.png' },
        { value: 'haiku_female_12.png', text: 'Female 12', imgSrc: '/img/profiles/haiku_female_12.png' },
        { value: 'haiku_female_13.png', text: 'Female 13', imgSrc: '/img/profiles/haiku_female_13.png' },
        { value: 'haiku_female_14.png', text: 'Female 14', imgSrc: '/img/profiles/haiku_female_14.png' },
        { value: 'haiku_female_15.png', text: 'Female 15', imgSrc: '/img/profiles/haiku_female_15.png' },
        { value: 'haiku_female_16.png', text: 'Female 16', imgSrc: '/img/profiles/haiku_female_16.png' },
        { value: 'haiku_female_17.png', text: 'Female 17', imgSrc: '/img/profiles/haiku_female_17.png' },
        { value: 'haiku_female_18.png', text: 'Female 18', imgSrc: '/img/profiles/haiku_female_18.png' },
        { value: 'haiku_female_20.png', text: 'Female 20', imgSrc: '/img/profiles/haiku_female_20.png' },
        { value: 'haiku_male_1.png', text: 'Male 1', imgSrc: '/img/profiles/haiku_male_1.png' },
        { value: 'haiku_male_2.png', text: 'Male 2', imgSrc: '/img/profiles/haiku_male_2.png' },
        { value: 'haiku_male_3.png', text: 'Male 3', imgSrc: '/img/profiles/haiku_male_3.png' },
        { value: 'haiku_male_4.png', text: 'Male 4', imgSrc: '/img/profiles/haiku_male_4.png' },
        { value: 'haiku_male_5.png', text: 'Male 5', imgSrc: '/img/profiles/haiku_male_5.png' },
        { value: 'haiku_male_6.png', text: 'Male 6', imgSrc: '/img/profiles/haiku_male_6.png' },
        { value: 'haiku_male_7.png', text: 'Male 7', imgSrc: '/img/profiles/haiku_male_7.png' },
        { value: 'haiku_male_8.png', text: 'Male 8', imgSrc: '/img/profiles/haiku_male_8.png' },
        { value: 'haiku_male_9.png', text: 'Male 9', imgSrc: '/img/profiles/haiku_male_9.png' },
        { value: 'haiku_male_10.png', text: 'Male 10', imgSrc: '/img/profiles/haiku_male_10.png' },
        { value: 'haiku_male_11.png', text: 'Male 11', imgSrc: '/img/profiles/haiku_male_11.png' },
        { value: 'haiku_male_12.png', text: 'Male 12', imgSrc: '/img/profiles/haiku_male_12.png' },
        { value: 'haiku_male_13.png', text: 'Male 13', imgSrc: '/img/profiles/haiku_male_13.png' },
        { value: 'haiku_male_14.png', text: 'Male 14', imgSrc: '/img/profiles/haiku_male_14.png' },
        { value: 'haiku_male_15.png', text: 'Male 15', imgSrc: '/img/profiles/haiku_male_15.png' },
        { value: 'haiku_male_16.png', text: 'Male 16', imgSrc: '/img/profiles/haiku_male_16.png' },
        { value: 'haiku_male_17.png', text: 'Male 17', imgSrc: '/img/profiles/haiku_male_17.png' },
        { value: 'haiku_male_18.png', text: 'Male 18', imgSrc: '/img/profiles/haiku_male_18.png' },
        { value: 'haiku_male_19.png', text: 'Male 19', imgSrc: '/img/profiles/haiku_male_19.png' },
        { value: 'haiku_male_20.png', text: 'Male 20', imgSrc: '/img/profiles/haiku_male_20.png' },
        { value: 'haiku_male_21.png', text: 'Male 21', imgSrc: '/img/profiles/haiku_male_21.png' },
        { value: 'haiku_male_22.png', text: 'Male 22', imgSrc: '/img/profiles/haiku_male_22.png' },
    ];

    useEffect(() => {
        if (profile && !isNewProfile) {
            setName(profile.name);
            setRoleUuid(profile.role_uuid);
            setAvatar(profile.avatar);
            setDescription(profile.description);
            setWelcomeMessage(profile.welcome_message);
        } else {
            // Reset fields for new profile
            setName('');
            setRoleUuid('');
            setAvatar('');
            setDescription('');
            setWelcomeMessage('');
        }
    }, [profile, isNewProfile]);

    const handleRoleChange = newRoleUuid => {
        setRoleUuid(newRoleUuid);
    };

    const handleAvatarChange = newAvatar => {
        setAvatar(newAvatar);
    };

    return (
        <Modal show={show} onHide={onHide}>
            <Modal.Header closeButton>
                <Modal.Title>{isNewProfile ? 'Add New Profile' : 'Edit Profile'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3" controlId="profileName">
                        <Form.Label>Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group>
                        <RoleSelector
                            roles={roles}
                            selectedRoleUuid={roleUuid}
                            onChange={handleRoleChange}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>Image</Form.Label>
                        <ImageDropdown
                            options={avatarOptions}
                            onChange={handleAvatarChange}
                            initialSelectedImage={profile ? "/img/profiles/" + profile.avatar : ''}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="profileDescription">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={3}
                            placeholder="Enter description"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="profileWelcomeMessage">
                        <Form.Label>Welcome Message</Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={3}
                            placeholder="Enter welcome message"
                            value={welcomeMessage}
                            onChange={(e) => setWelcomeMessage(e.target.value)}
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer className="justify-content-start">
                {profile ? (
                    <>
                        <Button variant="danger" onClick={() => onDelete(profile)}>Delete</Button>
                        <div className="ms-auto">
                            <Button variant="secondary" onClick={onHide} className="me-2">
                                Close
                            </Button>
                            <Button variant="primary" onClick={() => onSave(profile, {name, roleUuid, avatar, description, welcomeMessage})}>
                                Save Changes
                            </Button>
                        </div>
                    </>
                ) : (
                    <Button variant="primary" onClick={() => onSave(null, {name, roleUuid, avatar, description, welcomeMessage})}>
                        Add
                    </Button>
                )}
            </Modal.Footer>
        </Modal>
    );
}

export default EditProfileModal;
