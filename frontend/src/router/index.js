import Vue from 'vue'
import VueRouter from 'vue-router'
import Case1View1 from '../views/Case1View1.vue'
import Case1View2 from '../views/Case1View2.vue'
import Case2View from '../views/Case2View.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Сase1View1',
    component: Case1View1
  },
  {
    path: '/scan',
    name: 'Сase1View2',
    component: Case1View2
  },
  {
    path: '/case2',
    name: 'Case2View',
    component: Case2View
  },
]

const router = new VueRouter({
  routes
})

export default router
