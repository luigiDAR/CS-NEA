<template>
    <div :class="taskStyle" >
        <p class="task-title">{{ taskData["title"] }}</p> 
        <p class="task-sender">From: {{ taskData["sender"] }}</p>
        <p class="task-deadline">Due on: {{ taskData["duedate"] }}</p>
    </div>
</template>

<script>
export default{
    name:"TaskButton",
    props:[
        "taskData"
    ],
    computed:{
        taskStyle(){
            if(this.taskData["status"]=="F"){
                return "task-imcomplete"
            } else{
                return "task-complete"
            }
        }
    }
}
</script>

<style scoped>
.task-complete{
    border: 1px solid black;
    background-color: rgb(225, 255, 227);
    padding-top: 8px;
}

.task-imcomplete{
    border: 1px solid black;
    background-color: rgb(255, 225, 225);
    padding-top: 8px;
}

.complete-task-btn{
    padding:16px;
    display: inline;
    cursor:pointer;
    background-color: white;
}

.task-title{
    font-weight: bold;
}

p{
    font-size: large;
}
</style>