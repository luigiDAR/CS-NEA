<template>
    <div class="page">
        <div class="sidebar">
            <!-- The first five buttons -->
            <div>
            
            <button>
                <img src="\imgs\icon.png" id="pfp" width="65" height="70" style="border:1.5px solid black; background-color:white;">
                </button>
            
            
            <button class="sidebutton" @click="goToPage('groups')">
                <img src="\imgs\groups.png" id="pfp" width="65" height="70" style="border:1.5px solid black; background-color:white;">
                <p>Groups</p>
                </button>
            
            
            
            <button class="sidebutton" @click="goToPage('tasks')">
                <img src="\imgs\tasks.png" id="pfp" width="65" height="70" style="border:1.5px solid black; background-color:white;">
                <p>Tasks</p>
                </button>
            
            
            <button class="sidebutton" @click="goToPage('posts')">
                <img src="\imgs\notices.png" id="pfp" width="65" height="70" style="border:1.5px solid black; background-color:white;">
                <p>Posts</p>
                </button>
            
            
                <button v-if="this.userData.role != 'W'" id="admin" class="sidebutton" @click="goToPage('admin')">
                <img src="\imgs\admin.png" id="pfp" width="65" height="70" style="border:1.5px solid black; background-color:white;">
                <p>Admin</p>
                </button>
            
            </div>
        
            <!--The last two buttons -->
            <div style="margin-top: auto; padding-bottom: 20px;">
            
            <button class="sidebutton" @click="goToPage('settings')">
                <img src="\imgs\settings.png" id="pfp" width="65" height="70" style="border:1.5px solid black; background-color:white;">
                <p>Settings</p>
                </button>
            
            
            <button class="sidebutton" @click="$router.push('/logout')">
                <img src="\imgs\logout.png" id="pfp" width="65" height="70" style="border:1.5px solid black; background-color:white;">
                <p>Log-out</p>
                </button>
            
            </div>
        
        </div>
        <div class="main">
            <h1 v-if="$route.path==='/workspace'" >Hello, {{ userData.firstname }} {{ userData.lastname }}</h1>
            <router-view v-slot="{ Component }">
                <component :is="Component" :user-data="userData" />
            </router-view>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
export default{
    data(){
        return{
            userData: "",
            isAdmin:undefined
        }
    },
    methods:{
        async getUserData(email){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/handleuser`,{
                operation:"getuserdata",
                content: [email]
            })
            .then((response)=>{
                this.userData = response.data
            })
            .catch((error)=>{
                console.log("Error:",error)
            })
        },
        goToPage(pagePath){
            if(this.$route.path===`/workspace/${pagePath}`){
                router.push('/workspace')
            } else {
                router.push(`/workspace/${pagePath}`)
            }
        }
    },
    beforeMount(){
        const email = localStorage.getItem("userEmail")
        this.getUserData(email)
    }
}
</script>

<style scoped>
.page {
	font-family:Lucida Sans;
}

.sidebar {
  height: 100vh; 
  width: 140px; 
  position: fixed;   
  z-index: 1; 
  top: 0; 
  left: 0;
  background-color: rgb(222, 218, 217); 
  overflow-x: hidden;
  padding-top: 20px;
  display: flex; 
  flex-direction: column; 
}

.main {
  margin-left: 140px; 
} 

.sidebutton {
  cursor: pointer;
  background-color: inherit;
  font-size: large;
}

.sidebutton:hover {
		border: solid;
		border-color: red;
}

button {
	font-family:Lucida Sans;	
    border: none;
    appearance: none;
    background-color: inherit;
}
</style>