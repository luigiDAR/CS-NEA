<template>
    <h3>Create new group</h3>
    <form @submit.prevent="createGroup">
        <label for="newGroupName">Group name:</label>
        <input v-model="newGroupName" id="newGroupName" required/>
        <br>
        <label for="newGroupLeader">Group leader:</label>
        <select v-model="newGroupLeader" id="newGroupLeader" required>
            <option v-for="(admin,index) in allAdmins" :key="index">
                {{ `${admin.firstname} ${admin.lastname}` }}
            </option>
        </select>

        <p v-if="groupAndUserData.backendMsg">{{ backendMsg }}</p>
        <input class="submit" type="submit" />
    </form>

    <h3>Add a new member to a group</h3>
    <form @submit.prevent="addMemberToGroup">
        <label for="newUser">Add this user:</label>
        <select v-model="userToAdd" id="newUser" required>
            <option v-for="(user,index) in groupAndUserData.usersArray" :key="index">
                {{ user.firstname }} {{ user.lastname }}
            </option>
        </select>

        <label for="selectedGroup">In this group:</label>
        <select v-model="groupToAddMember" id="group" required>
            <option v-for="(group,index) in groupAndUserData.groupsArray" :key="index">
                {{ group.name }}
            </option>
        </select>

        <p v-if="groupAndUserData.backendMsg">{{ backendMsg }}</p>
        <input class="submit" type="submit" />
    </form>

    <h3>Delete group</h3>
    <form @submit.prevent="deleteGroup">
        <label for="group">Delete this group:</label>
        <select v-model="groupToDelete" id="group" required>
            <option v-for="(group,index) in groupAndUserData.groupsArray" :key="index">
                {{ group.name }}
            </option>
        </select>

        <p v-if="groupAndUserData.backendMsg">{{ backendMsg }}</p>
        <input class="submit" type="submit" />
    </form>
    <br>
</template>

<script>
export default{
    emits:[
        "createGroup",
        "addUserToGroup",
        "deleteGroup"
    ],
    props:{
        groupAndUserData:Object
    },
    data(){
        return{
            allAdmins:[],
            newGroupName:undefined,
            newGroupLeader:undefined,
            userToAdd:undefined,
            groupToAddMember:undefined,
            groupToDelete:undefined
        }
    },
    watch:{
        groupAndUserData(){
            this.allAdmins = this.groupAndUserData.usersArray.filter(user=>
            user.role!=="W"
            ) 
        }
    },
    methods:{
        getUserObjFromName(userSelected){
            const [selectedFirstname, selectedLastname] = userSelected.split(" ");
            return this.groupAndUserData.usersArray.find(
                user => user.firstname === selectedFirstname && user.lastname === selectedLastname
            );
        },
        getGroupObjFromName(selectedGroupName){
            return this.groupAndUserData.groupsArray.find(
                group => group.name == selectedGroupName
            );
        },
        createGroup(){
            this.$emit('createGroup',{
                group:this.newGroupName,
                groupleader:this.getUserObjFromName(this.newGroupLeader)
            })
        },
        addMemberToGroup(){
            this.$emit('addUserToGroup',{
                user:this.getUserObjFromName(this.userToAdd),
                group:this.getGroupObjFromName(this.groupToAddMember)
            })
        },
        deleteGroup(){
            this.$emit('deleteGroup',this.getGroupObjFromName(this.groupToDelete)
            )
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

.submit{
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