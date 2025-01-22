import { createStore, Store } from 'vuex'
import { InjectionKey } from 'vue'

// 定义 state 类型
export interface State {
  // 添加具体的 state 类型定义
}

// 定义 injection key
export const key: InjectionKey<Store<State>> = Symbol()

const isDev = import.meta.env.DEV

export default createStore<State>({
  state: {},
  mutations: {},
  actions: {},
  modules: {}
})
