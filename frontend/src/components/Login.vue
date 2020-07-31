<template>
    <b-container>
        <b-form @submit="onSubmit" class="box">
            <h1>Login</h1>
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
            <router-link to="#">
                <i class="box-link text-muted">Forgot password?</i>
            </router-link>
            <router-link to="/register">
                <i class="box-link text-muted">Register</i>
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
                    login: '',
                    password: '',
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


