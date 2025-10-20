<template>
    <div id="message-display" ref="msgContent">
        <ul >
            <li v-for="(msg,index) in allMessages" :key="index">
                <MessageElement :message-data="{
                    msgContent:msg.content,
                    msgSenderObj:msg.sender,
                    msgDate:msg.sentdate,
                }" />
            </li>
        </ul>
    </div>
        
    <div id="message-bar">
        <input v-model="message" @keyup.enter="sendNewMessage">
        <button @click="sendNewMessage">Send</button>
    </div>
</template>

<script>
import MessageElement from '@/elements/MessageElement.vue';

export default{
    name:"GroupMessager",
    components:{
        MessageElement
    },
    props:{
        allMessages:Object,
    },
    emits:[
        "sent-message"
    ],
    data(){
        return{
            message:'',
            
        }
    },
    watch: {
        'allMessages.messageArray': {
            handler() {
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            },
            deep: true
        }
    },
    methods:{
        sendNewMessage(){
            if (this.message != ""){
                this.$emit('sent-message',this.message)
                this.message = ''
            } else {
                alert("You can't send empty messages.")
            }
            
        },
        scrollToBottom() {
            const content = this.$refs.msgContent;
            if (content) {
                content.scrollTop = content.scrollHeight;
            }
        },
    }
}
</script>

<style scoped>
li{
    list-style-type:none;
    position: relative;
}

input{
    display: inline;
    margin-right: 10px;
    border-radius: 10px;
    padding:12px;
}

button{
    display: inline;
    padding:20px;
    background-color: green;
    color: white;
    border:none;
    border-radius: 8px;
    width:10%;
}

#message-display{
    background-color: rgb(230, 230, 230);
    overflow-y: auto;
}

#message-bar{
    background-color: rgb(162, 209, 255);
    height: 70px;
}
</style>