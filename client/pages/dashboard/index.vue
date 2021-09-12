<template>
  <div>
    <Heading title="All Accounts">
      <template slot="trailing">
        <BaseButton type="success" class="align-self-center" size="sm" @click="showAccountModal">
          Add account
        </BaseButton>
      </template>
    </Heading>
    <BaseInput v-model="search" placeholder="Search..." class="mb-4" />
    <div class="row">
      <div v-for="element in activeAccounts" :key="element.id" class="col-12 col-lg-6">
        <Account :element="element" />
      </div>
    </div>
    <AccountModal :create="true" :default-folder="defaultFolder.id" />
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
    ...mapGetters('folders', { folders: 'get' }),
    activeAccounts() {
      return this.accounts.filter(
        element =>
          element.name.toLowerCase().includes(this.search.toLowerCase()) ||
          element.username.toLowerCase().includes(this.search.toLowerCase())
      )
    },
    defaultFolder() {
      return this.folders.find(element => element.built_in === true)
    },
  },
  methods: {
    showAccountModal() {
      this.$bvModal.show('account-modal-')
    },
  },
}
</script>
