<template>
<v-container fluid grid-list-xl>
<v-layout row wrap>
    <v-flex xs12>
        <h2>Question Types</h2>
    </v-flex>
</v-layout>
<v-layout row wrap>
    <v-flex xs12>
    <v-btn color="primary" dark @click.native.stop="editItem()">New Item</v-btn>
    <question-type-edit :itemId="editedId" @on-save="onItemSaved"/>
    <v-data-table
        :headers="headers"
        :items="items"
        hide-actions
    >
        <template slot="items" slot-scope="props">
        <tr>
            <td @click="editedId = props.item.id">{{ props.item.name }}</td>
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
    </v-flex>
</v-layout>
</v-container>
</template>
<script>

import _ from 'lodash';
import QuestionTypeEdit from './question-type-edit.vue'

export default {
  name: 'question-type',
  components: {
    QuestionTypeEdit
  },
  data() {
    return {
        headers: [
            {text: 'Name', align: 'left', value: 'name', sortable: false},
            { text: 'Actions', value: 'name', sortable: false }
        ],
        items: [],
        apiUrl: '/workflows/question-type',
        editedId: null
    }
  },
  methods:  {
    editItem(item) {
        var itemId = -1;
        if (!_.isNil(item)) {
            itemId = item.id
        }
        this.editedId = null;
        setTimeout(() => {this.editedId = itemId}, 300);
    },
    deleteItem(item) {
        const index = this.items.indexOf(item)
        if (confirm('Are you sure you want to delete this item?')) {
            this.$http.delete(this.apiUrl +'/rest/' + item.id + '/')
            .then(response => {
                alert('Deleted');
                this.items.splice(index, 1);
            });
        };
    },
    onItemSaved(item) {
        var list_item = this.fetchItem(item);
        if (this.editedId === -1) {
            this.items.push(list_item);
        } else {
            const idx = _.findIndex(this.items, (o) => o.id == item.id);
            Object.assign(this.items[idx], list_item);
        }
    },
    fetchItem(item) {
        return item;
    },
    fetchItems() {
        const params = {};
        this.$http.get(this.apiUrl + '/views/list', {params: params})
        .then(response => {
            this.items = response.data.items;
        });
    }
  },
  computed: {
  },
  created() {
    this.fetchItems();
  }
}
</script>
