export const state = () => ({
  shares: [],
  isNull: true,
})

export const mutations = {
  set(state, shares) {
    state.shares = [...shares]
    state.isNull = false
  },
  add(state, share) {
    state.shares.push(Object.assign({}, share))
  },
  remove(state, id) {
    state.shares = state.shares.filter(element => element.folder !== id)
  },
  reset(state) {
    state.shares = []
    state.isNull = true
  },
}

export const getters = {
  get(state) {
    return [...state.shares]
  },
  isNull(state) {
    return state.isNull
  },
}
