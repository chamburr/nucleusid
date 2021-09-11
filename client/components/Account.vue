<template>
  <div class="btn pb-4 px-0 h-100 w-100">
    <Card
      class="account-card bg-dark h-100"
      body-classes="d-flex flex-column justify-content-between"
      @click="showSettings"
    >
      <p class="h5 font-weight-bold">{{ element.name }}</p>
      <p class="mb-0 text-light">{{ element.username }}</p>
    </Card>
    <BaseModal
      :id="`account-modal-${element.id}`"
      title="Account Settings"
      ok-title="Update"
      @ok="updateSettings"
      @cancel="
        name = element.name
        username = element.username
        password = element.password
        note = element.note
      "
    >
      <BaseInput :id="`account-name-${element.id}`" v-model="name" label="Name" />
      <BaseInput
        :id="`account-username-${element.id}`"
        v-model="username"
        label="Username"
        :copy="true"
      />
      <BaseInput
        :id="`account-password-${element.id}`"
        v-model="password"
        type="password"
        label="Password"
        :copy="true"
      />
      <BaseInput
        :id="`account-note-${element.id}`"
        v-model="note"
        class="account-note"
        label="Note"
        multiline
      />
      <p>Actions</p>
      <BaseButton type="primary" size="sm" @click="changeFolder">Change folder</BaseButton>
      <BaseButton type="danger" size="sm" @click="deleteAccount">Delete</BaseButton>
    </BaseModal>
    <BaseModal :id="`account-folder-modal-${element.id}`" title="Change Folder" ok-title="Update">
      <BaseSelect
        v-model="folder"
        :options="folders"
        model-key="id"
        label="name"
        :allow-empty="false"
      />
    </BaseModal>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Account',
  props: {
    element: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      name: this.element.name,
      username: this.element.username,
      password: this.element.password,
      note: this.element.note,
      folder: this.element.folder,
    }
  },
  computed: {
    ...mapGetters('folders', { folders: 'get' }),
  },
  methods: {
    showSettings() {
      this.$bvModal.show(`account-folder-modal-${this.element.id}`)
      // this.$bvModal.show(`account-modal-${this.element.id}`)
    },
    async updateSettings() {
      await this.$axios
        .patch(`/accounts/${this.element.id}`)
        .then(() => {
          this.$store.commit('accounts/update', {
            id: this.element.id,
            name: this.name,
            username: this.username,
            password: this.password,
            note: this.note,
          })
          this.$toast.success('Updated the account.')
        })
        .catch(this.$error)
    },
    async deleteAccount() {
      await this.$axios
        .delete(`/accounts/${this.element.id}`)
        .then(() => {
          this.$store.commit('accounts/remove', this.element.id)
          this.$toast.success('Removed the account.')
        })
        .catch(this.$error)
    },
    showChangeFolder() {
      this.$bvModal.show(`account-folder-modal-${this.element.id}`)
    },
  },
}
</script>

<style scoped lang="scss">
.account-card:hover {
  @include box-shadow($btn-hover-box-shadow);

  transform: translateY(-1px);
}

.account-note {
  /deep/ textarea {
    resize: none;
    height: 6em;
  }
}
</style>
