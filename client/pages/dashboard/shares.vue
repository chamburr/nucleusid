<template>
  <div>
    <Heading title="Shares" />
    <h2 class="mb-4">Pending</h2>
    <Card
      v-for="element in pendingShares"
      :key="`pending${element.folder}`"
      class="bg-dark mb-4"
      body-classes="py-3"
    >
      <div class="d-flex justify-content-between align-items-center">
        <p class="font-weight-bold mb-0">{{ element.folder_name }}</p>
        <div>
          <BaseButton
            type="success"
            class="align-self-center"
            size="sm"
            @click="acceptShare(element.folder)"
          >
            Accept
          </BaseButton>
          <BaseButton
            type="danger"
            class="align-self-center"
            size="sm"
            @click="deleteShare(element.folder)"
          >
            Delete
          </BaseButton>
        </div>
      </div>
    </Card>
    <h2 class="mb-4">Confirmed</h2>
    <Card
      v-for="element in confirmedShares"
      :key="`confirmed-${element.folder}`"
      class="bg-dark mb-4"
      body-classes="py-3"
    >
      <div class="d-flex justify-content-between align-items-center">
        <p class="font-weight-bold mb-0">{{ element.folder_name }}</p>
        <BaseButton
          type="danger"
          class="align-self-center"
          size="sm"
          @click="deleteShare(element.folder)"
        >
          Delete
        </BaseButton>
      </div>
    </Card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  layout: 'dashboard',
  meta: {
    title: 'Shares',
  },
  async asyncData({ $axios, store, $fatal }) {
    if (store.getters['shares/isNull']) {
      const shares = await $axios.get('/shares').catch($fatal)
      store.commit('shares/set', shares.data.shares)
    }
  },
  data() {
    return {}
  },
  computed: {
    ...mapGetters('shares', { shares: 'get' }),
    pendingShares() {
      return this.shares.filter(element => !element.owner && !element.confirmed)
    },
    confirmedShares() {
      return this.shares.filter(element => !element.owner && element.confirmed)
    },
  },
  methods: {
    async acceptShare(id) {
      await this.$axios
        .post(`/shares/${id}`)
        .then(async () => {
          this.$store.commit('shares/update', { id, confirmed: true })
          this.$toast.success('Accepted the share.')
          await this.updateFolders()
        })
        .catch(this.$error)
    },
    async deleteShare(id) {
      await this.$axios
        .delete(`/shares/${id}`)
        .then(async () => {
          this.$store.commit('shares/remove', id)
          this.$toast.success('Deleted the share.')
          await this.updateFolders()
        })
        .catch(this.$error)
    },
    async updateFolders() {
      const folders = await this.$axios.get('/folders').catch(this.$error)
      this.$store.commit('folders/set', folders.data.folders)
    },
  },
}
</script>
