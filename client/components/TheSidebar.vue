<template>
  <nav id="sidebar-nav" class="text-center py-5">
    <div id="sidebar-container" class="bg-dark py-5 h-100 overflow-scroll-y scrollbar-none">
      <div class="container px-5 pb-2">
        <img id="sidebar-icon" class="rounded" :src="user.avatar" alt="Icon" />
        <p class="h5 text-wrap font-weight-bold mt-3 mb-2">{{ user.name }}</p>
      </div>
      <div class="text-left">
        <div class="small font-weight-bold text-light text-uppercase px-4 mt-3 mb-2">Main</div>
        <NuxtLink to="/dashboard">
          <div class="sidebar-link font-weight-bold text-white px-4 py-2">All Accounts</div>
        </NuxtLink>
        <div
          class="
            small
            font-weight-bold
            text-light text-uppercase
            px-4
            mt-3
            mb-2
            d-flex
            justify-content-between
          "
        >
          Folders
          <BaseButton
            id="sidebar-folder-plus"
            icon="fas plus"
            class="pl-0 small"
            type=""
            text-color="light"
            :icon-only="true"
            @click="newFolder"
          />
        </div>
        <NuxtLink
          v-for="element in folders"
          :key="element.id"
          :to="`/dashboard/folders/${element.id}`"
        >
          <div class="sidebar-link font-weight-bold text-white px-4 py-2">{{ element.name }}</div>
        </NuxtLink>
        <div class="small font-weight-bold text-light text-uppercase px-4 mt-3 mb-2">Others</div>
        <NuxtLink to="/dashboard/settings">
          <div class="sidebar-link font-weight-bold text-white px-4 py-2">Settings</div>
        </NuxtLink>
        <NuxtLink to="/dashboard/shares">
          <div class="sidebar-link font-weight-bold text-white px-4 py-2">Shares</div>
        </NuxtLink>
      </div>
    </div>
    <BaseModal
      id="sidebar-folder-modal"
      title="New Folder"
      ok-title="Create"
      @cancel="folder = ''"
      @ok="createFolder"
    >
      <BaseInput id="sidebar-folder-name" v-model="folder" label="Name" />
    </BaseModal>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'TheSidebar',
  data() {
    return {
      folder: '',
    }
  },
  computed: {
    ...mapGetters('user', { user: 'get' }),
    ...mapGetters('folders', { folders: 'get' }),
  },
  methods: {
    newFolder() {
      this.$bvModal.show('sidebar-folder-modal')
    },
    async createFolder() {
      if (!this.folder) {
        this.$toast.danger('Name cannot be empty.')
        this.folder = ''
        return
      }

      if (this.folder.length < 2 || this.folder.length > 32) {
        this.$toast.danger('Name must be between 2 and 32 characters.')
        this.folder = ''
        return
      }

      const folder = await this.$axios
        .post('/folders', {
          name: this.folder,
        })
        .catch(this.$error)

      this.folder = ''
      this.$store.commit('folders/add', folder.data)
      this.$toast.success('Created the folder.')
    },
  },
}
</script>

<style scoped lang="scss">
.sidebar-link:hover {
  color: $gray-400;
  background-color: $gray-700;
}

#sidebar-nav {
  top: 75px;
}

@include media-breakpoint-up(md) {
  #sidebar-nav {
    position: sticky;
    height: calc(100vh - 75px);
  }
}

#sidebar-container {
  border-radius: 0.75rem;
}

#sidebar-icon {
  height: 100px;
  width: 100px;
}

#sidebar-folder-plus {
  height: 0;
  border: 0;

  /deep/ .icon {
    height: initial !important;
    top: -3px;
    width: 0;
    position: relative;

    svg {
      font-size: 1rem;
    }
  }
}
</style>
