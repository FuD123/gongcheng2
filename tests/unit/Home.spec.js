import { mount } from '@vue/test-utils'
import Home from '@/views/Home.vue'
import { createStore } from 'vuex'

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

describe('Home.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Home, {
      global: {
        plugins: [store]
      }
    })
  })

  it('renders the home container', () => {
    expect(wrapper.find('[data-test="home-container"]').exists()).toBe(true)
  })

  it('shows welcome message', () => {
    expect(wrapper.find('[data-test="welcome-message"]').exists()).toBe(true)
    expect(wrapper.find('[data-test="welcome-message"]').text()).toContain('Welcome')
  })

  it('shows guest message when not authenticated', () => {
    expect(wrapper.find('[data-test="guest-message"]').exists()).toBe(true)
    expect(wrapper.find('[data-test="guest-message"]').text()).toContain('Please sign in')
  })

  it('shows personalized message when authenticated', async () => {
    store.commit('setUser', { name: 'Test User' })
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('[data-test="user-message"]').exists()).toBe(true)
    expect(wrapper.find('[data-test="user-message"]').text()).toContain('Test User')
  })

  it('renders feature list', () => {
    const features = wrapper.findAll('[data-test="feature-item"]')
    expect(features.length).toBeGreaterThan(0)
  })

  it('shows get started button when not authenticated', () => {
    expect(wrapper.find('[data-test="get-started-button"]').exists()).toBe(true)
  })

  it('shows dashboard button when authenticated', async () => {
    store.commit('setUser', { name: 'Test User' })
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('[data-test="dashboard-button"]').exists()).toBe(true)
  })

  it('emits login event when get started clicked', async () => {
    await wrapper.find('[data-test="get-started-button"]').trigger('click')
    expect(wrapper.emitted('login')).toBeTruthy()
  })

  it('emits dashboard event when dashboard clicked', async () => {
    store.commit('setUser', { name: 'Test User' })
    await wrapper.vm.$nextTick()
    
    await wrapper.find('[data-test="dashboard-button"]').trigger('click')
    expect(wrapper.emitted('dashboard')).toBeTruthy()
  })
})
