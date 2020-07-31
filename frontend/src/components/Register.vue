<template>
  <b-container>
      <b-form @submit="onSubmit" class="box">
        <h1>Login</h1>
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

<style>
  body {
    margin: 0;
    padding: 0;
    font-family: sans-serif;
    background: linear-gradient(to right, #b92b27, #1565c0)
  }

  .box {
    text-align: center;
    margin: auto;
  }

  .box input[type="text"],
  .box input[type="email"],
  .box input[type="password"] {
    background: none;
    display: block;
    margin: 20px auto;
    text-align: center;
    border: 2px solid #3498db;
    padding: 10px 10px;
    width: 250px;
    outline: none;
    color: white;
    border-radius: 24px;
    transition: 0.25s
  }

  .box h1 {
    color: white;
    text-transform: uppercase;
    font-weight: 500
  }

  .box input[type="text"]:focus,
  .box input[type="email"]:focus,
  .box input[type="password"]:focus {
    width: 300px;
    border-color: #2ecc71
  }

  .box input[type="submit"] {
    background: none;
    display: block;
    margin: 20px auto;
    text-align: center;
    border: 2px solid #2ecc71;
    padding: 14px 40px;
    outline: none;
    color: white;
    border-radius: 24px;
    transition: 0.25s;
    cursor: pointer
  }

  .box input[type="submit"]:hover {
    background: #2ecc71
  }
</style>