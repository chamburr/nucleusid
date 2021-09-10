<template>
  <div>
    <div id="hero-top-container">
      <div id="hero-top-content" class="container pt-2 pb-0">
        <div class="row h-100">
          <div class="hero-top-column col-12 col-md-7 text-center text-md-left">
            <div class="d-md-none text-center mt-5 mb-3">
              <img id="hero-top-icon-sm" src="~/static/icon.png" alt="Icon" />
            </div>
            <h1 class="display-1">NucleusID</h1>
            <h2 class="display-4">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum porta
              velit consequat sagittis.
            </h2>
            <div class="d-inline-block mt-3">
              <NuxtLink to="/dashboard">
                <BaseButton type="secondary" size="lg" class="mt-3 px-5 rounded-pill">
                  <span class="h5 font-weight-700 text-primary">Get Started</span>
                </BaseButton>
              </NuxtLink>
            </div>
          </div>
          <div class="hero-top-column col-md-5 d-none d-md-flex align-items-center">
            <img id="hero-top-icon" src="~/static/icon.png" alt="Icon" />
          </div>
        </div>
      </div>
      <img id="hero-top-wave" src="~/assets/images/hero-1.svg" alt="Hero" />
    </div>
    <div class="container text-center pb-5">
      <h2 class="display-2 mt-5 pb-3">About NucleusID</h2>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum porta velit
        consequat sagittis.
      </p>
      <h2 class="display-2 mt-5 pb-3">Features</h2>
      <div
        v-for="element in [0, 1, 2, 3]"
        :key="element"
        class="home-feature-container row pb-5 d-flex flex-md-row"
        :class="{ 'flex-column-reverse': element % 2 === 0 }"
      >
        <div
          v-if="element % 2 === 1"
          class="home-feature-column feature-icon col-12 col-md-6 align-items-center"
        >
          <p>insert placeholder image</p>
        </div>
        <div class="home-feature-column feature-text col-12 col-md-6 mt-4 mt-md-0">
          <h3 class="display-4">Lorem ipsum dolor sit amet</h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non porta diam. Proin metus
            tortor, gravida pulvinar nunc quis, varius lacinia leo. Praesent in sapien ut ipsum
            lacinia lacinia. Cras non mi vel ipsum convallis rutrum a sed nulla.
          </p>
        </div>
        <div
          v-if="element % 2 === 0"
          class="home-feature-column feature-icon col-12 col-md-6 align-items-center"
        >
          <p>insert placeholder image</p>
        </div>
      </div>
    </div>
    <div id="hero-bottom-container">
      <img id="hero-bottom-wave" src="~/assets/images/hero-2.svg" alt="Hero" />
      <div class="container text-center px-5 pb-5 pt-4">
        <h2 class="display-3">What are you waiting for?</h2>
        <p class="h5">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non porta diam. Proin metus
          tortor, gravida pulvinar nunc quis, varius lacinia leo. Praesent in sapien ut ipsum
          lacinia lacinia. Cras non mi vel ipsum convallis rutrum a sed nulla.
        </p>
        <div class="d-inline-block mt-3">
          <NuxtLink to="/dashboard">
            <BaseButton type="secondary" size="lg" class="mt-3 px-5 rounded-pill">
              <span class="h5 font-weight-700 text-primary">Get Started</span>
            </BaseButton>
          </NuxtLink>
        </div>
        <div class="align-items-centers mt-5">
          <p>insert placeholder image</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'home',
}
</script>

<style scoped lang="scss">
.home-feature-column {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

#hero-top-container {
  position: relative;
  top: -76px;
  margin-bottom: -76px;
  width: 100%;
  background: linear-gradient(90deg, #1488cc 0%, #2b32b2 100%);
  z-index: 0;
}

#hero-top-content {
  position: relative;
  top: 65px;
  height: 65vh;
  min-height: 400px;
}

#hero-top-wave {
  width: 100%;
  height: 10vh;
  margin-bottom: -1px;
}

@include media-breakpoint-up(sm) {
  #hero-top-content {
    height: 45vh;
  }

  #hero-top-wave {
    height: 20vh;
  }
}

.hero-top-column {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 80%;
}

@include media-breakpoint-up(sm) {
  .hero-top-column {
    height: 100%;
  }
}

#hero-top-icon-sm {
  height: 40vw;
  max-width: 100%;
}

#hero-top-icon {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 35vw;
  max-height: 55%;
}

#hero-bottom-container {
  width: 100%;
  background: linear-gradient(90deg, #1488cc 0%, #2b32b2 100%);
  z-index: -1;
}

#hero-bottom-wave {
  width: 100%;
  height: 10vh;
  margin-top: -1px;
}

@include media-breakpoint-up(sm) {
  #hero-bottom-wave {
    height: 20vh;
  }
}
</style>
