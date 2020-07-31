<template>
    <b-navbar toggleable="sm" type="dark" variant="info">
        <b-navbar-brand href="#">Best store</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
                <b-nav-item to="/home">Home</b-nav-item>
                <b-nav-item to="/page">Page</b-nav-item>

                <b-nav-item to="#" disabled>Test</b-nav-item>
            </b-navbar-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">

                <template v-if="username">
                    <b-nav-item href="#">{{username}}</b-nav-item>
                    <b-nav-item href="#" @click="logout">Logout</b-nav-item>
                </template>

                <template v-else>
                    <b-nav-item href="/login">Signin</b-nav-item>
                    <b-nav-item href="/register">Signup</b-nav-item>
                </template>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>


<script>
    export default {
        name: "Navbar",
        data: () => ({
            username: undefined
        }),
        methods: {
            logout() {
                console.log('logout')
            }
        }
    }
</script>
