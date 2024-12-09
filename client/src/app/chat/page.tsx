
"use client"
import React, { useState, ChangeEvent, KeyboardEvent } from "react";
import axios from "axios";
import LoadingModal from "../components/LoadingModal";

interface Message {
    id: number;
    sender: "Agent" | "User";
    text: string;
}

const ChatApp: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, sender: "Agent", text: "Hi there! I'm your AI-powered assistant for all things insurance-related. How can I help you today? Whether you need information on your policy, claim status, or anything else, just let me know!" },
    ]);

    const [newMessage, setNewMessage] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);


    const handleInputChange = (e: ChangeEvent<HTMLInputElement>): void => {
        setNewMessage(e.target.value);
    };

    const handleSendMessage = (): void => {
        if (newMessage.trim() === "") return;
        setMessages((prevMessages) => [
            ...prevMessages,
            { id: prevMessages.length + 1, sender: "User", text: newMessage },
        ]);

        getAgentResponse(newMessage);
        setNewMessage(""); 
    };

    const getAgentResponse = async (message: string) : Promise<string | undefined> => {
        try {
            
            setIsLoading(true)
            const response = await axios.post('http://localhost:8000/chat',{
                message
            } , {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            console.log('Response data:', response.data.payload.output);
    
            setMessages((prevMessages) => [
                ...prevMessages,
                { id: prevMessages.length + 1, sender: "Agent", text: response.data.payload.output },
            ]);
    
            return response.data;

        } catch (error) {
            alert(error)
        }
        finally{
            setIsLoading(false)
        }
    }

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>): void => {
        if (e.key === "Enter") handleSendMessage();
    };

    return (
        <div className="container my-3">
            <LoadingModal isLoading={isLoading} message="" />
            <div className="card">
                <div className="card-header text-center">
                    <h5>Chat</h5>
                </div>
                <div className="card-body" style={{ maxHeight: "600px", overflowY: "auto" }}>
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`d-flex mb-2 ${message.sender === "User" ? "justify-content-end" : "justify-content-start"
                                }`}
                        >
                            <div
                                className={`p-2 rounded ${message.sender === "User" ? "bg-light text-dark" : "bg-primary text-white"
                                    }`}
                                style={{ maxWidth: "60%" }}
                            >
                                <small className="d-block">
                                    <strong>{message.sender}</strong>
                                </small>
                                <span>{message.text}</span>
                            </div>
                        </div>
                    ))}
                </div>
                <div className="card-footer d-flex">
                    <input
                        type="text"
                        className="form-control me-2"
                        placeholder="Type your message..."
                        value={newMessage}
                        onChange={handleInputChange}
                        onKeyDown={handleKeyDown}
                    />
                    <button className="btn btn-primary" onClick={handleSendMessage}>
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatApp;
