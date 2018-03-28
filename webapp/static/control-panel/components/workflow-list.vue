<template>
  <div class="workflow-list">
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
  </div>
</template>
<script>
import _ from 'lodash';

export default {
  name: 'workflow-list',
  props: {
    items: Array,
    categories: Array
  },
  data() {
    return {
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
    }
  },
  methods: {
    onRowClick(item) {
        this.$emit('select-item', item);
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
        console.log('try to save', this.editedItem);
        if (this.editedItem.category) {
            this.editedItem.category_id = this.editedItem.category.id;
            this.editedItem.category_name = this.editedItem.category.name;
        }
        this.$http.post('/workflow/save', this.editedItem).
        then(response => {
            console.log(response);
            alert('Saved');
            if (this.editedIndex > -1) {
            Object.assign(this.items[this.editedIndex], this.editedItem)
            } else {
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
  }
}
</script>
