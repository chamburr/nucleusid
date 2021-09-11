export const state = () => ({
  shares: [],
  isNull: true,
})

export const mutations = {
  set(state, shares) {
    state.shares = [...shares]
    state.isNull = false
  },
  update(state, { id, confirmed }) {
    state.shares.find(element => element.folder === id).confirmed = confirmed
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
