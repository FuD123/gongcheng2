import { mount } from '@vue/test-utils'
import App from '@/App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createStore } from 'vuex'

const routes = [
  { path: '/', component: { template: '<div>Home</div>' } },
  { path: '/dashboard', component: { template: '<div>Dashboard</div>' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const store = createStore({
  state: {
    auth: {
      user: null,
      isAuthenticated: false
    }
  },
  mutations: {
    setUser(state, user) {
      state.auth.user = user
      state.auth.isAuthenticated = true
    }
  }
})

describe('App.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(App, {
      global: {
        plugins: [router, store]
      }
    })
  })

  it('renders the app container', () => {
    expect(wrapper.find('[data-test="app-container"]').exists()).toBe(true)
  })

  it('renders the navigation bar', () => {
    expect(wrapper.find('[data-test="nav-bar"]').exists()).toBe(true)
  })

  it('renders router view', () => {
    expect(wrapper.find('[data-test="router-view"]').exists()).toBe(true)
  })

  it('shows login button when not authenticated', () => {
    expect(wrapper.find('[data-test="login-button"]').exists()).toBe(true)
    expect(wrapper.find('[data-test="logout-button"]').exists()).toBe(false)
  })

  it('shows logout button when authenticated', async () => {
    store.commit('setUser', { username: 'testuser' })
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('[data-test="logout-button"]').exists()).toBe(true)
    expect(wrapper.find('[data-test="login-button"]').exists()).toBe(false)
  })

  it('navigates to home page', async () => {
    await router.push('/')
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('[data-test="router-view"]').text()).toContain('Home')
  })

  it('navigates to dashboard page', async () => {
    await router.push('/dashboard')
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('[data-test="router-view"]').text()).toContain('Dashboard')
  })
})
