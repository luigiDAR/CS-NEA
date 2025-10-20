<template>
    <div id="adminmanager">
        <div id="header">
        <h1>Admin Manager</h1>
        <p>Here you can select the roles of users in the organization.</p>
        </div>
    </div>
    <div>
        <h3>Current admins:</h3>
        <table>                
            <thead>           
                <tr>               
                    <th>First Name</th> 
                    <th>Last Name</th>
                    <th>Role</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody>              
                <tr v-for="(admin,index) in adminsArray" :key="index">
                    <td>{{ admin.firstname }}</td>   
                    <td>{{ admin.lastname }}</td>
                    <td>{{ admin.role }}</td>
                    <td>{{ admin.email }}</td>
                </tr>
            </tbody>
        </table>
        <h3>Add or remove an Admin:</h3>
        <p id="backend-message" v-if="backendMsg">{{ backendMsg }}</p>
        <AdminForm @changeUserRole="(newChange)=>{toggleRole(newChange)}" :all-users-array="usersArray"/>
    </div>
</template>

<script>
import AdminForm from '@/elements/AdminForm.vue';
import axios from 'axios'

export default{
    name:"AdminManager",
    components:{
        AdminForm
    },
    data(){
        return{
            usersArray: [],
            adminsArray:[],
            backendMsg:'',
        }
    },
    methods:{
        async getAllUsersInOrg(){
            console.log("new data fetched")
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/admin`,{
                operation:"memberslist",
                content:localStorage.getItem("userEmail")
            }).then((response)=>{
                this.usersArray = response.data.filter(user=>
                    user.email !== localStorage.getItem("userEmail")
                )
            }).catch((error)=>{
                console.log("Error:",error)
            })
        },
        async getAllAdminsInOrg(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/admin`,{
                operation:"getalladmins",
                content:localStorage.getItem("userEmail")
            }).then((response)=>{
                this.adminsArray = response.data
            }).catch((error)=>{
                console.log("Error:",error)
            })
        },
        async setNewUserRole(userEmail, userNewRole) {
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            try {
                const response = await axios.post(`${backendUrl}/admin`, {
                    operation: "setnewrole",
                    content: {
                        userEmail: userEmail,
                        newRole: userNewRole
                    }
                });
                this.backendMsg = response.data;
                await this.getAllAdminsInOrg(); 
            } catch (error) {
                console.log("Error:", error);
            }
        },
        async toggleRole(dataObj){
            const user = dataObj.email
            const newRole = dataObj.newRole
            await this.setNewUserRole(user, newRole)
            await this.getAllAdminsInOrg();
            await this.getAllUsersInOrg();
        }
    },
    beforeMount(){
        this.getAllUsersInOrg()
        this.getAllAdminsInOrg()
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

#adminmanager{
    max-height: inherit;
}
</style>