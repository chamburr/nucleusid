export default ({ $axios, $moment }, inject) => {
  inject('utils', {
    checkEmail(element) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(element)
    },
  })
}
