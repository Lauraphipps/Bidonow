<template>
  <div id="app">
    <v-app>
        <workflow-view/>
    </v-app>
  </div>
</template>

<script>
import WorkflowView from './components/workflow-view.vue';

export default {
  name: 'app',
  components: {
    WorkflowView
  },
  mounted() {
  }
}
</script>

<style>
</style>
