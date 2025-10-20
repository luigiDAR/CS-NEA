<template>
    <div class="post">
        <div class="post-header">
            <p class="post-title">{{ postInfo["title"] }}</p>
            <p class="post-meta">{{ postInfo["author"] }} sent this on {{ postInfo["datePublished"] }}</p>
        </div>
        <div>
            <p class="post-content">{{  postInfo["content"] }}</p>
        </div>
    </div>
</template>

<script setup>
import { onBeforeMount } from 'vue';
import { getDBformatDate } from '@/utils/datetime';
const props = defineProps({
    postInfo:Object
})

const formatDate = () => {
    const formattedDate = getDBformatDate(props.postInfo.datePublished)
    return formattedDate
    
}


onBeforeMount(()=>{
    props.postInfo["datePublished"] = formatDate()
})
</script>

<style scoped>
.post{
    text-align: center;
    border-radius: 8px;
    padding-top: 5px;
    padding-bottom: 5px;
    border: 1.5px solid black;
    background-color: rgb(248, 248, 248);
    color:black;
    font-family: sans-serif;        
    max-width: 100%;     
    margin: 0 auto;       
    height: 380px;
    width: 90%;  
    box-sizing: border-box;
}

.post-title{
    font-size:large;
    font-weight: bold;
}

.post-meta{
    color:rgb(41, 41, 41)
}

.post-header{
    padding-bottom: 5px;
}
</style>