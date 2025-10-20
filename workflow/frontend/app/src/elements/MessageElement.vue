<template>
    <div :class="this.isMsgFromUser?'userMsg msgBody':'otherMsg msgBody'">
        <div class="msg-heading">
            <p v-if="messageData.msgSenderObj">{{ this.messageData.msgSenderObj.firstname }} {{ this.messageData.msgSenderObj.lastname }}</p>
            <p v-else>Loading sender data...</p>
        </div>
        <div class="msg-content">
            <p>{{ this.messageData.msgContent }}</p>
        </div>
        <div class="msg-footer">
            <p>{{ this.messageData.msgDate }}</p>
        </div>
    </div>
</template>

<script>
export default{
    props:{
        messageData:Object,
    },
    data(){
        return{
            currentUserEmail:localStorage.getItem("userEmail"),
        }
    },
    computed:{
        isMsgFromUser(){
            if (this.messageData.msgSenderObj.email == this.currentUserEmail){
                return true
            } else{
                return false
            }
        }
    }
}
</script>

<style scoped>
.msgBody{
    border-radius: 8px;
    display:block;
    width:60%;
    padding-bottom: 4px;
}

.userMsg{
    background-color: rgb(26, 216, 137);
    margin-left: auto;
    text-align: right;
}

.otherMsg{
    background-color: rgb(39, 158, 255);
    margin-right: auto;
    text-align: left;
}

.msg-heading{
    font-size: 16px;
    font-weight: bold;
}

.msg-content{
    font-size:18px;
}   

.msg-footer{
    font-size:10px;
}
</style>