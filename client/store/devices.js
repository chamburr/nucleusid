export const state = () => ({
  devices: [],
})

export const mutations = {
  set(state, devices) {
    state.devices = [...devices]
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
