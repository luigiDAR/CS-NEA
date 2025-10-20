<template>
    <div>
        <h1>Login Page</h1>
    </div>

   <div id="login-form">
        <div id="messages">
            <p v-if="errorMessage">{{ errorMessage }}</p>
        </div>

        <form @submit.prevent="sendUserInput">
            <label for="email">Enter email:</label>
            <input v-model="email" type="text" id="email" autocomplete="on" required /> <br>
            <label for="pwd">Enter password:</label>
            <input v-model="password" type="password" id="pwd" required /> <br>
            <input type="submit" id="submit-btn"/>
        </form>
        <button @click="changeForm">Create new account</button>
    </div> 
</template>

<script>
import axios from "axios";
import { clearTempStorage } from '@/utils/browserstorage';
import { setTempStorage } from "@/utils/browserstorage";

export default{
    name:"LoginForm",
    emits:[
        'new-acc'
    ],
    data(){
        return{
            email:"",
            password:"",
            errorMessage:""
        }
    },
    methods:{
        async sendUserInput(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/login`, {
            operation: "login",
            content: [this.email,this.password]
            })
            .then((response)=>{
                if (response["data"] == "Succesfull login"){
                    setTempStorage(this.email)
                    console.log("user is logged in")
                    this.$router.replace("/workspace")
                } else{
                    this.errorMessage = response["data"]
                }
                
            })
            .catch ((error)=>{
                console.error("Error sending data:", error)
            }) 
        },
        changeForm(){
            this.$emit('new-acc')
        }
    },
    mounted(){
        const currentTime = new Date()
        if (
            localStorage.getItem("isLoggedIn")==="true" 
            && 
            currentTime.getTime()-localStorage.getItem("timeToken") < 7200000
        ){
            this.$router.push("/workspace")
        } else {
            clearTempStorage()
        }
    }
}
</script>

<style scoped>
input {
    margin:0 auto;
    width: 50%;
}

#submit-btn {
    border: none;   
    border-radius: 8px;        
    background-color: green;   
    padding: 10px 20px;     
    color: white;          
    cursor: pointer; 
    margin-bottom: 30px;       
}

#login-form{
    text-align: center;
    background-color: rgb(245, 209, 169);
    margin: auto;
    max-width: 50%;
    padding-top:5px;
    padding-bottom:15px;
    border-radius: 12px;
}

#messages{
    color:red;
    text-decoration:underline;
}

label{
    display: block;
}
</style>
