<template>
  <div>
    <Heading title="Verify">
      {{ verified ? 'Your email has been verified.' : 'Verifying your email...'}}
    </Heading>
  </div>
</template>

<script>
export default {
  data() {
    return {
      verified: false
    }
  },
  async mounted() {
    await this.$axios
      .post('/user/verify', {token: this.$route.query.token ?? ''})
      .then(async () => {
        this.verified = true
      })
      .catch(this.$fatal)
  },
}
</script>
