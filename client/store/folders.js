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
  update(state, { id, name, sharing }) {
    const folder = state.folders.find(element => element.id === id)

    if (name) {
      folder.name = name
    }

    if (sharing != null) {
      folder.sharing = sharing
      folder.shares = []
    }
  },
  remove(state, id) {
    state.folders = state.folders.filter(element => element.id !== id)
  },
  setShare(state, { id, shares }) {
    state.folders.find(element => element.id === id).shares = [...shares]
  },
  addShare(state, { id, share }) {
    state.folders.find(element => element.id === id).shares.push(Object.assign({}, share))
  },
  updateShare(state, { id, person, viewOnly }) {
    state.folders
      .find(element => element.id === id)
      .shares.find(element => element.person === person).view_only = viewOnly
  },
  removeShare(state, { id, person }) {
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
  isNull(state) {
    return state.folders.length === 0
  },
}
