<template>
</template>

<script>
import modal from '../components/modal.vue';

export default {
  name: 'app',
  data: {
    message: 'Hello Vue.js!',
    showModal: false
  },
  components: {
    modal: modal
  },
  render() {
  },
  methods: {
      reverseMessage: function () {
          this.message = this.message.split('').reverse().join('');
      },
      openSignUp: function () {
          alert('Open signup');
      }
  },
  components: {
  },
  mounted() {
  }
}
</script>

<style>
</style>
