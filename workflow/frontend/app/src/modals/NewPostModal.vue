<template>
  <div class="modal-mask">
      <div class="modal-wrapper">
          <div class="modal-container">

              <div class="modal-header">
                  <h1>Creating a new post</h1>
              </div>

              <div class="modal-body">
                  <form @submit.prevent="sendNewPost">
                      <label for="title">Title of post:</label>
                      <input v-model="title" type="text" name="title" required />

                      <label for="content">Content:</label>
                      <textarea v-model="content" name="content" rows="4" cols="25" required></textarea>
                      <input type="submit" id="create-btn" />
                  </form>
              </div>

              <div class="modal-footer">
                    
                    <button id="close-btn" @click="$emit('close','cancel')">Cancel</button>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
export default{
  emits:[
      "close"
  ],
  data(){
      return{
          content:"",
          title:""
      }
  },
  methods:{
      isTitleValueValid(){
      if (this.title.length>50){
          return false
      } else {
          return true
      }
      },

      isFormNotEmpty(){
      if (this.content === "" || this.title === "" ){
          return false
      } else{
          return true
      }
      },

      checkIfFormIsValid(){
      return (this.isTitleValueValid())
      },
      sendNewPost(){
      if (this.checkIfFormIsValid()){
          this.$emit("close",{
              title:this.title,
              content:this.content
          })
      } else{
          alert("Error, title must be less than 50 characters.")
      }
      }
  }
}
</script>

<style scoped>
.modal-mask {
position: fixed;
z-index: 9998;
top: 0;
left: 0;
width: 100%;
height: 100%;
background-color: rgba(0, 0, 0, 0.5);
display: table;
transition: opacity 0.3s ease;
}

.modal-wrapper {
display: table-cell;
vertical-align: middle;
}

.modal-container {
width: 40%;
height: 40%;
margin: 0px auto;
padding: 20px 30px;
background-color: #fff;
border-radius: 2px;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
transition: all 0.3s ease;
font-family: Helvetica, Arial, sans-serif;
text-align: center;
}

.modal-header h1 {
margin-top: 0;
color: #42b983;
}

.modal-body {
margin: 20px 0;
}

.modal-default-button {
float: right;
}

.modal-enter {
opacity: 0;
}

.modal-leave-active {
opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
-webkit-transform: scale(1.1);
transform: scale(1.1);
}

input, label{
  display:block;
  padding:2px;
  margin-bottom: 2px;
}

input, textarea{
margin: 0 auto;
width: 60%;
}

#close-btn{
font-size: 1.25rem;         
padding: 0.5rem 1rem;       
background-color: #eb1818;  
color: #ffffff;                
border: none;               
border-radius: 6px;         
cursor: pointer;
margin-right: 10px;
}

#close-btn:hover {
background-color: #c01414;  
}

#create-btn{
font-size: 1.25rem;         
padding: 0.5rem 1rem;       
background-color: #189742;  
color: #ffffff;                
border: none;               
border-radius: 6px;         
cursor: pointer;

}

#create-btn:hover {
background-color: #127232; 
}


</style>