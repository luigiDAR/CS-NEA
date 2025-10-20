<template>
    <div id="group-page">
        <div id="group-sidebar">
            <p id="sidebar-heading">Groups</p>
            <hr>
            <div id="options">
                <ul>
                <li v-for="(group,index) in groupsArray" :key="index">
                    <GroupButton style="cursor:pointer;" @click="selectGroup(index)" :group-data="{name:group.name}" />
                </li>
            </ul>
            </div>
        </div>
        <div id="group-main">
            <SelectedGroup 
                v-if="selectedGroup!=undefined" 
                :group-data="{
                    name:this.selectedGroup.name,
                    groupid:this.selectedGroup.groupid,
                    groupLeader:this.selectedGroup.leader
                }" 
                :user-data="{
                    userid:this.userData.userid
                }" 
            />
        </div>
    </div>
</template>

<script>
import GroupButton from '@/elements/GroupButton.vue';
import SelectedGroup from '@/sections/SelectedGroup.vue';
import axios from 'axios'

export default{
    name:"GroupsPage",
    props:[
        "userData"
    ],
    components:{
        GroupButton,
        SelectedGroup
    },
    data(){
        return{
            groupsArray:[],
            selectedGroup:undefined
        }
    },
    methods:{
        async getGroups(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/groups`,{
                operation:"getusergroups",
                content:localStorage.getItem("userEmail")
            })
            .then((response)=>{
                this.groupsArray = response.data
            })

            .catch((error)=>{
                console.log("Error:",error)
            })
        },
        selectGroup(groupIndex){   
            this.selectedGroup = this.groupsArray[groupIndex]
        }
    },
    beforeMount(){
        this.getGroups()
    }
}
</script>

<style scoped>
#group-sidebar {
    background-color: rgb(222, 218, 217);
    height: 100vh;
    width: 280px;
}

#group-page{
    display: flex;
    margin: 0px;
}

#group-main {
    flex-grow: 1;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 80px 1fr;
    max-height: 100vh; 
}

button{
    font-size: 18px;
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

li{
    list-style-type:none;
}

ul{
    padding:0px;
    text-align: center;
}
</style>