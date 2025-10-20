<template>
    <div id="task-page">
        <NewTaskModal v-if="showModal" @close="(n)=>{this.handleModal(n); showModal=false;}" />
        <div id="task-sidebar">
            <p id="sidebar-heading">Tasks</p>
            <hr>
            <div id="options">
                <button v-if="userData.role!='W'" class="task-btn" style="width:100%;" @click="showModal=true">Create task</button>
                <button class="task-btn" @click="showOnlyCompleted=false">To-do</button>
                <button class="task-btn" @click="showOnlyCompleted=true">Completed</button>
            </div>
            <ul v-if="!showOnlyCompleted">
                <li  v-for="(task,index) in allTasks" :key="index">
                    <TaskButton v-if="task.status == 'F'" style="cursor:pointer;" @click="selectTask(index)" :task-data="{
                        title:task.title,
                        content:task.content,
                        sender:task.sender,
                        sentdate:task.sentdate,
                        duedate:task.duedate,
                        status:task.status
                    }" />
                </li>
            </ul>
            <ul v-else>
                <li v-for="(task,index) in allTasks" :key="index">
                    <TaskButton v-if="task.status == 'T'" style="cursor:pointer;" @click="selectTask(index)" :task-data="{
                        title:task.title,
                        content:task.content,
                        sender:task.sender,
                        sentdate:task.sentdate,
                        duedate:task.duedate,
                        status:task.status
                    }" />
                </li>
            </ul>
        </div>
        <div id="task-main">
            <SelectedTask @toggle-task="(newStatus)=>this.toggleSelectedToggle(newStatus)" v-if="showSelectedTask" :task-data="{
                title:selectedTaskData.title,
                content:selectedTaskData.content,
                sender:selectedTaskData.sender,
                sentdate:selectedTaskData.sentdate,
                duedate:selectedTaskData.duedate,
                status:selectedTaskData.status
            }"/>
            <h1 v-else>Hello {{ userData.firstname }}, how you doing?</h1>
        </div>
    </div>
</template>

<script>
import NewTaskModal from '@/modals/NewTaskModal.vue'
import SelectedTask from '@/sections/SelectedTask.vue'
import TaskButton from '@/elements/TaskButton.vue'
import axios from 'axios'

export default{
    name:'TaskPage',
    props:[
        "userData"
    ],
    components:{
        SelectedTask,
        TaskButton,
        NewTaskModal
    },
    data(){
        return{
            allTasks:[],
            showSelectedTask:false,
            showOnlyCompleted:false, 
            selectedTaskId:undefined,
            showModal:false,
            newTask:{
                title:"",
                content:"",
                duedate:"",
                sentdate:"",
                receiverFirstname:"",
                receiverLastname:"",
                sender:localStorage.getItem("userEmail")
            },
            newStatus:undefined
        }
    },
    computed:{
        selectedTaskData(){
            if (this.selectedTaskId === undefined){
                return undefined
            } else{
                return {
                    title:this.allTasks[this.selectedTaskId].title,
                    content:this.allTasks[this.selectedTaskId].content,
                    sender:this.allTasks[this.selectedTaskId].sender,
                    sentdate:this.allTasks[this.selectedTaskId].sentdate,
                    duedate:this.allTasks[this.selectedTaskId].duedate,
                    status:this.allTasks[this.selectedTaskId].status
                }
            }
        }
    },
    methods:{
        //get all the tasks related to this user
        async getTasks(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/tasks`,{
                operation:"getalltasks",
                content:localStorage.getItem("userEmail")
            })
            .then((response)=>{
                this.allTasks = response.data
            })
            .catch((error)=>{
                console.log("Error:",error)
            })
        },
        async createTask(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/tasks`,{
                operation:"createnewtask",
                content: this.newTask
            })
            .then((response)=>{
                console.log(response["data"])
            })
            .catch((error)=>{
                console.error("Error sending data:",error)
            })
        },
        async updateTaskStatus(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/tasks`,{
                operation:"updatetaskstatus",
                content:{
                    title:this.selectedTaskData.title,
                    newStatus:this.newStatus
                }
            })
            .then((response)=>{
                console.log(response["data"])
            })
            .catch((error)=>{
                console.error("Error sending data:",error)
            })
        },
        selectTask(taskIndex){
            this.selectedTaskId = taskIndex
            this.showSelectedTask = true
        },
        toggleSelectedToggle(nStatus){
            if (nStatus){
                this.newStatus = "T"
                this.updateTaskStatus()
                this.getTasks()
            } else {
                this.newStatus = "F"
                this.updateTaskStatus()
                this.getTasks()
            }
        },
        handleModal(n){
            if (n!=="cancel"){
                this.newTask.title = n["title"]
                this.newTask.content = n["content"]
                const dateObject = new Date()
                const sentDate = `${dateObject.getFullYear()}-${dateObject.getMonth()+1}-${dateObject.getDate()} ${dateObject.getHours()}:${dateObject.getMinutes()}:${dateObject.getSeconds()}`
                this.newTask.sentdate = sentDate
                this.newTask.duedate=n["duedate"]
                const nameArray = n["receiver"].split(/\s+/)
                this.newTask.receiverFirstname = nameArray[0]
                this.newTask.receiverLastname = nameArray[1]
                this.createTask()
            }
        }
    },
    beforeMount(){
        this.getTasks()
    }
}
</script>

<style scoped>
#task-sidebar {
    background-color: rgb(222, 218, 217);
    height: 100vh;
    width: 280px;
}

#task-page{
    display: flex;
    margin: 0px;
}

#task-main{
    flex-grow: 1;
}

#tasks-display{
    display: flex;
    flex-direction: column;
    text-align: center;
}

.task-btn{
    width: 50%;
}

.task-btn:hover {
  background-color: #c0c0c0;  
}

li{
    list-style-type:none;
}

ul{
    padding:0px;
    text-align: center;
}

button{
    font-size: 18px;
    border:1px solid black;
    background-color: white;
}

hr {
  display: block;
  height: 1px;
  border: 0;
  border-top: 1px solid #000000;
  margin: 1em 0;
  padding: 0;
}

#sidebar-heading{
    font-size: 28px;
    margin-bottom: 0;
}
</style>