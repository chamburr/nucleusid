<template>
  <div>
    <Heading title="Register" />
    <div class="col-12 col-md-8 col-lg-6 px-0">
      <BaseInput
        id="register-name"
        v-model="name"
        type="text"
        class="mb-4"
        :required="true"
        label="Name"
      />
      <BaseInput
        id="register-email"
        v-model="email"
        type="email"
        class="mb-4"
        :required="true"
        label="Email"
      />
      <BaseInput
        id="register-password"
        v-model="password"
        type="password"
        class="mb-4"
        :required="true"
        label="Password"
      />
    </div>
    <div class="d-flex mt-5">
      <BaseButton type="primary" class="mr-3" @click="register">
        <span class="h6 font-weight-bold">Register</span>
      </BaseButton>
      <NuxtLink to="/login">
        <BaseButton type="">
          <span class="h6 font-weight-bold text-light">Login</span>
        </BaseButton>
      </NuxtLink>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
    }
  },
  head: {
    title: 'Register',
  },
  mounted() {
    if (localStorage.getItem('token') ?? sessionStorage.getItem('token')) {
      this.$router.push('/dashboard')
    }
  },
  methods: {
    async register() {
      if (!this.name) {
        this.$toast.danger('Name cannot be empty.')
        return
      }

      if (!this.email) {
        this.$toast.danger('Email cannot be empty.')
        return
      }

      if (!this.password) {
        this.$toast.danger('Password cannot be empty.')
        return
      }

      if (this.name.length > 64) {
        this.$toast.danger('Name must be less than 64 characters.')
        return
      }

      if (!this.$utils.checkEmail(this.email) || this.email.length < 6 || this.email.length > 256) {
        this.$toast.danger('Email address must be valid.')
        return
      }

      if (this.password.length < 8 || this.email.length > 256) {
        this.$toast.danger('Password must be between 8 and 256 characters.')
        return
      }

      await this.$axios
        .$post(`/auth/register`, { name: this.name, email: this.email, password: this.password })
        .then(() => {
          this.$toast.success('Your account is registered successfully.')
          this.$router.push('/login')
        })
        .catch(this.$error)
    },
  },
}
</script>
