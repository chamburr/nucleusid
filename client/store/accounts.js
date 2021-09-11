export const state = () => ({
  accounts: [],
  isNull: true,
})

export const mutations = {
  set(state, accounts) {
    state.accounts = [...accounts]
    state.isNull = false
  },
  add(state, account) {
    state.accounts.push(Object.assign({}, account))
  },
  update(state, { id, name, username, password, note }) {
    const account = state.accounts.find(element => element.id === id)

    account.name = name
    account.username = username
    account.password = password
    account.note = note
  },
  remove(state, id) {
    state.accounts = state.accounts.filter(element => element.id !== id)
  },
  reset(state) {
    state.accounts = []
    state.isNull = true
  },
}

export const getters = {
  get(state) {
    return [...state.accounts]
  },
  isNull(state) {
    return state.isNull
  },
}
