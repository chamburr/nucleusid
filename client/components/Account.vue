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
    <AccountModal :element="element" />
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
      this.$bvModal.show(`account-modal-${this.element.id}`)
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
