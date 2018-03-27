<template>
  <div class="workflow-view">
  <div v-if="!selectedItem">
  <h2>Workflow list</h2>
    <v-container fluid>
        <v-layout row wrap>
            <v-flex xs6>
                <v-select :items="workflow_categories" v-model="filter_workflow_category" label="Filter by category" :loading="workflow_categories_loading">
                    <template slot="selection" slot-scope="data">{{ data.item.name }}</template>
                    <template slot="item" slot-scope="data">
                        <v-list-tile-content v-text="data.item.name"></v-list-tile-content>
                    </template>
                </v-select>
            </v-flex>
        </v-layout>
        <v-layout row wrap>
            <v-flex xs6>
                <workflow-list :items="workflow_items" @select-item="selectItem"/>
            </v-flex>
        </v-layout>
    </v-container>
  </div> <!-- !selectedItem -->
  <div v-if="selectedItem">
  <h2> Workflow Detaild {{ selectedItem.id }} </h2>
  <workflow-item-view :id="selectedItem.id"/>
  </div> <!-- selectedItem -->
  </div>
</template>

<script>
import WorkflowList from './workflow-list.vue'
import WorkflowItemView from './workflow-item-view.vue'

export default {
  name: 'workflow-view',
  components: {
    WorkflowList,
    WorkflowItemView
  },
  data() {
    return {
        workflow_categories: [],
        workflow_categories_loading: true,
        filter_workflow_category: null,
        workflow_items: [],
        selectedItem: null,
    }
  },
  methods: {
    fetchWorkflowItems() {
        this.$http.get('/workflow/')
        .then(response => {
            this.workflow_items = response.data.workflow_items;
        });
    },
    selectItem(item) {
        this.selectedItem = item;
    }
  },
  watch: {
    filter_workflow_category() {
        this.fetchWorkflowItems();
    }
  },
  created() {
    this.$http.get('/workflowcategory/')
    .then(response => {
        var items = response.data.workflowcategories;
        var all_item = {id: null, name: 'All'};
        this.workflow_categories = [all_item].concat(items);
        this.filter_workflow_category = all_item;
        this.workflow_categories_loading = false;
    });
  }
}
</script>

<style>
</style>
