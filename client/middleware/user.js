export default async ({ $axios, $fatal, store, redirect, route }) => {
  if (store.getters['user/isNull']) {
    if (!localStorage.getItem('token') && !sessionStorage.getItem('token')) {
      redirect(`/login?redirect=${encodeURIComponent(route.fullPath)}`)
      return
    }

    const user = await $axios.$get('/user').catch(err => {
      localStorage.clear()
      sessionStorage.clear()

      if (err.response.status !== 401) $fatal(err)
      else redirect(`/login?redirect=${encodeURIComponent(route.fullPath)}`)
    })

    if (!user) {
      return
    }

    store.commit('user/set', user)
  }

  if (store.getters['accounts/isNull']) {
    const accounts = await $axios.get('/accounts').catch($fatal)

    store.commit('accounts/set', accounts.data.accounts)
  }

  if (store.getters['folders/isNull']) {
    const folders = await $axios.get('/folders').catch($fatal)

    store.commit('folders/set', folders.data.folders)
  }
}
