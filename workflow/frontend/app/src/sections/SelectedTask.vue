<template>
    <div :class="taskStyle">
        <p class="task-title">{{ taskData["title"] }}</p>
        <p class="task-content">{{ taskData["content"] }}</p>
        <p class="task-date">Due on: {{ taskData["duedate"] }}</p>
        <p class="task-date">Sent on: {{ taskData["sentdate"] }}</p>
        <p class="task-sender">Sent by: {{ taskData["sender"] }}</p>
        <div v-if="isCompleted">
            <p class="task-completed" v-if="isCompleted">This task is completed</p>
            <button class="task-toggle-btn" @click="makeTaskImcomplete">Mark as imcompleted</button>
        </div>
        <div v-if="!isCompleted">
            <p class="task-imcomplete" v-if="!isCompleted">This task is not completed</p>
            <button class="task-toggle-btn" @click="makeTaskComplete">Mark as completed</button>
        </div>
        
        
        
    </div>
</template>

<script>
export default{
    name:"SelectedTask",
    props:[
        "taskData"
    ],
    emits:[
        "toggle-task"
    ],
    data(){
        return{

        }
    },
    computed:{
        isCompleted(){
            return this.taskData["status"] === "T" ? true : false
        },
        taskStyle(){
            if(this.taskData["status"]=="F"){
                return "task-imcomplete"
            } else{
                return "task-complete"
            }
        }
    },
    methods:{
        makeTaskImcomplete(){
            this.$emit('toggle-task',false)
        },
        makeTaskComplete(){
            this.$emit('toggle-task',true)
        }
    }
}
</script>

<style scoped>
.task-complete{
    font-family: 'Lucida Sans';
    background-color: rgb(228, 255, 245);
    height:100%;
}

.task-imcomplete{
    font-family: 'Lucida Sans';
    background-color: rgb(255, 231, 228);
    height:100%;
}

.task-title{
    font-size: 32px;
    font-weight: bold;
}

.task-content{
    font-size:28px;
    padding-bottom: 10px;
}

.task-completed{
    color:green;
}

.task-imcomplete{
    color:red;
}

.task-toggle-btn{
    background-color:rgb(3, 180, 3);
    color:white;
    border: none;
    border-radius: 6px;
    padding:16px;
    font:large;
    cursor:pointer;
}

p{
    color:black;
}
</style>