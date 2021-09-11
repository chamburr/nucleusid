<template>
  <div class="pb-4">
    <div :class="$slots.trailing ? 'd-flex justify-content-between' : ''">
      <h1 class="display-2 mb-0">{{ title }}</h1>
      <slot name="trailing"></slot>
    </div>
    <p class="heading-description"><slot></slot></p>
  </div>
</template>

<script>
export default {
  name: 'Heading',
  props: {
    title: {
      type: String,
      default: '',
    },
  },
}
</script>

<style scoped lang="scss">
.heading-description {
  font-size: 1.15em;
}
</style>
