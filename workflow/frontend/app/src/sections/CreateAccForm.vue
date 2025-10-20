<template>
    <h1>Create a new account</h1>
    <div id="login-form">
        <form @submit.prevent="sendUserInput" class="login-form">
            <p v-if="errorMessage" style="color:red;">{{ errorMessage }}</p>
            <label for="fname">Enter your first name:</label>
            <input v-model="fname" type="text" id="fname" required /> <br>

            <label for="lname">Enter your last name:</label>
            <input v-model="lname" type="text" id="lname" required /> <br>

            <label for="email">Enter your email:</label>
            <input v-model="email" type="email" id="email" autocomplete="on" required /> <br>

            <label for="firstpwd">Create your password:</label>
            <input v-model="firstpwd" type="password" id="firstpwd" required /> <br>

            <label for="secondpwd">Confirm password:</label>
            <input v-model="secondpwd" type="password" id="secondpwd" required /> <br>

            <p>Select one of the following:</p>
            <label for="notneworg">I am joining an existing organization</label>
            <input type="radio" id="notneworg" name="orgtype" @input="newOrg=false" required/> <br>
            
            <label for="neworg">I am creating a new organization</label> 
            <input  type="radio" id="neworg" name="orgtype" @input="newOrg=true"/> <br>

            <div v-if="newOrg===false">
                <label for="orgid">Enter organization ID:</label> 
                <input v-model="orgId" type="number" min="0" id="orgid" required/> <br>
            </div>

            <div v-if="newOrg===true">
                <label for="orgName">Give your organization a name:</label> 
                <input v-model="orgName" type="text" id="orgName" required/> <br>
            </div>

            <input type="submit" id="submit-btn"/>

            <button @click="changeForm" >Login to existing account</button>
        </form>
        <p>{{ newOrg }}</p>
    </div> 
</template>

<script>
import axios from 'axios'
import { setTempStorage } from '@/utils/browserstorage'
export default{
    name:"NewAccForm",
    emits:[
        'exist-acc'
    ],
    data(){
        return{
            fname:"",
            lname:"",
            email:"",
            firstpwd:"",
            secondpwd:"",
            errorMessage:"",
            newOrg:undefined,
            orgId:"",
            orgName:""
        }
    },
    methods:{
        changeForm(){
            this.$emit('exist-acc')
        },
        checkUsername(){
            if (this.fname.length < 50 && this.lname.length < 50){
                return true
            } else{
                this.errorMessage = "First and last name must be less than 50 characters."
                return false
            }
        },
        checkPasswordInput(){
            if (this.firstpwd === this.secondpwd){
                const pwdRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]).+$/
                if (pwdRegex.test(this.firstpwd)==true){
                    return true
                } else{
                    this.errorMessage = "Password must contain at least one lower case letter, one upper case letter, one number and one special character."
                    return false
                }  
            } else{
                this.errorMessage = "Passwords don't match."
                return false
            }
        },
        async createNewUserInExistingOrg(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/login`, {
                operation:"signin",
                content: {
                fname: this.fname,
                lname: this.lname,
                email: this.email,
                password: this.firstpwd,
                orgId: this.orgId,
                role:"W"
            }
            })
            .then((response)=>{
                console.log(response.data)
            })
            .catch ((error)=>{
                console.error("Error sending data:", error)
            }) 
        },
        async createNewUserAndNewOrg(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/login`, {
                operation:"signin",
                content: {
                fname: this.fname,
                lname: this.lname,
                email: this.email,
                password: this.firstpwd,
                orgName: this.orgName,
                role:"W"
            }
            })
            .then((response)=>{
                console.log(response["data"])
            })
            .catch ((error)=>{
                console.error("Error sending data:", error)
            }) 
        },
        sendUserInput(){
            if (this.checkUsername()&&this.checkPasswordInput()){
                this.errorMessage = ""
                if (this.newOrg === false){
                    this.createNewUserInExistingOrg().then(()=>{
                        console.log("user created")
                        setTempStorage(this.email)
                        this.$router.push("/workspace")
                    })
                } else{
                    this.createNewUserAndNewOrg().then(()=>{
                        console.log("user created")
                        setTempStorage(this.email)
                        this.$router.push("/workspace")
                    })
                    
                }
            }
        }

    }
}
</script>

<style scoped>
input {
    margin:0 auto;
    width: 50%;
    display: block;
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

.login-form{
    text-align: center;
    background-color: rgb(245, 209, 169);
    margin: auto;
    width: 80%;
    height:80%;
    padding-top:5px;
    padding-bottom:15px;
    border-radius: 12px;
}

#messages{
    color:red;
    text-decoration:underline;
}
</style>