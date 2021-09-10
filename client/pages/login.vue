<template>
  <div>
    <Heading title="Login" />
    <div class="col-12 col-md-8 col-lg-6 px-0">
      <BaseInput
        id="login-email"
        v-model="email"
        type="email"
        class="mb-4"
        :required="true"
        label="Email"
      />
      <BaseInput
        id="login-password"
        v-model="password"
        type="password"
        class="mb-4"
        :required="true"
        label="Password"
      />
      <BaseCheckbox id="login-remember" v-model="remember" class="mb-4" label="Remember me" />
    </div>
    <div class="d-flex mt-5">
      <BaseButton type="primary" class="mr-3" @click="login">
        <span class="h6 font-weight-bold">Login</span>
      </BaseButton>
      <NuxtLink to="/register">
        <BaseButton type="">
          <span class="h6 font-weight-bold text-light">Register</span>
        </BaseButton>
      </NuxtLink>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      remember: true,
    }
  },
  head: {
    title: 'Login',
  },
  mounted() {
    if (localStorage.getItem('token') ?? sessionStorage.getItem('token')) {
      this.$router.push('/dashboard')
    }
  },
  methods: {
    async login() {
      if (!this.email) {
        this.$toast.danger('Email cannot be empty.')
        return
      }

      if (!this.password) {
        this.$toast.danger('Password cannot be empty.')
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
        .$post(`/auth/login`, { email: this.email, password: this.password })
        .then(res => {
          if (this.remember) localStorage.setItem('token', res.token)
          else sessionStorage.setItem('token', res.token)

          this.$toast.success('You have logged in successfully.')

          let redirect = this.$route.query.redirect ?? '/dashboard'
          if (!redirect.startsWith('/')) {
            redirect = '/dashboard'
          }

          this.$router.push(redirect)
        })
        .catch(this.$error)
    },
  },
}
</script>
