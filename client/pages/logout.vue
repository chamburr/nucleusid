<template>
  <div>
    <Heading title="Redirecting..." />
  </div>
</template>

<script>
export default {
  async mounted() {
    await this.$axios
      .post('/auth/logout')
      .then(async () => {
        this.$store.commit('accounts/reset')
        this.$store.commit('devices/reset')
        this.$store.commit('folders/reset')
        this.$store.commit('shares/reset')
        this.$store.commit('user/reset')

        localStorage.clear()
        sessionStorage.clear()

        this.$toast.success('You have logged out successfully.')
        await this.$router.push('/login')
      })
      .catch(this.$fatal)
  },
}
</script>
