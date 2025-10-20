<template>
    <LoginForm v-if="!isNewAcc" @new-acc="goToNew"/>
    <CreateAccForm v-if="isNewAcc" @exist-acc="goToNew" />
</template>

<script>
import LoginForm from '../sections/LoginForm.vue'
import CreateAccForm from '../sections/CreateAccForm.vue'

export default{
    data(){
        return{
            isNewAcc: false
        }
    },
    components:{
        LoginForm,
        CreateAccForm
    },
    methods: {
        goToNew(){
            this.isNewAcc = !this.isNewAcc
        }
    }
}
</script>
