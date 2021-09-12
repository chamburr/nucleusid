<template>
  <div>
    <Heading :title="folder.name">
      <template slot="trailing">
        <div>
          <BaseButton type="success" class="align-self-center" size="sm" @click="showAccountModal">
            Add account
          </BaseButton>
          <BaseButton
            v-if="!folder.built_in"
            type="primary"
            class="align-self-center"
            size="sm"
            @click="showSettings"
          >
            Settings
          </BaseButton>
        </div>
      </template>
    </Heading>
    <BaseInput v-model="search" placeholder="Search..." class="mb-4" />
    <div class="row">
      <div v-for="element in activeAccounts" :key="element.id" class="col-12 col-lg-6">
        <Account :element="element" />
      </div>
    </div>
    <BaseModal
      id="folder-modal"
      title="Folder Settings"
      ok-title="Update"
      @ok="updateSettings"
      @cancel="reset"
    >
      <BaseInput id="folder-name" v-model="name" label="Name" />
      <p>Sharing</p>
      <BaseButton
        v-if="!folder.sharing"
        class="mb-3"
        type="success"
        size="sm"
        @click="updateSharing(true)"
      >
        Enable sharing
      </BaseButton>
      <BaseButton v-else type="danger" size="sm" @click="updateSharing(false)">
        Disable sharing
      </BaseButton>
      <div v-if="folder.sharing" class="mt-4">
        <div class="d-flex mb-4">
          <BaseInput v-model="email" class="mr-3 flex-grow-1 mb-0" placeholder="Enter email" />
          <BaseButton type="primary" @click="addShare">Add</BaseButton>
        </div>
        <Card
          v-for="element in folder.shares"
          :key="element.person"
          class="bg-dark mb-3"
          body-classes="py-3"
        >
          <div
            v-b-toggle="`share-${element.person}`"
            class="d-flex justify-content-between align-items-center"
          >
            <p class="font-weight-bold mb-0">{{ element.person_email }}</p>
            <p class="text-light mb-0">
              {{ element.owner ? 'Owner' : element.view_only ? 'Read' : 'Read & write' }}
            </p>
          </div>
          <BCollapse :id="`share-${element.person}`" role="tabpanel">
            <div v-if="!element.owner" class="mt-2">
              <BaseButton
                type="primary"
                class="align-self-center"
                size="sm"
                @click="updateShare(element.person, !element.view_only)"
              >
                Change to {{ element.view_only ? 'read & write' : 'read only' }}
              </BaseButton>
              <BaseButton
                type="danger"
                class="align-self-center"
                size="sm"
                @click="deleteShare(element.person)"
              >
                Remove
              </BaseButton>
            </div>
            <div v-else>
              <p class="mt-2 mb-0">No actions available for owner.</p>
            </div>
          </BCollapse>
        </Card>
      </div>
      <p>Actions</p>
      <BaseButton type="danger" size="sm" @click="deleteFolder">Delete</BaseButton>
    </BaseModal>
    <AccountModal :create="true" :default-folder="folder.id" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  layout: 'dashboard',
  meta() {
    return {
      title: this.folder.name,
    }
  },
  data() {
    return {
      search: '',
      name: '',
      email: '',
    }
  },
  computed: {
    ...mapGetters('accounts', { accounts: 'get' }),
    ...mapGetters('folders', { folders: 'get' }),
    folder() {
      return this.folders.find(element => element.id === this.$route.params.id)
    },
    activeAccounts() {
      return this.accounts
        .filter(element => element.folder === this.folder.id)
        .filter(
          element =>
            element.name.toLowerCase().includes(this.search.toLowerCase()) ||
            element.username.toLowerCase().includes(this.search.toLowerCase())
        )
    },
  },
  async mounted() {
    if (!this.folder) {
      this.$nuxt.error({ statusCode: 404 })
      return
    }

    this.name = this.folder.name

    if (this.folder.sharing && this.folder.shares.length === 0) {
      await this.loadShares()
    }
  },
  methods: {
    reset() {
      this.name = this.folder.name
      this.email = ''
    },
    async loadShares() {
      await this.$axios
        .get(`/folders/${this.folder.id}/shares`)
        .then(res => {
          this.$store.commit('folders/setShare', { id: this.folder.id, shares: res.data.shares })
        })
        .catch(this.$fatal)
    },
    showSettings() {
      this.$bvModal.show('folder-modal')
    },
    showAccountModal() {
      this.$bvModal.show('account-modal-')
    },
    async updateSettings() {
      await this.$axios
        .patch(`/folders/${this.folder.id}`, {
          name: this.name,
        })
        .then(() => {
          this.$store.commit('folders/update', { id: this.folder.id, name: this.name })
          this.$toast.success('Updated the folder settings.')
        })
        .catch(this.$error)
    },
    async updateSharing(sharing) {
      await this.$axios
        .patch(`/folders/${this.folder.id}`, {
          sharing,
        })
        .then(async () => {
          this.$store.commit('folders/update', { id: this.folder.id, sharing })
          this.$toast.success('Updated the folder settings.')
          await this.loadShares()
        })
        .catch(this.$error)
    },
    async deleteFolder() {
      await this.$axios
        .delete(`/folders/${this.folder.id}`)
        .then(async () => {
          this.$store.commit('folders/remove', this.folder.id)
          this.$toast.success('Removed the folder.')
          await this.$router.push('/dashboard')
        })
        .catch(this.$error)
    },
    async addShare() {
      if (!this.email) {
        this.$toast.danger('Email cannot be empty')
        return
      }

      if (!this.$utils.checkEmail(this.email) || this.email.length < 6 || this.email.length > 256) {
        this.$toast.danger('Email address must be valid.')
        return
      }

      await this.$axios
        .post(`/folders/${this.folder.id}/shares`, { email: this.email, view_only: true })
        .then(res => {
          this.email = ''
          this.$store.commit('folders/addShare', { id: this.folder.id, share: res.data })
          this.$toast.success('Invited the user to the folder.')
        })
        .catch(this.$error)
    },
    async updateShare(id, viewOnly) {
      await this.$axios
        .patch(`/folders/${this.folder.id}/shares/${id}`, {
          view_only: viewOnly,
        })
        .then(() => {
          this.$store.commit('folders/updateShare', { id: this.folder.id, person: id, viewOnly })
          this.$toast.success('Updated the settings for the user.')
        })
        .catch(this.$error)
    },
    async deleteShare(id) {
      await this.$axios
        .delete(`/folders/${this.folder.id}/shares/${id}`)
        .then(() => {
          this.$store.commit('folders/removeShare', { id: this.folder.id, person: id })
          this.$toast.success('Removed the user from the folder.')
        })
        .catch(this.$error)
    },
  },
}
</script>
