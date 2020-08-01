<template>
  <b-navbar toggleable="sm" type="dark" variant="info">
    <b-navbar-brand href="#">Best store</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item to="/home">{{ $t('home') }}</b-nav-item>
        <b-nav-item to="/page">Page</b-nav-item>

        <b-nav-item to="#" disabled>Test</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">


        <template v-if="username">
          <b-nav-item href="#">{{ username }}</b-nav-item>
          <b-nav-item href="#" @click="logout">Logout</b-nav-item>
        </template>
        <template v-else>
          <b-nav-item to="/login">{{ $t('signIn') }}</b-nav-item>
          <b-nav-item to="/register">{{ $t('signUp') }}</b-nav-item>
        </template>

        <b-nav-item-dropdown
            id="my-nav-dropdown"
            :text="lang"
            toggle-class="nav-link-custom"
            right
        >
          <b-dropdown-item
              @click="changeLocale(lang)"
              v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang">{{ lang }}
          </b-dropdown-item>
        </b-nav-item-dropdown>

      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>


<script>
export default {
  name: "Navbar",
  data: () => ({
    username: undefined,
    langs: ['en', 'ru'],
    lang: 'en'
  }),
  methods: {
    logout() {
      console.log('logout')
    },
    changeLocale(locale) {
      this.$i18n.locale = locale
      this.$data.lang = locale
    }
  }
}
</script>
