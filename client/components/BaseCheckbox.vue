<template>
  <div class="custom-control custom-checkbox pr-2 checkbox-container">
    <input
      :id="id"
      v-model="realValue"
      v-bind="$attrs"
      class="custom-control-input"
      :class="inputClasses"
      type="checkbox"
    />
    <label :for="id" class="custom-control-label checkbox-label">
      {{ label }}
    </label>
  </div>
</template>
<script>
export default {
  name: 'BaseCheckbox',
  inheritAttrs: false,
  props: {
    id: {
      type: String,
      default: '',
    },
    label: {
      type: String,
      default: '',
    },
    inputClasses: {
      type: String,
      default: '',
    },
    value: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      realValue: this.value,
    }
  },
  watch: {
    value(newValue) {
      this.realValue = newValue
    },
    realValue(newValue) {
      this.$emit('input', newValue)
    },
  },
}
</script>

<style scoped lang="scss">
.checkbox-container {
  padding-left: 2rem;
}

.checkbox-label {
  font-size: 1rem !important;
  font-weight: 500;
}

.custom-control-label::before,
.custom-control-label::after {
  left: -2rem;
}
</style>
