<template>
    <table>                
        <thead>           
            <tr >               
                <th v-for="key in arrayOfObjectProperties">{{ key }}</th>
            </tr>
        </thead>
        <tbody>              
            <tr v-for="(record,index) in queryData" :key="index">
                <td v-for="(key,index) in arrayOfObjectProperties" :key="index">
                    {{ record[key] }}
                </td>
            </tr>
        </tbody>
    </table>
</template>
<script>
export default{
    name:"RecordTemplate",
    props:{
        queryData:Array 
    },
    computed:{
        arrayOfObjectProperties(){
            let keysArray = []
            for (let property in this.queryData[0]){
                keysArray.push(property)
            }
            return keysArray
        }
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

</style>