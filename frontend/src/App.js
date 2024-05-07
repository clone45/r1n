import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import NavBar from "./components/NavBar";
import LowerNavBar from './components/LowerNavBar';
import TeamSelectionModal from "./components/TeamSelectionModal";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Chat from "./components/Chat";
import ManageTeams from './components/ManageTeams';
import ManageProfiles from './components/ManageProfiles';

function App() {
    const [socket, setSocket] = useState(null);
    const [agents, setAgents] = useState([]); // The loaded agents in the chat
    const [loadingCount, setLoadingCount] = useState(0);
    const [selectedAgent, setSelectedAgent] = useState(null);
    const [messages, setMessages] = useState([]);
    const [teams, setTeams] = useState([]);
    const [profiles, setProfiles] = useState([]); // Available profiles
    const [roles, setRoles] = useState([]);
    const [showModal, setShowModal] = useState(false);

    // Here's why this is localhost:4000.  Typically, if this container was within the
    // docker network, it would use the other container's name.  For example, http://node-backend:4000
    // However, code running in the browser runs outside of the docker network, so it can't use the container name.
    // Instead, it uses localhost:4000, which is the port that the backend is exposed on the host machine.

    const apiBaseUrl = "http://localhost:4000";

    console.log("API Base URL:", apiBaseUrl);
    console.log("process.env.NODE_BACKEND_URL:", process.env.NODE_BACKEND_URL);

    const handleNewMessage = (newMessage) => {
        setMessages((prevMessages) => [...prevMessages, newMessage]);
    };

    const handleOpenLoadTeamModal = async () => {
        setShowModal(true);
    };

    const handleLoadTeam = async (uuid, number_of_team_members) => {
        console.log("Loading team:", uuid);

        // First, remove any existing agents
        setAgents([]);
        setSelectedAgent(null);
        setMessages([]);

        // Dismiss the current team if one is active
        await handleDismissTeam();

        setLoadingCount(number_of_team_members);

        try {
            // TODO: Is there a possible issue here where the response from the launch
            // request will return after the agents have already checked in?

            const response = await fetch(`${apiBaseUrl}/team/${uuid}/launch`, {
                method: "POST",
            });

            if (!response.ok) {
                throw new Error("Failed to launch team");
            }

            const data = await response.json();
            setShowModal(false);
        } catch (error) {
            console.error("Failed to launch team:", error);
        }
    };

    const handleDismissTeam = async () => {
        console.log("Dismissing team...");

        // Check to see if there are any agents
        if (agents.length > 0) {
            // Use a dialog box to confirm the dismissal
            const confirmDismiss = window.confirm(
                "Are you sure you want to dismiss the team?"
            );

            if (confirmDismiss) {
                try {
                    const response = await fetch(`${apiBaseUrl}/team/dismiss`, {
                        method: "POST",
                    });
                    if (!response.ok) {
                        throw new Error("Failed to dismiss team");
                    }
                } catch (error) {
                    console.error("Failed to dismiss team:", error);
                }
            } else {
                console.log("Dismissal cancelled by user");
            }
        }
    };

    useEffect(() => {
        const fetchTeams = async () => {
            console.log("Fetching team list at startup...");
            try {
                // TODO: This isn't really calling the API to get the teams.  It's
                // using the old method of making an additional request to agent_manager in order
                // to get the profiles attached to the teams.  I'll need to update this.
                const response = await fetch(`${apiBaseUrl}/api/teams`);
                if (!response.ok) {
                    throw new Error("Failed to fetch teams");
                }
                const teamsData = await response.json();
                setTeams(teamsData);

                console.log("Teams loaded at startup:", teamsData);

            } catch (error) {
                console.error("Failed to load teams at startup:", error);
            }
        };
    
        fetchTeams();
    }, []); // The empty array ensures this runs only once on mount.

    // Fetch all profiles
    useEffect(() => {
        const fetchProfiles = async () => {
            console.log("Fetching all profiles...");
            try {
                const response = await fetch(`${apiBaseUrl}/api/profiles`);
                if (!response.ok) {
                    throw new Error(`Failed to fetch profiles: ${response.status} ${response.statusText}`);
                }
                const profilesData = await response.json();
                setProfiles(profilesData);

                console.log("Profiles loaded at startup:", profilesData);

            } catch (error) {
                console.error("Failed to load profiles:", error);
            }
        };

        fetchProfiles();
    }, []);

    useEffect(() => {
        const fetchRoles = async () => {
            console.log("Fetching all roles...");
            try {
                const response = await fetch(`${apiBaseUrl}/api/roles`);
                if (!response.ok) {
                    throw new Error(`Failed to fetch roles: ${response.status} ${response.statusText}`);
                }
                const rolesData = await response.json();
                setRoles(rolesData);

                console.log("Roles loaded at startup:", rolesData);

            } catch (error) {
                console.error("Failed to load roles:", error);
            }
        };

        fetchRoles();
    }, []);


    useEffect(() => {
        // Set up the WebSocket connection
        const newSocket = io(apiBaseUrl);
        console.log("Attempting to connect", newSocket);
        setSocket(newSocket);

        setLoadingCount(0);

        newSocket.on("connect", async () => {
            // The socket is now connected, proceed to notify the server
            console.log("WebSocket connected, notifying server UI is ready");
            try {
                const response = await fetch(`${apiBaseUrl}/ui-ready`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }

                // Handle response here if needed
            } catch (error) {
                console.error("Error notifying server:", error);
            }
        });

        newSocket.on("FromServer", (messageStr) => {
            const msg = JSON.parse(messageStr);

            // Logic for handling different message types
            switch (msg.message_type) {
                // ====  ui.add_agent ====
                case "ui.add_agent": {
                    console.log(msg.content);

                    const {
                        name,
                        queue,
                        role,
                        avatar,
                        profile,
                        instance_uuid,
                    } = JSON.parse(msg.content);
                    setAgents((prevAgents) => {
                        // Decrement loading count
                        setLoadingCount((prevCount) =>
                            Math.max(0, prevCount - 1)
                        );

                        const existingAgent = prevAgents.find(
                            (agent) => agent.queue === queue
                        );

                        console.log("role", role);

                        if (!existingAgent) {
                            let new_agent = {
                                name: name,
                                queue: queue,
                                role: role,
                                profile: profile,
                                instance_uuid: instance_uuid,
                                isThinking: false,
                            };

                            // Add new agent
                            const updatedAgents = [...prevAgents, new_agent];

                            if (updatedAgents.length === 1) {
                                // This is essentially creating agent object and setting it as the elected agent
                                // Note that the agent object here is missing a lot of properties, such as avatar, profile, capabilities, etc.
                                setSelectedAgent(new_agent);
                            }
                            return updatedAgents;
                        }
                    });
                    break;
                }

                // ====  ui.remove_agent ====
                case "ui.remove_agent": {
                    const { name, queue } = JSON.parse(msg.content);
                    setAgents((prevAgents) =>
                        prevAgents.filter((agent) => agent.queue !== queue)
                    );
                    break;
                }

                case "ui.agent_thinking_started": {
                    const { name, queue } = JSON.parse(msg.content);
                    setAgents((prevAgents) =>
                        prevAgents.map((agent) => {
                            if (
                                agent.profile.name === name &&
                                agent.queue === queue
                            ) {
                                return { ...agent, isThinking: true };
                            }
                            return agent;
                        })
                    );
                    break;
                }

                case "ui.agent_thinking_completed": {
                    const { name, queue } = JSON.parse(msg.content);
                    setAgents((prevAgents) =>
                        prevAgents.map((agent) => {
                            if (
                                agent.profile.name === name &&
                                agent.queue === queue
                            ) {
                                return { ...agent, isThinking: false };
                            }
                            return agent;
                        })
                    );
                    break;
                }

                // ====  message ====
                case "message": {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        {
                            from_name: msg.from_name,
                            from_queue: msg.from_queue,
                            from_persona: msg.from_persona,
                            to_name: msg.to_name,
                            to_queue: msg.to_queue,
                            to_persona: msg.to_persona,
                            cc_queue: msg.cc_queue,
                            content: msg.content,
                            message_type: msg.message_type,
                            timestamp: msg.timestamp,
                        },
                    ]);
                    console.log("Message received via websocket:", msg);
                    break;
                }

                default:
                // Handle other message types or default case
            }
        });

        return () => {
            // Clean up the WebSocket connection on unmount
            newSocket.close();
        };
    }, []); // Empty dependency array means this runs once on mount

    return (
        <Router>
            <div className="container-fluid app-container">
                <NavBar
                    handleOpenLoadTeamModal={handleOpenLoadTeamModal}
                    handleDismissTeam={handleDismissTeam}
                />
                <Routes>
                    <Route path="/" element={
                        <Chat
                            agents={agents}
                            selectedAgent={selectedAgent}
                            messages={messages}
                            loadingCount={loadingCount}
                            apiBaseUrl={apiBaseUrl}
                            setSelectedAgent={setSelectedAgent}
                            handleOpenLoadTeamModal={
                                handleOpenLoadTeamModal
                            }
                            handleNewMessage={handleNewMessage}
                        />
                    } />

                    <Route path="/manage-teams" element={
                        <ManageTeams 
                            teams={teams}
                            apiBaseUrl={apiBaseUrl}
                            setTeams={setTeams}
                            profiles={profiles}
                        />
                    } />

                    <Route path="/manage-profiles" element={
                        <ManageProfiles 
                            profiles={profiles}
                            apiBaseUrl={apiBaseUrl}
                            setProfiles={setProfiles}
                            roles={roles}
                        />
                    } />

                </Routes>
                <TeamSelectionModal
                    teams={teams}
                    showModal={showModal}
                    onClose={() => setShowModal(false)}
                    onLoadTeam={handleLoadTeam}
                />
            </div>
        </Router>
    );
}

export default App;
