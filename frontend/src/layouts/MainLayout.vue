<template>
  <div>
    <div class="app-main-layout">

      <Navbar/>

      <main class="app-content">
        <div class="app-page">
          <router-view/>
        </div>
      </main>

    </div>
  </div>
</template>

<script>
import Navbar from '@/components/app/Navbar'

export default {
  name: 'main-layout',
  data: () => ({
    isOpen: true
  }),
  components: {
    Navbar
  }
}
</script>

<style scoped>
.app-page {
  margin: 10px;
}
</style>
