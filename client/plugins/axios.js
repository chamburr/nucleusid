export default ({ $axios }) => {
  $axios.onRequest(config => {
    const token = localStorage.getItem('token') ?? sessionStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  })
}
