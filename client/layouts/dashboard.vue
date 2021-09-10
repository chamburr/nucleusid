<template>
  <div>
    <TheHeader :dashboard="true" />
    <div
      id="dashboard-container"
      class="d-md-flex flex-nowrap justify-content-center container-fluid px-4 px-md-0"
    >
      <div id="dashboard-sidebar" class="d-inline-block px-2 px-md-5">
        <TheSidebar />
      </div>
      <div id="dashboard-content" class="d-md-block py-5 pr-0 pr-md-5 w-100">
        <div class="d-flex flex-column h-100">
          <Nuxt />
        </div>
      </div>
    </div>
    <TheFooter />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  middleware: ['user'],
  head: {
    title: 'Dashboard',
  },
  computed: {
    ...mapGetters('user', ['get']),
  },
}
</script>

<style scoped lang="scss">
#dashboard-back {
  font-size: 0.9em;
}

#dashboard-content {
  min-width: 0;
  flex-shrink: 2;
}

#dashboard-container {
  max-width: map-get($container-max-widths, 'sm');
}

@include media-breakpoint-up(md) {
  #dashboard-container {
    max-width: map-get($container-max-widths, 'xl') + 100px;
  }
}

@include media-breakpoint-down(sm) {
  #dashboard-sidebar {
    width: 100%;
  }
}

@include media-breakpoint-up(md) {
  #dashboard-sidebar {
    min-width: 300px;
    max-width: 40%;
  }
}

@include media-breakpoint-up(lg) {
  #dashboard-sidebar {
    min-width: 30%;
  }
}
</style>
