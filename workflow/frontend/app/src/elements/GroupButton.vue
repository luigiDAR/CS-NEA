<template>
    <div class="group-btn">
        <p class="group-title">{{ this.groupData.name}}</p>
    </div>
</template>

<script>
export default{
    name:"GroupButton",
    props:[
        "groupData"
    ] 
}
</script>

<style scoped>
.group-btn{
    border: 1px solid black;
    background-color: rgb(255, 255, 255);
    padding-top: 8px;
    cursor: pointer;
}
</style>