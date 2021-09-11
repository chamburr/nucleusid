<template>
  <BModal
    v-bind="$attrs"
    :id="id"
    :centered="true"
    header-bg-variant="gray"
    body-bg-variant="gray"
    footer-bg-variant="gray"
    :cancel-variant="cancelVariant"
    :ok-variant="okVariant"
    :title="title"
    v-on="$listeners"
  >
    <slot></slot>
    <template #modal-footer>
      <slot name="folder"></slot>
    </template>
  </BModal>
</template>

<script>
export default {
  name: 'BaseModal',
  props: {
    id: {
      type: String,
      default: '',
    },
    title: {
      type: String,
      default: '',
    },
    cancelVariant: {
      type: String,
      default: 'gray',
    },
    okVariant: {
      type: String,
      default: 'success',
    },
  },
}
</script>
