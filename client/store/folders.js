export const state = () => ({
  folders: [],
})

export const mutations = {
  set(state, folders) {
    state.folders = [...folders.map(element => ({ shares: [], ...element }))]
  },
  add(state, folder) {
    state.folders.push(Object.assign({ shares: [] }, folder))
  },
  remove(state, id) {
    state.folders = state.folders.filter(element => element.id !== id)
  },
  setShare(state, id, shares) {
    state.folders.find(element => element.id === id).shares = [...shares]
  },
  addShare(state, id, share) {
    state.folders.find(element => element.id === id).shares.push(Object.assign({}, share))
  },
  removeShare(state, id, person) {
    const folder = state.folders.find(element => element.id === id)
    folder.shares = folder.shares.filter(element => element.person !== person)
  },
  reset(state) {
    state.folders = []
  },
}

export const getters = {
  get(state) {
    return [...state.folders]
  },
  getById(state, id) {
    return {
      ...(state.folders.find(element => element.id === id) ?? {}),
    }
  },
  isNull(state) {
    return state.folders.length === 0
  },
  isShareNull(state, id) {
    const folder = state.folders.find(element => element.id === id)
    return folder.sharing === false || folder.shares.length === 0
  },
}
