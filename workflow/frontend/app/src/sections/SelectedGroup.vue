<template>
    <div id="loading-page" v-if="!isContentLoaded">
        <div id="loading-wrapper">
            <div id="loading-content">
                <h1>Loading...</h1>
            </div>
        </div>
    </div>
    <div id="group-header">
        <p id="group-name">{{ this.groupData.name }}</p>
        <button id="change-tool-btn" @click="isChatOpen=!isChatOpen">{{ isChatOpen ? "View files" : "Go to chat"}}</button>
    </div>
    <div id="group-body">
        <GroupMessager @sent-message="(msgObj)=>sendMessage(msgObj)" :all-messages="this.groupMessages"/>
    </div>
</template>

<script>
import GroupMessager from './GroupMessager.vue';
import { getDBformatDate } from '@/utils/datetime';



export default{
    props:[
        "groupData",
        "userData"
    ],
    components:{
        GroupMessager
    },
    data(){
        return{
            isChatOpen:true,
            groupMessages: [],
            socket: null,
            isContentLoaded:true,
            newMsg:"",
            storedMsgs:[]
        }
    },
    watch:{
        groupData(){
            if (this.socket && this.socket.readyState === WebSocket.OPEN) {
                console.log("closing wb connection...")
                this.groupMessages = []
                this.socket.close();
                this.initializeSocket()
            }
        }
    },
    methods:{
        sendMessage(messageContent) {
            const currentDate = new Date()
            const formattedDate = getDBformatDate(currentDate)
            const message = { type: 'message', content: messageContent, sender:this.userData.userid, datesent: formattedDate};
            this.socket.send(JSON.stringify(message));
        },
        initializeSocket() {
            const websocketUrl = window.location.hostname + ':3000';
            this.socket = new WebSocket(`ws://${websocketUrl}`);

            // When the WebSocket opens, send the join message
            this.socket.onopen = () => {
                const groupInfo = { type: 'join', group: this.groupData.groupid, user:this.userData.userid };
                this.socket.send(JSON.stringify(groupInfo));
            };

            // Handle incoming messages from the WebSocket server
            this.socket.onmessage = (event) => {
                const wsMessage = JSON.parse(event.data);
                if (wsMessage.type === 'message') {
                    console.log('Received chat message:', wsMessage.content);
                    this.groupMessages.push(wsMessage)
                } else if (wsMessage.type === 'info') {
                    console.log(wsMessage.message); 
                } else if (wsMessage.type === 'database') {
                    wsMessage.message.forEach(element => {
                        this.groupMessages.push(element)
                    });
                }
            };  
        },
    },
    mounted() {
        this.initializeSocket()
    },
    beforeUnmount(){
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            console.log("closing wb connection...")
            this.socket.close();
        }
    }
}
</script>

<style scoped>
#loading-page{
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity 0.3s ease;
}

#loading-wrapper {
    display: table-cell;
    vertical-align: middle;
}

#loading-content{
    width: 20%;
    height: 20%;
    margin: 0px auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    font-family: Helvetica, Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center; 
}

#group-name{
    display: inline;
    font-size:24px;
    padding-left: 10px;
    position: absolute;
    left:0;
}

#change-tool-btn{
    padding:20px;
    background-color: inherit;
    cursor:pointer;
    font-size:18px;
    background-color: white;
    position: absolute;
    right:0;
}

#change-tool-btn:hover{
    background-color: rgb(221, 221, 221);
}

#group-header {
    border: 1px solid black;
    padding: 15px 0 10px 0;
    width: 100%;
    height: 80px; /* Fixed height for the header */
    background-color: rgb(162, 209, 255);
    position: relative;
}

#group-body {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;

    overflow-y: auto;   
    height: 100%; 
}
</style>