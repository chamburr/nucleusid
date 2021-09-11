<template>
  <div>
    <Heading title="Settings" />
    <h2 class="mb-4">Profile</h2>
    <BaseInput id="settings-name" v-model="name" class="mb-4" label="Name" />
    <BaseInput
      id="settings-email"
      v-model="email"
      type="email"
      class="mb-4"
      :label="`Email (${user.verified ? 'verified' : 'not verified'})`"
    />
    <BaseButton type="success" @click="updateProfile">Update profile</BaseButton>
    <BaseButton v-if="!user.verified" type="primary" @click="resendVerification"
      >Resend verification email</BaseButton
    >
    <h2 class="mt-5 mb-4">Security</h2>
    <BaseInput
      id="settings-old-password"
      v-model="oldPassword"
      type="password"
      class="mb-4"
      label="Current password"
    />
    <BaseInput
      id="settings-password"
      v-model="newPassword"
      type="password"
      class="mb-4"
      label="New password"
    />
    <BaseButton type="success" @click="updatePassword">Update password</BaseButton>
    <h2 class="mt-5 mb-4">Devices</h2>
    <Card
      v-for="element in devices"
      :key="element.id"
      class="bg-dark mb-4"
      body-classes="py-3"
      :button="true"
      @click="showDevice(element)"
    >
      <div class="d-flex justify-content-between">
        <p class="font-weight-bold mb-0">{{ element.name }}</p>
        <p v-if="element.current" class="text-light mb-0">This device</p>
      </div>
    </Card>
    <h2 class="mt-5 mb-4">Danger Zone</h2>
    <BaseButton type="danger" @click="showDeleteUser">Delete account</BaseButton>
    <BaseModal
      id="settings-device-modal"
      :title="device.name"
      ok-variant="danger"
      ok-title="Log out"
      @cancel="device = {}"
      @ok="deleteDevice(device.id)"
    >
      <p class="mb-0">
        IP address: {{ device.ip_address }}
        <br />
        Location: {{ device.location }}
        <br />
        Last login: {{ device.last_login }}
        <br />
        Created at: {{ device.created_at }}
      </p>
    </BaseModal>
    <BaseModal
      id="settings-delete-modal"
      title="Delete account"
      ok-variant="danger"
      ok-title="Delete"
      @cancel="deletePassword = ''"
      @ok="deleteUser"
    >
      <p>This will permanently delete your account. It is irreversible.</p>
      <BaseInput
        id="settings-delete-password"
        v-model="deletePassword"
        type="password"
        label="Password"
      />
    </BaseModal>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  layout: 'dashboard',
  meta: {
    title: 'Settings',
  },
  async asyncData({ $axios, store, $fatal }) {
    if (store.getters['devices/isNull']) {
      const devices = await $axios.get('/devices').catch($fatal)
      store.commit('devices/set', devices.data.devices)
    }
  },
  data() {
    return {
      name: '',
      email: '',
      oldPassword: '',
      newPassword: '',
      deletePassword: '',
      device: {},
    }
  },
  computed: {
    ...mapGetters('user', { user: 'get' }),
    ...mapGetters('devices', { devices: 'get' }),
  },
  mounted() {
    this.name = this.user.name
    this.email = this.user.email
  },
  methods: {
    async updateProfile() {
      if (!this.name) {
        this.$toast.danger('Name cannot be empty.')
        return
      }

      if (!this.email) {
        this.$toast.danger('Email cannot be empty.')
        return
      }

      if (this.name.length > 64) {
        this.$toast.danger('Name must be less than 64 characters.')
        return
      }

      if (!this.$utils.checkEmail(this.email) || this.email.length < 6 || this.email.length > 256) {
        this.$toast.danger('Email address must be valid.')
      }

      await this.$axios
        .patch('/user', {
          name: this.name,
          email: this.email,
        })
        .then(async () => {
          await this.$axios
            .get('/user')
            .then(res => {
              this.$store.commit('user/set', res.data)
            })
            .catch(this.$error)
        })
        .catch(this.$error)
    },
    async resendVerification() {
      await this.$axios
        .post('/user/resend_verify')
        .then(() => {
          this.$toast.success('Sent verification email.')
        })
        .catch(this.$error)
    },
    async updatePassword() {
      if (!this.oldPassword) {
        this.$toast.danger('Old password cannot be empty.')
        return
      }

      if (!this.newPassword) {
        this.$toast.danger('Password cannot be empty.')
        return
      }

      if (this.oldPassword.length < 8 || this.oldPassword.length > 256) {
        this.$toast.danger('Old password must be between 8 and 256 characters.')
        return
      }

      if (this.newPassword.length < 8 || this.newPassword.length > 256) {
        this.$toast.danger('Password must be between 8 and 256 characters.')
        return
      }

      await this.$axios
        .put('/user/password', {
          old_password: this.oldPassword,
          password: this.newPassword,
        })
        .then(() => {
          this.$toast.success('Changed the password.')
          setTimeout(() => window.location.reload(), 2000)
        })
        .catch(this.$error)
    },
    showDevice(device) {
      this.device = device
      this.$bvModal.show('settings-device-modal')
    },
    async deleteDevice(id) {
      if (this.devices.find(element => element.current).id === id) {
        await this.$router.push('/logout')
        return
      }

      await this.$axios
        .delete(`/devices/${id}`)
        .then(() => {
          this.$store.commit('devices/remove', id)
          this.$toast.success('Logged out of the device.')
        })
        .catch(this.$error)
    },
    showDeleteUser() {
      this.$bvModal.show('settings-delete-modal')
    },
    async deleteUser() {
      if (!this.deletePassword) {
        this.$toast.danger('Password cannot be empty.')
      }

      await this.$axios
        .delete('/user', { data: { password: this.deletePassword } })
        .then(() => {
          this.$toast.success('Deleted account.')
          setTimeout(() => window.location.reload(), 2000)
        })
        .catch(this.$error)
    },
  },
}
</script>
