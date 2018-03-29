<template>
  <div class="workflow-view">
    <v-container fluid grid-list-xl>
        <v-layout row wrap>
            <v-flex xs3>
    <v-navigation-drawer permanent>
    <v-toolbar flat>
      <v-list>
        <v-list-tile>
          <v-list-tile-title class="title">
            Bidonow Admin
          </v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-toolbar>
    <v-divider></v-divider>
    <v-list dense class="pt-0">
      <v-list-tile v-for="tab in tabs" @click="currentTab = tab" :class="['tab-button', { active: currentTab === tab }]">
        <v-list-tile-content>
          <v-list-tile-title>{{ tab.name }}</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
            </v-flex>
            <v-flex xs9>
            <component v-bind:is="currentTab.component" class="tab" ></component>
            </v-flex>
        </v-layout>
    </v-container>
  </div>
</template>

<script>
import WorkflowList from './workflow-list.vue'
import QuestionTypeList from './question-type-list.vue'
import WorkflowCategoryList from './workflow-category-list.vue'


export default {
  name: 'workflow-view',
  components: {
    WorkflowList, QuestionTypeList
  },
  data() {
    return {
        tabs: [
            {'name': 'Workflows', component: WorkflowList},
            {'name': 'Question Types', component: QuestionTypeList},
            {'name': 'Categories', component: WorkflowCategoryList}
        ],
        currentTab: null,
    }
  },
  methods: {
  },
  watch: {
  },
  created() {
    this.currentTab = this.tabs[0];
  }
}
</script>

<style>
</style>
