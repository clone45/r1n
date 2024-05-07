import React from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const NavBar = ({ handleOpenLoadTeamModal, handleDismissTeam }) => {
  return (
<Navbar className="fixed-top primary-navbar" bg="light">
  <Navbar.Brand href="#" className="brand-label">r1n.ai</Navbar.Brand>
  <Nav className="me-auto">
    {/* Chat Icon positioned on the left */}
    <Link to="/" className="btn btn-light chat-icon-button">
      <i className="fas fa-comments"></i>
    </Link>
  </Nav>
  <Nav className="justify-content-end">
    {/* Users Dropdown positioned on the right */}
    <NavDropdown align="end" title={<i className="fas fa-cog"></i>} id="nav-settings" >
      <NavDropdown.Item as={Link} to="/manage-teams">Manage Teams</NavDropdown.Item>
      <NavDropdown.Item as={Link} to="/manage-profiles">Manage Profiles</NavDropdown.Item>
      <NavDropdown.Divider />
      <NavDropdown.Item onClick={handleOpenLoadTeamModal}>Load Team</NavDropdown.Item>
    </NavDropdown>
  </Nav>
</Navbar>

  );
};

export default NavBar;
