<template> 
    <div id="settings-page">
        <div id="settings-body">
            <h1>Welcome to settings</h1>
            <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>
            <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

            <form @submit.prevent="updateUserPersonalData">
                <p id="form-title">My Personal Details</p>
                <hr>
                <div class="input-fields">
                    <label for="firstname">My firstname:</label>
                    <input v-model="newFirstname" :placeholder="this.userData.firstname" id="firstname" required/>
                    <label for="lastname">My last name:</label>
                    <input v-model="newLastname" :placeholder="this.userData.lastname" id="lastname" required/>
                    <br>
                    <input type="submit" class="submit-btn" />
                </div>
                

            </form>

            <form @submit.prevent="updateUserLoginData">
                <p id="form-title">My Login Details</p>
                <hr>
                <div class="input-fields">
                    <label for="email">My email:</label>
                    <input v-model="newEmail" type="email" :placeholder="this.userLoginData.email" id="email" required/>
                    <label for="new-password">Enter new password:</label>
                    <input v-model="newPassword" type="password" id="new-password" required/> 
                    <label for="new-password-confirm">Re-enter new password:</label>
                    <input v-model="doubleCheckPassword" type="password" id="new-password-confirm" required/> 
                    <label for="old-password">Enter current password to update login details:</label>
                    <input v-model="currentPassword" type="password" id="old-password" required/> 
                    <br>
                    <input type="submit" class="submit-btn" />
                </div>


            </form>

        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default{
    name:"SettingsPage",
    props:[
        "userData"
    ],
    data(){
        return{
            userLoginData:{},
            successMsg:undefined,
            errorMsg:undefined,
            newFirstname:undefined,
            newLastname:undefined,
            newEmail:undefined,
            currentPassword:undefined,
            newPassword:undefined,
            doubleCheckPassword:undefined
        }
    },
    methods:{
        async getUserLoginData(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/handleuser`,{
                operation:"getuserlogininfo",
                content: localStorage.getItem("userEmail")
            })
            .then((response)=>{
                this.userLoginData = response.data
            })
            .catch((error)=>{
                console.log("Error:",error)
            })
        },
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
        async sendNewPersonalData(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/handleuser`,{
                operation:"updateuserpersonalinfo",
                content: {
                    email:localStorage.getItem("userEmail"),
                    newFirstname:this.newFirstname,
                    newLastname:this.newLastname
                }
            })
            .then((response)=>{
                this.successMsg = response["data"]
                console.log(response["data"])
            })
            .catch((error)=>{
                this.errorMsg = error
                console.log("Error:",error)
            })
        },
        async sendNewLoginData(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/handleuser`,{
                operation:"updateuserlogininfo",
                content: {
                    currentEmail:localStorage.getItem("userEmail"),
                    newEmail:this.newEmail,
                    oldPassword:this.currentPassword,
                    newPassword:this.newPassword
                }
            })
            .then((response)=>{
                this.successMsg = response.data
            })
            .catch((error)=>{
                this.errorMsg = error
                console.log("Error:",error)
            })
        },
        checkUserInputForPersonal(){
            if (this.newFirstname.length < 50 && this.newLastname.length < 50){
                if (this.newFirstname != this.userData.firstname && this.newLastname != this.userData.lastname){
                    return true
                } else {
                    this.errorMsg = "You have entered your current name."  
                    return false  
                }
            } else{
                this.errorMsg = "Names must be less than 50 characters."
                return false
            }
        },
        checkUserInputForLogin(){
            if (this.newEmail.length < 50 && this.newPassword.length < 50){
                return true
            } else{
                this.errorMsg = "Email and new password must be less than 30 characters."
                return false
            }
        },
        checkPasswordsMatch(){
            if (this.newPassword === this.doubleCheckPassword){
                return true
            } else {
                this.errorMsg = "Password don't match"
                return false
            }
        },
        updateUserPersonalData(){
            if (this.checkUserInputForPersonal()){
                this.sendNewPersonalData()
                this.getUserData()
            }
        },
        updateUserLoginData(){
            if (this.checkUserInputForLogin() && this.checkPasswordsMatch()){
                this.sendNewLoginData().then(()=>{
                    this.getUserLoginData()
                    this.newEmail = ""
                    this.currentPassword = ""
                    this.newPassword = ""
                    this.doubleCheckPassword = ""
                })
                
            }
        }
    },
    beforeMount(){
        this.getUserLoginData()
    }
}
</script>

<style scoped>
#settings-page{
    text-align: left;
    margin-left: 40px;
    height: 100vh;
    width: 100vh; 
}

#settings-body{
    max-width: 100%;
    max-height: 100%;
    box-sizing: border-box;
}

.input-fields{
    text-align: left;
    padding-left: 12px;
}

form{
    border:1px solid black;
    background-color: inherit;
    text-align: center;
    width: 80%;
    padding-bottom: 40px;
    margin-bottom: 40px;
    font-size: 24px;
}

input{
    display:inline;
    width: 40%;
    height: 30px;
    border-radius: 8px;
    font-size: 20px;
    margin-bottom: 10px;
}

hr {
  display: block;
  height: 1px;
  width: 100%;
  border: 0;
  border-top: 1px solid #000000;
  margin: 1em 0;
  padding: 0;
}

.submit-btn{
    display:inline;
    padding:18px;
    font-size: 20px;
    border-radius: 10px;
    background-color: rgb(0, 77, 128);
    color: white;
    border:none;
    width:25%;
    height:55px;
    min-width: fit-content;
    cursor: pointer;
    margin-top: 10px;
}

.success-msg{
    color:green;
    font-size: 20px;
}

.error-msg{
    color:red;
    font-size: 20px;
}

label{
    display: block;
}
</style>