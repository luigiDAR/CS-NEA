<template>
    <div id="admin-page">
        <div id="admin-sidebar">
            <p id="sidebar-heading">Admin Tools</p>
            <hr>
            <button class="tool-btn" @click="goToPage('query')">Query the database</button>
            <button class="tool-btn" @click="goToPage('members')">Member's List</button>
            <button class="tool-btn" @click="goToPage('records')">Records</button>
            <button class="tool-btn" @click="goToPage('manage-admins')">Manage admins</button>
            <button class="tool-btn" @click="goToPage('manage-groups')">Manage groups</button>
        </div>
        <div id="admin-main">
            <h1 v-if="$route.path==='/workspace/admin'" >Hello, {{ userData.firstname }} {{ userData.lastname }}. Please select an admin tool.</h1>
            <router-view v-slot="{ Component }">
                <component :is="Component" />
            </router-view>
        </div>
    </div>
</template>

<script>
import AdminManager from '@/sections/AdminManager.vue';
import AdminQueryForm from '@/sections/AdminQueryForm.vue';
import AdminRecords from '@/sections/AdminRecords.vue';
import GroupManager from '@/sections/GroupManager.vue';
import MembersListTable from '@/sections/MembersListTable.vue';

export default{
    name:"AdminPage",
    props:[
        "userData"
    ],
    components:{
        AdminQueryForm,
        MembersListTable,
        AdminManager,
        GroupManager,
        AdminRecords
    },
    methods:{
        goToPage(toolName){
            if (this.$router.currentRoute.value.fullPath == `/workspace/admin/${toolName}`){
                this.$router.push(`/workspace/admin`)
            } else {
                this.$router.push(`/workspace/admin/${toolName}`)
            }
        }
    }
}
</script>

<style scoped>
#admin-sidebar {
    background-color: rgb(222, 218, 217);
    height: 100vh;
    width: 280px;
    display: flex;
    flex-direction: column;
}

#admin-page{
    display: flex;
    margin: 0px;
}

#admin-main{
    flex-grow: 1;

    height: 100vh; 
}

button{
    font-size: 18px;
    border: 1px solid black;
    background-color: rgb(241, 241, 241);
    color: black;
    margin: auto;
    margin-top: 4px;
    margin-bottom: 4px;
    padding-top: 20px;
    padding-bottom: 20px;
    cursor: pointer;
    width: 80%;
}
button:hover {
  background-color: #c0c0c0;  
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