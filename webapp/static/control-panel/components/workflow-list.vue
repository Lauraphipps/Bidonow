<template>
  <div class="workflow-list">
    <v-layout row wrap v-if="!selectedItem">
        <v-flex xs12>
            <h2>Workflow list</h2>
                <v-select :items="categories" v-model="filter_workflow_category" label="Filter by category" :loading="workflow_categories_loading">
                    <template slot="selection" slot-scope="data">{{ data.item.name }}</template>
                    <template slot="item" slot-scope="data">
                        <v-list-tile-content v-text="data.item.name"></v-list-tile-content>
                    </template>
                </v-select>
        </v-flex>
    </v-layout>
    <v-layout row wrap v-if="!selectedItem">
        <v-flex xs12>
      <v-dialog v-model="showCloneDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">Clone Workflow</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm12 md12>
                <v-text-field label="Enter new name" v-model="cloneItem.name"></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click.native="showCloneDialog = false">Cancel</v-btn>
          <v-btn color="blue darken-1" flat @click.native="clone">Copy</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
      <v-dialog v-model="dialog" max-width="500px">
      <v-btn color="primary" dark slot="activator" class="mb-2">New Item</v-btn>
      <v-card>
        <v-card-title>
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm12 md12>
                <v-text-field label="Name" v-model="editedItem.name"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-text-field label="Description" v-model="editedItem.description" multi-line></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-select
                    :items="categories"
                    v-model="editedItem.category"
                    label="Category"
                    single-line
                >
                    <template slot="selection" slot-scope="data">{{ data.item.name }}</template>
                    <template slot="item" slot-scope="data">
                        <v-list-tile-content v-text="data.item.name"></v-list-tile-content>
                    </template>
                </v-select>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click.native="close">Cancel</v-btn>
          <v-btn color="blue darken-1" flat @click.native="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
        </v-flex>
    </v-layout>
    <v-layout row wrap v-if="!selectedItem">
        <v-flex xs12>
        <v-data-table
            :headers="headers"
            :items="items"
            hide-actions
        >
            <template slot="items" slot-scope="props">
            <tr>
                <td @click="onRowClick(props.item)">{{ props.item.name }}</td>
                <td class="text-xs-right">{{ props.item.category_name }}</td>
                <td class="justify-center layout px-0">
                    <v-btn icon class="mx-0" @click="openCloneDialog(props.item)">
                        <v-icon color="teal">content_copy</v-icon>
                    </v-btn>
                    <v-btn icon class="mx-0" @click="editItem(props.item)">
                        <v-icon color="teal">edit</v-icon>
                    </v-btn>
                    <v-btn icon class="mx-0" @click="deleteItem(props.item)">
                        <v-icon color="pink">delete</v-icon>
                    </v-btn>
                </td>
            </tr>
            </template>
        </v-data-table>
        </v-flex>
    </v-layout>
    <v-layout row wrap v-if="selectedItem">
        <v-flex xs12 sm12 md12>
            <h2>Workflow {{ selectedItem.name }} ({{ selectedItem.id }})</h2>
            <workflow-item-view :bundleId="selectedItem.id" @back="showList"/>
        </v-flex>
    </v-layout>
  </div>
</template>
<script>
import _ from 'lodash';
import WorkflowItemView from './workflow-item-view.vue'

export default {
  name: 'workflow-list',
  components: {
    WorkflowItemView
  },
  data() {
    return {
        categories: [],
        items: [],
        headers: [
            {
                text: 'Name',
                align: 'left',
                value: 'name',
                sortable: false
            },
            { text: 'Category', value: 'category_name', sortable: false },
            { text: 'Actions', value: 'name', sortable: false }
        ],
        dialog: false,
        editedIndex: -1,
        editedItem: {},
        selectedItem: null,
        workflow_categories_loading: true,
        filter_workflow_category: null,
        showCloneDialog: false,
        cloneItem: {}
    }
  },
  watch: {
    filter_workflow_category() {
        this.fetchWorkflowItems();
    }
  },
  methods: {
    showList() {
        this.selectedItem = null;
    },
    openCloneDialog(item) {
        this.cloneItem = _.cloneDeep(item);
        this.showCloneDialog = true;
    },
    clone() {
        const item = this.cloneItem;
        const data = {
            id: item.id,
            name: item.name
        }
        this.$http.post('/workflow/clone', data)
        .then(response => {
            this.items.push(response.data);
            this.showCloneDialog = false;
        })
    },
    fetchWorkflowItems() {
        var params  = {};
        console.log(this.filter_workflow_category);
        if (this.filter_workflow_category !== null) {
            params.category_id = this.filter_workflow_category.id;
        }
        console.log('Fetch data', params);
        this.$http.get('/workflow/', {params: params})
        .then(response => {
            this.items = response.data.workflow_items;
        });
    },
    onRowClick(item) {
        this.selectedItem = item;
    },

    editItem (item) {
        this.editedIndex = this.items.indexOf(item);
        this.editedItem = Object.assign({}, item);
        var category = _.find(this.categories, o => o.id === this.editedItem.category_id);
        this.editedItem.category = category;
        console.log(this.editedItem);
        this.dialog = true;
    },

    deleteItem (item) {
        const index = this.items.indexOf(item)
        if (confirm('Are you sure you want to delete this item?')) {
            this.$http.post('/workflow/delete', {id: item.id})
            .then(response => {
                alert('Deleted');
                this.items.splice(index, 1);
            });
        } 
      },

    close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },

    save () {
        if (this.editedItem.category) {
            this.editedItem.category_id = this.editedItem.category.id;
            this.editedItem.category_name = this.editedItem.category.name;
        }
        this.$http.post('/workflow/save', this.editedItem).
        then(response => {
            alert('Saved');
            console.log(response.data);
            if (this.editedIndex > -1) {
                Object.assign(this.items[this.editedIndex], this.editedItem)
            } else {
                this.editedItem.id = response.data.id;
                this.items.push(this.editedItem)
            }
            this.close()
        });
      }
  },
  computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      }
  },
  created() {
    this.$http.get('/workflowcategory/')
    .then(response => {
        var items = response.data.workflowcategories;
        var all_item = {id: null, name: 'All'};
        this.categories = [all_item].concat(items);
        this.filter_workflow_category = all_item;
        this.workflow_categories_loading = false;
    });
  }
}
</script>
