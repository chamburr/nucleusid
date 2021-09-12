<template>
  <div>
    <BaseModal
      :id="`account-modal-${element.id}`"
      :title="create ? 'Add Account' : 'Account Settings'"
      :ok-title="create ? 'Add' : 'Update'"
      @ok="create ? createAccount() : updateAccount()"
      @cancel="reset"
    >
      <template v-if="create">
        <p>Folder</p>
        <BaseSelect
          v-model="folder"
          class="mb-3"
          :options="folders"
          model-key="id"
          label="name"
          :allow-empty="false"
        />
      </template>
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
      <template v-if="!create">
        <p>Actions</p>
        <BaseButton type="primary" size="sm" @click="showChangeFolder">Change folder</BaseButton>
        <BaseButton type="danger" size="sm" @click="deleteAccount">Delete</BaseButton>
      </template>
    </BaseModal>
    <BaseModal
      v-if="!create"
      :id="`account-folder-modal-${element.id}`"
      title="Change Folder"
      ok-title="Update"
      @cancel="folder = element.folder"
      @ok="changeFolder"
    >
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
      default: () => ({ id: '' }),
    },
    create: {
      type: Boolean,
      default: false,
    },
    defaultFolder: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      name: this.element.name ?? '',
      username: this.element.username ?? '',
      password: this.element.password ?? '',
      note: this.element.note ?? '',
      folder: this.element.folder ?? this.defaultFolder,
    }
  },
  computed: {
    ...mapGetters('folders', { folders: 'get' }),
  },
  methods: {
    reset() {
      this.name = this.element.name ?? ''
      this.username = this.element.username ?? ''
      this.password = this.element.password ?? ''
      this.note = this.element.note ?? ''
      this.folder = this.element.folder ?? this.defaultFolder
    },
    showChangeFolder() {
      this.$bvModal.show(`account-folder-modal-${this.element.id}`)
    },
    async changeFolder() {
      await this.$axios
        .put(`/accounts/${this.element.id}/folder`, { folder: this.folder })
        .then(() => {
          this.$store.commit('accounts/update', { id: this.element.id, folder: this.folder })
          this.$toast.success('Updated the folder.')
        })
        .catch(this.$error)
    },
    checkAccount() {
      if (!this.name) {
        this.$toast.danger('Name cannot be empty.')
        return false
      }

      if (!this.username) {
        this.$toast.danger('Username cannot be empty.')
        return false
      }

      if (!this.password) {
        this.$toast.danger('Password cannot be empty.')
        return false
      }

      if (this.name.length > 64) {
        this.$toast.danger('Note must be 64 characters and below.')
        return false
      }

      if (this.username.length > 256) {
        this.$toast.danger('Username must be 256 characters and below.')
        return false
      }

      if (this.password.length > 256) {
        this.$toast.danger('Password must be 256 characters and below.')
        return false
      }

      if (this.note.length > 1024) {
        this.$toast.danger('Note must be 1024 characters and below.')
        return false
      }

      return true
    },
    async createAccount() {
      if (!this.checkAccount()) return

      await this.$axios
        .post(`/accounts`, {
          folder: this.folder,
          name: this.name,
          username: this.username,
          password: this.password,
          note: this.note,
        })
        .then(res => {
          this.reset()
          this.$store.commit('accounts/add', res.data)
          this.$toast.success('Created the account.')
        })
        .catch(this.$error)
    },
    async updateAccount() {
      if (!this.checkAccount()) return

      await this.$axios
        .patch(`/accounts/${this.element.id}`, {
          name: this.name,
          username: this.username,
          password: this.password,
          note: this.note,
        })
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
  },
}
</script>

<style scoped lang="scss">
.account-add-note {
  /deep/ textarea {
    resize: none;
    height: 6em;
  }
}
</style>
