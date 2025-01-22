export interface NavLink {
  name: string
  path: string
  icon?: string
  children?: NavLink[]
  permissions?: string[]
}
