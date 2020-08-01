<template>
  <b-container>
    <b-form @submit="onSubmit" class="box">
      <h1>{{ $t('register') }}</h1>
      <b-form-input
          id="email"
          v-model="form.email"
          type="email"
          required
          :placeholder="$t('form-email')"
      ></b-form-input>
      <!--          :state="validation"-->

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
          :placeholder="$t('form-password')"
      ></b-form-input>

      <b-form-input
          id="confirm-password"
          v-model="form.confirm_password"
          required
          :placeholder="$t('form-confirm-password')"
      ></b-form-input>
      <router-link to="/login">
        <i class="box-link text-muted">{{ $t('form-login-button') }}</i>
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
        email: '',
        login: '',
        password: '',
        confirm_password: ''
      }
    }
  },
  metaInfo: {
    title: 'Register'
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