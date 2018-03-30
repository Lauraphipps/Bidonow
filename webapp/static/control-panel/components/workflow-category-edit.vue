<template>
<v-dialog v-model="showDialog" max-width="500px">
    <v-card>
    <v-card-title>
        <span class="headline">{{ formTitle }}</span>
    </v-card-title>
    <v-card-text>
        <v-container grid-list-md>
        <v-layout wrap>
            <v-flex xs12 sm12 md12>
            <v-text-field label="Name" v-model="item.name"></v-text-field>
            </v-flex>
            <v-flex xs12 sm12 md12>
            <v-text-field label="Description" v-model="item.description" multi-line></v-text-field>
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
</template>
<script>

import _ from 'lodash';


export default {
  name: 'edit-item',
  components: {
  },
  props: {
    itemId: Number
  },
  data() {
    return {
        apiUrl: '/workflows/workflow-category/rest/',
        default: {},
        item: {},
        showDialog: false
    }
  },
  watch: {
    itemId() {
        if (this.itemId === null) {
            this.showDialog = false;
        } else {
            this.showDialog = true;
            this.fetchItem();
        }
    }
  },
  methods: {
    isNew() {
        return (this.itemId === null || this.itemId === -1)
    },
    fetchItem() {
        if (this.isNew()) {
            this.item = this.default;
        } else {
            this.$http.get(this.apiUrl + this.itemId + '/')
            .then(response => {
                this.item = response.data;
            });
        }
    },
    close () {
        this.showDialog = false;
    },
    save () {
        this.$http.post(this.apiUrl, this.item).
        then(response => {
            alert('Saved');
            this.item = response.data;
            this.close()
            this.$emit('on-save', this.item);
        });
      }
  },
  computed: {
      formTitle () {
        return this.isNew() ? 'New Item' : 'Edit Item'
      }
  },
  created() {
  }
}
</script>
