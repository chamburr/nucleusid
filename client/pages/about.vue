<template>
  <div>
    <Heading title="About">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum porta velit
      consequat sagittis.
    </Heading>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non porta diam. Proin metus
      tortor, gravida pulvinar nunc quis, varius lacinia leo. Praesent in sapien ut ipsum lacinia
      lacinia. Cras non mi vel ipsum convallis rutrum a sed nulla.
    </p>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non porta diam. Proin metus
      tortor, gravida pulvinar nunc quis, varius lacinia leo. Praesent in sapien ut ipsum lacinia
      lacinia. Cras non mi vel ipsum convallis rutrum a sed nulla.
    </p>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non porta diam. Proin metus
      tortor, gravida pulvinar nunc quis, varius lacinia leo. Praesent in sapien ut ipsum lacinia
      lacinia. Cras non mi vel ipsum convallis rutrum a sed nulla.
    </p>
    <h2 class="mt-5 mb-4">Team</h2>
    <div class="row">
      <div
        v-for="element in people"
        :key="element.name"
        class="about-card col-12 col-md-6 col-lg-4 mt-4 mt-md-0 pb-4"
      >
        <Card class="bg-dark h-100" body-classes="d-flex flex-column text-center">
          <div class="pb-4">
            <img
              class="about-icon mw-100 mh-100 rounded-circle"
              :src="`${element.image}?size=512`"
              alt="Icon"
            />
          </div>
          <div class="flex-grow-1 d-flex flex-column">
            <p class="font-weight-bold h4">
              {{ element.name }}
            </p>
            <p class="about-description mb-0">{{ element.description }}</p>
            <div class="flex-grow-1 d-flex flex-column justify-content-end">
              <hr v-if="element.website || element.github" class="my-3" />
              <div>
                <a v-if="element.website" target="_blank" :href="element.website">
                  <BaseIcon name="fas globe" class="big" />
                </a>
                <a v-if="element.github" target="_blank" :href="element.github">
                  <BaseIcon name="fab github" class="big" />
                </a>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
    <h2 class="mt-5 mb-4">Contact Us</h2>
    <p>Email us at hi@chamburr.xyz! We hope to hear from you.</p>
  </div>
</template>

<script>
export default {
  async asyncData({ $getContent }) {
    return {
      people: await $getContent('about'),
    }
  },
  head: {
    title: 'About',
  },
}
</script>

<style scoped lang="scss">
.about-description {
  white-space: pre;
}

.about-card {
  box-sizing: border-box;
}

.about-icon {
  width: 160px;
  height: 160px;
}
</style>
