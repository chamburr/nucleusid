<template>
  <div class="form-group d-flex flex-column" :class="[{ focused: focused }]">
    <slot v-bind="slotData">
      <slot name="before">
        <label v-if="label" :for="id" class="input-label d-block mb-2" :class="labelClasses">
          {{ label }}
        </label>
      </slot>
      <div v-if="!multiline" class="input-group">
        <input
          :id="id"
          v-model="realValue"
          v-bind="$attrs"
          class="form-control"
          :class="inputClasses"
          :type="showPassword ? 'text' : type"
          aria-describedby="addon-right addon-left"
          v-on="listeners"
        />
        <div
          v-if="type === 'password' || copy"
          class="input-group-append bg-dark px-2 align-items-center"
        >
          <BaseButton
            v-if="type === 'password'"
            :icon="showPassword ? 'fas eye-slash' : 'fas eye'"
            type=""
            text-color="light"
            :icon-only="true"
            @click="showPassword = !showPassword"
          />
          <BaseButton
            v-if="copy"
            icon="fas copy"
            type=""
            text-color="light"
            :icon-only="true"
            @click="copyValue"
          />
        </div>
      </div>
      <textarea
        v-else
        :id="id"
        v-model="realValue"
        v-bind="$attrs"
        class="form-control"
        :class="inputClasses"
        v-on="listeners"
      ></textarea>
    </slot>
  </div>
</template>

<script>
export default {
  name: 'BaseInput',
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
    required: {
      type: Boolean,
      default: false,
    },
    inputClasses: {
      type: String,
      default: 'bg-dark border-0 text-white',
    },
    labelClasses: {
      type: String,
      default: '',
    },
    type: {
      type: String,
      default: 'text',
    },
    value: {
      default: '',
    },
    multiline: {
      type: Boolean,
      default: false,
    },
    copy: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      focused: false,
      realValue: this.value,
      showPassword: false,
    }
  },
  computed: {
    listeners() {
      return {
        focus: this.onFocus,
        blur: this.onBlur,
      }
    },
    slotData() {
      return {
        ...this.listeners,
        focused: this.focused,
      }
    },
  },
  watch: {
    value(newValue) {
      if (typeof newValue === 'string' || typeof newValue === 'number') {
        this.realValue = newValue
      }
    },
    realValue(newValue) {
      if (this.type === 'number') {
        if (typeof newValue === 'string' && newValue.startsWith('0')) {
          while (newValue.charAt(0) === '0') {
            newValue = newValue.substring(1)
          }
          newValue = parseInt(newValue, 10) || ''
        }
        if (this.required && newValue === '') {
          newValue = 0
        }
      }
      this.realValue = newValue
      this.$emit('input', this.realValue)
    },
  },
  methods: {
    onFocus(value) {
      this.focused = true
      this.$emit('focus', value)
    },
    onBlur(value) {
      this.focused = false
      this.$emit('blur', value)
    },
    async copyValue() {
      await navigator.clipboard.writeText(this.realValue)
      this.$toast.success('Copied to clipboard.')
    },
  },
}
</script>

<style scoped lang="scss">
.input-label {
  font-size: 1rem;
  font-weight: 500;
}

.input-group-append {
  border-radius: 0 0.25em 0.25em 0;

  /deep/ .icon {
    display: flex !important;
  }
}
</style>
