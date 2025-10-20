<template>
    <div id="groupmanager">
        <div id="header">
            <h1>Group Manager</h1>
            <p>Here you can create and delete groups or add new members.</p>
        </div>
        <div id="main">
            <div id="tables">
            <h3>Current groups:</h3>
            <table>                
                <thead>           
                    <tr>               
                        <th>Name</th> 
                        <th>Leader</th>
                        <th>Number of members</th>
                    </tr>
                </thead>
                <tbody>              
                    <tr v-for="(group,index) in allGroups" :key="index">
                        <td>{{ group.name }}</td>
                        <td>{{group.leader.firstname}} {{group.leader.lastname}}</td>
                        <td>{{ group.noOfMembers}}</td>
                    </tr>
                </tbody>
            </table> 
            </div>
            <p id="backend" v-if="backendMsg">{{ backendMsg }}</p>
            <div id="groupforms">
                <ModifyGroupsForm :group-and-user-data="{
                    groupsArray:allGroups,
                    usersArray:allUsers
                }" 
                @create-group="(newGroupObj)=>createGroupInDB(newGroupObj)"
                @add-user-to-group="(userAndGroupObj)=>addUserToAGroup(userAndGroupObj)"
                @delete-group="(groupObj)=>deleteAGroup(groupObj)"
                /> 
            </div>
        </div>
    </div>
    
</template>

<script>
import ModifyGroupsForm from '@/elements/ModifyGroupsForm.vue';
import axios from 'axios'
export default{
    name:"GroupManager",
    components:{
        ModifyGroupsForm
    },
    data(){
        return{
            allGroups:[],
            allUsers:[],
            backendMsg:undefined,
        }
    },
    methods:{
        async getAllGroupsInOrg(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/groups`,{
                operation:"getallgroups",
                content:localStorage.getItem("userEmail")
            }).then((response)=>{
                this.allGroups = response.data
            }).catch((error)=>{
                console.log("Error:",error)
            })
        },
        async getAllUsersInOrg(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/admin`,{
                operation:"memberslist",
                content:localStorage.getItem("userEmail")
            }).then((response)=>{
                this.allUsers = response.data
            }).catch((error)=>{
                console.log("Error:",error)
            })
        },
        async createGroupInDB(newGroup){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/groups`,{
                operation:"creategroup",
                content:{
                    newGroupName:newGroup.group,
                    newGroupLeader:newGroup.groupleader.email
                }
            }).then((response)=>{
                this.backendMsg = response.data
                this.getAllGroupsInOrg()
            }).catch((error)=>{
                console.log("Error:",error)
            })
        },
        async addUserToAGroup(userAndGroupObj){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/groups`,{
                operation:"addusertogroup",
                content:{
                    userToAdd:userAndGroupObj.user,
                    groupToAdd:userAndGroupObj.group
                }
            }).then((response)=>{
                this.backendMsg = response.data
                this.getAllGroupsInOrg()
            }).catch((error)=>{
                console.log("Error:",error)
            })
        },
        async deleteAGroup(groupObj){
            console.log(groupObj)
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/groups`,{
                operation:"deletegroup",
                content:{
                    group:groupObj,
                    leader:groupObj.leader
                }
            }).then((response)=>{
                this.backendMsg = response.data
                this.getAllGroupsInOrg()
            }).catch((error)=>{
                console.log("Error:",error)
            })
        }
    },
    beforeMount(){
        this.getAllGroupsInOrg()
        this.getAllUsersInOrg()
    }
}
</script>

<style scoped>
table {
  width: 50%;
  border-collapse: collapse;
  margin: auto;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

thead {
  background-color: #f4f4f4;
}

#backend-message{
    color:green;
}

#groupmanager{
    flex-grow: 1;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 120px 1fr;
    max-height: 100%;
}

#header{
    background-color: inherit;
}

#main{
    
    overflow-y: auto;
}

#backend{
    background-color: rgb(0, 77, 128);
    padding:8px 0px 8px 0px;
    color:white;
}
</style>