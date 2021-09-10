export default ({ $axios, $moment }, inject) => {
  inject('utils', {
    checkEmail(element) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(element)
    },
    clone(element) {
      return JSON.parse(JSON.stringify(element))
    },
    isEqual(before, after) {
      return JSON.stringify(before) === JSON.stringify(after)
    },
    isEmpty(element) {
      return Object.keys(element).length === 0
    },
    diff(before, after) {
      const diff = {}
      for (const element of Object.keys(before)) {
        const beforeString = JSON.stringify(before[element])
        const afterString = JSON.stringify(after[element])
        if (beforeString !== afterString) {
          diff[element] = JSON.parse(afterString)
        }
      }
      return diff
    },
  })
}
