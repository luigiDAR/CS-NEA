<template>
    <form @submit.prevent="checkUserInput">
        <label for="user">Make the user...</label>
        <select v-model="selectedUserName" id="user" required>
            <option v-for="(user,index) in allUsersArray" :key="index">
                {{ user.firstname }} {{ user.lastname }}
            </option>
        </select>
        <label for="role">...have a role of:</label>
        <select v-model="newRole" id="role"  required>
            <option>Admin</option>
            <option>Worker</option>
        </select>
        <p id="error-msg" v-if="errorMessage">{{ errorMessage }}</p>
        <input type="submit" />

    </form>
</template>

<script>
export default{
    emits:["changeUserRole"],
    props:["allUsersArray"],
    data(){
        return{
            selectedUserName:undefined,
            selectedUserDataObj:undefined,
            newRole:undefined,
            errorMessage:"",
        }
    },
    methods:{
        getUserDataFromName(){
            const [selectedFirstname, selectedLastname] = this.selectedUserName.split(" ");

            this.selectedUserDataObj = this.allUsersArray.find(
                user => user.firstname === selectedFirstname && user.lastname === selectedLastname
            );
        },
        isNewRoleDifferent(){
            if (this.selectedUserDataObj !== undefined){
                if (this.selectedUserDataObj.role !== this.newRole){
                    return true
                } else{
                    return false
                }
            }
        },
        changeOptionToCharacter(){
            if (this.newRole == "Admin"){
                this.newRole = "A"
            } else {
                this.newRole = "W"
            }
        },
        checkUserInput(){
            this.changeOptionToCharacter()
            this.getUserDataFromName()
            if (this.isNewRoleDifferent()){
                this.$emit('changeUserRole',{
                    email:this.selectedUserDataObj.email,
                    newRole:this.newRole
                })
                this.errorMessage = ""
            } else{
                this.errorMessage = "The user selected already has that role."
            }
        }
    }
}
</script>

<style scoped>
form{
    border:1px solid black;
    width:50%;
    margin:auto;
    padding: 15px 0px 30px 0px;
}
select,label{
    display: inline;
}

input{
    margin-top: 10%;
    padding:20px;
    border:none;
    border-radius: 8px;
    background-color: rgb(18, 182, 18);
    color:white;
    width:25%;
    height: 10%;
    cursor: pointer;
}

#error-msg{
    color: red;
}
</style>