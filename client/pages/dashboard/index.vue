<template>
  <div>
    <Heading title="All Accounts" />
    <BaseInput v-model="search" placeholder="Search..." class="mb-4" />
    <div class="row">
      <div v-for="element in activeAccounts" :key="element.id" class="col-12 col-lg-6">
        <Account :element="element" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  layout: 'dashboard',
  meta: {
    title: 'All Accounts',
  },
  data() {
    return {
      search: '',
    }
  },
  computed: {
    ...mapGetters('accounts', { accounts: 'get' }),
    activeAccounts() {
      return this.accounts.filter(
        element =>
          element.name.toLowerCase().includes(this.search.toLowerCase()) ||
          element.username.toLowerCase().includes(this.search.toLowerCase())
      )
    },
  },
}
</script>
