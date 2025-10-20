const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const axios = require('axios')

// Create an Express app
const app = express();

// Create an HTTP server
const server = http.createServer(app);

// Create WebSocket server and attach to HTTP server
const wss = new WebSocket.Server({ server });

// Store clients by group
const groups = {};


// Handle new WebSocket connections
wss.on('connection', (ws) => {
    let currentGroup = null;
    let currentUser = null;

    // ws represents the client connection
    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            
            // First message is assumed to be the group join message
            if (data.type === 'join' && data.group) {
                currentGroup = data.group;
                currentUser = data.user
                
                // Initialize group if it doesn't exist
                if (!groups[currentGroup]) {
                    groups[currentGroup] = [];
                }

                // Add this connection to the group
                groups[currentGroup].push(ws);
                getAllMessagesInDb(currentGroup,ws)
                console.log(`User${currentUser} joined Group#${currentGroup}`);
                
                // Send a confirmation message
                ws.send(JSON.stringify({ type: 'info', message: `Joined group ${currentGroup}` }));
            }

            // Subsequent messages are chat messages
            else if (data.type === 'message' && currentGroup) {
                // Broadcast to everyone in the same group
                storeMessageInDB(currentGroup,data,ws).then(()=>{
                    insertSenderDetails([data]).then(()=>{
                        broadcastToGroup(currentGroup, data);
                    })
                })
            } else {
                console.log('Invalid message type or group not set');
            }
        } catch (err) {
            console.error('Error parsing message:', err);
        }
    });

    // Handle client disconnect
    ws.on('close', () => {
        if (currentGroup && groups[currentGroup]) {
            const index = groups[currentGroup].indexOf(ws);
            if (index !== -1) {
                groups[currentGroup].splice(index, 1); // Remove the client from the group
                console.log(`User disconnected from group ${currentGroup}`);
            }
        }
    });

    // Handle errors
    ws.on('error', (error) => {
        console.error('WebSocket error:', error);
    });
});

// Broadcast a message to all clients in the given group
function broadcastToGroup(group, message) {
    if (groups[group]) {
        groups[group].forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({ type: 'message', content: message.content, sender:message.sender, sentdate:message.datesent }));
            }
        });
    }
}

async function storeMessageInDB(group,message,client){
    //message should be an object with content, sender and sent date
    axios.post('http://192.168.1.62:5000/messages',{
        operation:'storenewmessage',
        content:{
            group:group,
            content:message.content,
            sender:message.sender,
            sentdate:message.datesent
        }
    }).then((response)=>{
        client.send(JSON.stringify({ type: 'info', message: response.data }));
    }).catch((error)=>{
        console.log("Error storing new message:",error)
    })
}

async function getAllMessagesInDb(group,client){
    axios.post('http://192.168.1.62:5000/messages',{
        operation:"getallmessages",
        content:group
    })
    .then((response)=>{
        insertSenderDetails(response.data).then(()=>{
            console.log(response.data)
           client.send(JSON.stringify({ type: 'database', message: response.data })); 
        })
        
    })
    .catch((error)=>{
        console.log("Error:",error)
    })
}

async function getSenderData(senderId) {
    try {
        const response = await axios.post('http://192.168.1.62:5000/handleuser', {
            operation: "getuseremail",
            content: senderId
        });
        return response.data;
    } catch (error) {
        console.log("Error:", error);
    }
}

async function insertSenderDetails(arrayOfMessages){
    for (let msg of arrayOfMessages){
        msg.sender = await getSenderData(msg.sender)
    }
}



// Start the server
server.listen(3000, '0.0.0.0', () => {
    console.log('WebSocket server listening on port 3000');
  });
