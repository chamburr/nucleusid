<template>
  <div
    class="card"
    :class="[
      { 'card-button': button },
      { [`shadow-${shadowSize}`]: shadowSize },
      { [`bg-${type}`]: type },
      { shadow: shadow },
    ]"
    v-on="$listeners"
  >
    <div v-if="$slots.header" class="card-header" :class="headerClasses">
      <slot name="header"></slot>
    </div>
    <div class="card-body" :class="bodyClasses">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="card-footer" :class="footerClasses">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    type: {
      type: String,
      default: '',
    },
    button: {
      type: Boolean,
      default: false,
    },
    shadow: {
      type: Boolean,
      default: true,
    },
    shadowSize: {
      type: String,
      default: '',
    },
    bodyClasses: {
      type: [String, Object],
      default: '',
    },
    headerClasses: {
      type: [String, Object],
      default: '',
    },
    footerClasses: {
      type: [String, Object],
      default: '',
    },
  },
}
</script>

<style scoped lang="scss">
.card-button:hover {
  @include box-shadow($btn-hover-box-shadow);

  transform: translateY(-1px);
  cursor: pointer;
}
</style>
