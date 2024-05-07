import React from 'react';
import { Form } from 'react-bootstrap';

function RoleSelector({ roles, selectedRoleUuid, onChange }) {
    return (
        <Form.Group className="mb-3" controlId="profileRole">
            <Form.Label>Role</Form.Label>
            <Form.Control as="select" value={selectedRoleUuid} onChange={e => onChange(e.target.value)}>
                <option value="">Select a role</option>
                {roles.map(role => (
                    <option key={role.uuid} value={role.uuid}>
                        {role.name}
                    </option>
                ))}
            </Form.Control>
        </Form.Group>
    );
}

export default RoleSelector;
