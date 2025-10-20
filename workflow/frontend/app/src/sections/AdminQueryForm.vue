<template>
    <div id="header">
        <h1>Database query</h1>
        <p>Generate a report by filling the criteria for the search tool.</p>
    </div>
    <div>
        <form @submit.prevent="sendSQLquery">
        <table>                
            <thead>           
                <tr>               
                    <th>Field</th>
                    <th>Condition</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>              
                <tr>
                    <td>
                        <select v-model="selectedField" required>
                            <option v-for="field in fieldsArray">{{ field }}</option>
                        </select>
                    </td>
                    <td>
                        <select v-model="selectedCondition" required>
                            <option v-for="condition in conditionsArray">{{ condition }}</option>
                        </select>
                    </td>
                    <td>
                        <select v-if="isDropdownValue" v-model="selectedValue" required>
                            <option v-for="(value,index) in valuesArray" :value="dropdownValueArray[index]">{{ value }}</option>
                        </select>
                        <input v-else v-model="selectedValue" 
                        :type="inputType" 
                        :min="inputType==='number'?0:null" 
                        :max="inputType==='number'?99:null"  
                        :maxlength="selectedCondition==='Must start with:'?1:null"
                        required/>
                    </td>
                </tr>
            </tbody>
        </table>

        <input type="submit" id="submit-btn" />
        </form>

        <RecordTemplate v-if="reportData!==null" :query-data="this.reportData" />
    </div>
</template>

<script>
import axios from 'axios'
import RecordTemplate from './RecordTemplate.vue'
export default{
    name:"AdminQueryForm",
    components:{
        RecordTemplate
    },
    data(){
        return{
            fieldsArray:["Email","Gender","Age","First Name","Last name","Role"],
            conditionsObject:{
                email:["Equal to:"],
                gender:["Equal to:"],
                age:["Equal to:","Lower than:","Greater than:"],
                name:["Equal to:","Must start with:"],
                role:["Equal to:"]
            },
            valuesObject:{
                gender:["Male","Female"],
                role:["Admin","Worker"]
            },
            selectedField:undefined,
            selectedCondition:undefined,
            selectedValue:undefined,
            reportData:null
        }
    },
    computed:{
        conditionsArray(){
            switch (this.selectedField){
                case "Email":
                    return this.conditionsObject.email
                case "Gender":
                    return this.conditionsObject.gender
                case "Age":
                    return this.conditionsObject.age
                case "Role":
                    return this.conditionsObject.role
                case "First Name":
                case "Last name":
                    return this.conditionsObject.name
                default:
                    return this.conditionsObject.email
            }
        },
        valuesArray(){
            if (this.selectedField === "Gender" || this.selectedField === "Role"){
                switch (this.selectedField){
                    case "Gender":
                        return this.valuesObject.gender
                    case "Role":
                        return this.valuesObject.role
                }
            }
        },
        isDropdownValue(){
            if (this.selectedField === "Gender" || this.selectedField === "Role"){
                return true
            }
        },
        inputType(){
            switch (this.selectedField){
                case "Email":
                    return "email"
                case "Age":
                    return "number"
                case "First Name":
                case "Last name":
                    return "text"
                default:
                    return "email"
            }
        },
        dropdownValueArray(){
            switch (this.selectedField){
                case "Gender":
                    return ["M","F"]
                case "Role":
                    return ["A","W"]
            } 
        }
    }, 
    methods:{
        async sendSQLquery(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/admin`, {
                operation:"executequery",
                content: {
                    currentUser:localStorage.getItem("userEmail"),
                    field:this.selectedField,
                    operator:this.selectedCondition,
                    value:this.selectedValue
                }
            })
            .then((response)=>{
                console.log(response.data)
                this.reportData = response.data
            })
            .catch ((error)=>{
                console.error("Error sending data:", error)
            }) 
        }
    }
}
</script>

<style scoped>
#fields{
    width:40px;
    height:fit-content;
    font-size: 18px;
    margin-bottom: 2%;
}

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

#submit-btn{
    padding: 8px 24px 8px 24px;
    font-size: 18px;
    border-radius: 10px;
    background-color: rgb(0, 128, 38);
    color: white;
    border:none;
    width: fit-content;
    height: fit-content;
    cursor: pointer;
    margin-top: 30px;
}
</style>