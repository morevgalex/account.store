<template>
  <b-container>
    <b-form @submit.prevent="onSubmit" class="box">
      <h1>{{ $t('login') }}</h1>
      <b-form-input
          id="login"
          v-model="form.login"
          required
          :placeholder="$t('form-login')"
      ></b-form-input>

      <b-form-input
          id="password"
          v-model="form.password"
          required
          placeholder="Password"
      ></b-form-input>
      <router-link to="#" @click="onSubmit">
        <i class="box-link text-muted">{{ $t('form-forgot-password') }}</i>
      </router-link>
      <router-link to="/register">
        <i class="box-link text-muted">{{ $t('form-register-button') }}</i>
      </router-link>
      <input type="submit" :value="$t('form-submit-button')">
    </b-form>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        login: '',
        password: '',
      }
    }
  },
  metaInfo: {
    title: 'Login'
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      alert(JSON.stringify(this.form))
    }
  },
  computed: {}
}
</script>


