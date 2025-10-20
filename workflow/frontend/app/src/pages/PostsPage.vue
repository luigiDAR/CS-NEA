<template>

    <h1>Welcome to the posts page</h1>
    <button v-if="userData['role']!='W'" id="new-post-btn" @click="showModal=true">Create a new post</button>

    <NewPostModal v-if="showModal" @close="(n)=>{this.handleModal(n); showModal=false;}" />
     
    <p>{{ this.backendData ? this.backendData : "" }}</p>
    <div>
        <ul class="grid-container">
            <li v-for="(post,index) in this.postData" :key="index" class="grid-item">
                <PostTemplate :post-info="{
                    author:post.author,
                    content:post.content,
                    datePublished:post.date,
                    id:post.id,    
                    title:post.title
                }" />
            </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';
import PostTemplate from '../sections/PostTemplate.vue';
import NewPostModal from '../modals/NewPostModal.vue';
import { getDBformatDate } from '@/utils/datetime';

export default{
    props:[
        "postInfo",
        "userData"
    ],
    components:{
        PostTemplate,
        NewPostModal
    },
    data(){
        return{
            newPost:{
                title:"",
                content:"",
                datePublished:"",
                email:localStorage.getItem("userEmail")
            },
            postData:"",
            backendData:"",
            showModal:false
        }
    },
    methods:{
        async getPosts(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/posts`,{
                operation:"getallposts",
                content:localStorage.getItem("userEmail")
            })
            .then((response)=>{
                this.postData = response.data
            })
            .catch((error)=>{
                console.log("Error:",error)
            })
        },
        async createPost(){
            const backendUrl = window.location.origin.replace(':8080', ':5000');
            axios.post(`${backendUrl}/posts`,{
                operation:"createnewpost",
                content: this.newPost
            })
            .then((response)=>{
                this.backendData = response["data"]
            })
            .catch((error)=>{
                console.error("Error sending data:",error)
            })
            .finally(()=>{
                this.getPosts()
            })
        },
        handleModal(n){
            if (n!=="cancel"){
                this.newPost.title = n["title"]
                this.newPost.content = n["content"]
                const dateOfPost = getDBformatDate(new Date())
                this.newPost.datePublished = dateOfPost
                this.createPost()
            }
        }
    },
    beforeMount(){
        this.getPosts()
    }
}
</script>

<style scoped>
li{
    list-style-type:none;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(1, 1fr); 
  grid-auto-rows: repeat(2, auto);
  gap: 30px; 
  padding: 10px;
  padding-left: 10%;
  padding-right: 10%;
  background-color: #f3f2f2;
}

.grid-item {
    display: flex;        
    align-items: stretch; 
}

#new-post-btn {
  font-size: 1.25rem;         
  padding: 0.5rem 1rem;       
  background-color: rgb(226, 225, 225);  
  color: #333;                
  border: none;               
  border-radius: 6px;         
  cursor: pointer;            
  transition: background 0.2s ease;
}

#new-post-btn:hover {
  background-color: #c0c0c0;  
}
</style>