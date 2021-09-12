<template>
  <div>
    <Heading title="Privacy Policy">
      This Privacy Policy describes our policies and procedures on the collection, use, and
      disclosure of your personal information when you access or use NucleusID's website and
      services.
    </Heading>
    <NuxtContent :document="privacy" />
  </div>
</template>

<script>
export default {
  async asyncData({ $content }) {
    return {
      privacy: await $content('privacy').fetch(),
    }
  },
  head: {
    title: 'Privacy Policy',
  },
}
</script>
