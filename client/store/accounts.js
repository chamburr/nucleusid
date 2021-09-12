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
  update(state, { id, name, username, password, note, folder }) {
    const account = state.accounts.find(element => element.id === id)

    if (name != null || username != null || password != null || note != null) {
      account.name = name
      account.username = username
      account.password = password
      account.note = note
    }

    if (folder != null) {
      account.folder = folder
    }
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
