//Importing Vue components
import LoginPage from '@/pages/LoginPage.vue'

import WorkspacePage from '@/pages/WorkspacePage.vue'
import GroupsPage from '@/pages/GroupsPage.vue'
import TasksPage from '@/pages/TasksPage.vue'
import PostsPage from '@/pages/PostsPage.vue'
import AdminPage from '@/pages/AdminPage.vue'
import SettingsPage from '@/pages/SettingsPage.vue'

import AdminManager from '@/sections/AdminManager.vue';
import AdminQueryForm from '@/sections/AdminQueryForm.vue';
import AdminRecords from '@/sections/AdminRecords.vue';
import GroupManager from '@/sections/GroupManager.vue';
import MembersListTable from '@/sections/MembersListTable.vue';

//Importing functions
import { createRouter, createWebHashHistory } from 'vue-router'
import { clearTempStorage } from '@/utils/browserstorage';

//Empty component used for logout path
const emptyComponent = { template: `<div></div>` }

//Defining a logout function, which clears the browser's temporary storage
const logout = ()=>{
  if ( clearTempStorage()){
    console.log("Successful logout")
  } 
}

//Defining routes
const routes = [
  {
    path:'/',
    redirect:'/login'
  },  
  {  
    path: '/login', 
    component: LoginPage
  },
  {
    path:'/logout',
    beforeEnter: (to,from,next)=>{
      logout()
      next('/')
    },
    component:emptyComponent 
  },
  {
    path:'/workspace',
    component: WorkspacePage,
    children:[
      {
        path:'groups',
        component:GroupsPage
      },
      {
        path:'tasks',
        component:TasksPage
      },
      {
        path:'posts',
        component:PostsPage
      },
      {
        path:'admin',
        component:AdminPage,
        children:[
          {
            path:'query',
            component:AdminQueryForm
          },
          {
            path:'members',
            component:MembersListTable
          },
          {
            path:'records',
            component:AdminRecords
          },
          {
            path:'manage-admins',
            component:AdminManager
          },
          {
            path:'manage-groups',
            component:GroupManager
          }
        ]
      },
      {
        path:'settings',
        component:SettingsPage
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next)=>{
    if (to.path === '/workspace' && localStorage.getItem('isLoggedIn') !== 'true') {
        next('/'); // redirect them to the login page
    } else {
        next(); // allow the navigation
    }
  }
)

export default router
