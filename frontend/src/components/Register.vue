<template>
  <b-container>
    <b-form @submit="onSubmit" class="box">
      <h1>Register</h1>
      <b-form-input
          id="email"
          v-model="form.email"
          type="email"
          required
          placeholder="Email"
      ></b-form-input>
      <!--          :state="validation"-->

      <b-form-input
          id="login"
          v-model="form.login"
          required
          placeholder="Login"
      ></b-form-input>

      <b-form-input
          id="password"
          v-model="form.password"
          required
          placeholder="Password"
      ></b-form-input>

      <b-form-input
          id="confirm-password"
          v-model="form.confirm_password"
          required
          placeholder="Confirm password"
      ></b-form-input>
      <router-link to="/login">
        <i class="box-link text-muted">Login</i>
      </router-link>
      <input type="submit" value="Submit">
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
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      alert(JSON.stringify(this.form))
    }
  },
  computed: {}
}
</script>