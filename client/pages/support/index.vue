<template>
  <div>
    <Heading title="Support">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum porta velit
      consequat sagittis.
    </Heading>
    <BaseInput v-model="search" placeholder="Search..." class="mb-4" />
    <div class="row">
      <div
        v-for="element in activeArticles"
        :key="element.slug"
        class="col-12 col-md-6 mt-4 mt-md-0 pb-4"
      >
        <NuxtLink :to="`/support/${element.slug}`">
          <Card class="support-card bg-dark h-100">
            <div class="text-center">
              <p class="h5 font-weight-bold">{{ element.title }}</p>
              <p class="mb-0 text-light">{{ element.description }}</p>
            </div>
          </Card>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async asyncData({ $content }) {
    return {
      articles: await $content('support').fetch(),
    }
  },
  data() {
    return {
      search: '',
    }
  },
  head: {
    title: 'Support',
  },
  computed: {
    activeArticles() {
      return this.articles.filter(
        element =>
          element.title.toLowerCase().includes(this.search.toLowerCase()) ||
          element.description.toLowerCase().includes(this.search.toLowerCase())
      )
    },
  },
}
</script>

<style scoped lang="scss">
.support-card {
  box-sizing: border-box;
}
</style>
