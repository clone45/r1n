import React from 'react';
import { Container, Nav, Navbar } from 'react-bootstrap';

const LowerNavBar = () => {
    return (
        <Navbar fixed="bottom" bg="dark" className="shadow">
            <Container>
                <Navbar.Brand href="#" className="brand-label">1n.ai</Navbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link href="#home">Home</Nav.Link>
                    <Nav.Link href="#features">Features</Nav.Link>
                    <Nav.Link href="#pricing">Pricing</Nav.Link>
                    <Nav.Link href="#about">About</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default LowerNavBar;
