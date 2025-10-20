<template>
    <div id="header">
        <h1>Member's List</h1>
    </div>
    <div>
        <table>                
            <thead>           
                <tr>               
                    <th>First Name</th> 
                    <th>Last Name</th>
                    <th>Role</th>
                    <th>Email</th>
                    <th>Age</th>
                    <th>Gender</th>
                </tr>
            </thead>
            <tbody>              
                <tr v-for="(user,index) in usersArray" :key="index">
                    <td>{{ user.firstname }}</td>   
                    <td>{{ user.lastname }}</td>
                    <td>{{ user.role }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.age }}</td>
                    <td>{{ user.gender }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    data(){
        return{
            usersArray: []
        }
    },
    methods:{
        async getAllUsersInOrg(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/admin`,{
                operation:"memberslist",
                content:localStorage.getItem("userEmail")
            }).then((response)=>{
                this.usersArray = response.data
                console.log(this.usersArray)
            }).catch((error)=>{
                console.log("Erro:",error)
            })
        }
    },
    beforeMount(){
        this.getAllUsersInOrg()
    }
}
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-left:4px;
  margin-right:4px;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

thead {
  background-color: #f4f4f4;
}
</style>