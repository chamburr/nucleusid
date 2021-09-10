<template>
  <div>
    <Heading :title="article.title">
      {{ article.description }}
    </Heading>
    <NuxtContent :document="article" />
  </div>
</template>

<script>
export default {
  async asyncData({ $content, route }) {
    return {
      article: await $content(`support/${route.params.id}`).fetch(),
    }
  },
  head() {
    return {
      title: this.article.title,
    }
  },
}
</script>
