declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

interface ImportMeta {
  readonly env: {
    MODE: string
    DEV: boolean 
    PROD: boolean
    BASE_URL: string
    VITE_APP_TITLE: string
  }
}
