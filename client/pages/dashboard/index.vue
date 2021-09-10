<template>
  <div>
    <Heading title="All Accounts" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  layout: 'dashboard',
  async asyncData({ $api, $axios, $fatal, route }) {
    // pass
  },
  computed: {
    ...mapGetters('accounts', ['get']),
  },
}
</script>

<style scoped lang="scss">
#overview-icon {
  width: 120px;
  height: 120px;
}
</style>
