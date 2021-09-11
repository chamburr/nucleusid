export const state = () => ({
  devices: [],
})

export const mutations = {
  set(state, devices) {
    state.devices = [...devices]
  },
  remove(state, id) {
    state.devices = state.devices.filter(element => element.id !== id)
  },
  reset(state) {
    state.devices = []
  },
}

export const getters = {
  get(state) {
    return [...state.devices]
  },
  isNull(state) {
    return state.devices.length === 0
  },
}
