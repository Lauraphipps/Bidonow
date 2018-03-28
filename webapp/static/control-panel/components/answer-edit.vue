<template>
    <div class="answer-edit">
      <v-dialog v-model="showDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm12 md12>
                <v-text-field label="Text" v-model="item.text"></v-text-field>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-select label="Type" v-model="item.answer_type" :items="answerTypes">
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
    </div>
</template>
<script>

import _ from 'lodash';

export default {
  name: 'question-edit',
  props: {
    itemId: Number,
    default: {}
  },
  methods: {
    fetchItem() {
        if (this.itemId === null || this.itemId === -1) return;
        this.$http.get('answer/' + this.itemId +'/')
        .then(response => {
            this.item = response.data
            this.attachAnswerType(this.item);
        });
    },
    attachAnswerType(item) {
        var answer_type = _.find(this.answerTypes, (o) => o.id === item.answer_type_id);
        item.answer_type = answer_type;
    },
    close () {
        this.showDialog = false
        setTimeout(() => {
          // this.editedItem = Object.assign({}, this.defaultItem)
          // this.editedIndex = -1
        }, 300)
    },
    save() {
        if (!_.isNil(this.item.answer_type)) {
            this.item.answer_type_id = this.item.answer_type.id;
        }
        this.$http.post('/answer/save', this.item)
        .then(response => {
            alert('Saved!');
            this.showDialog = false;
            var new_item = response.data;
            this.attachAnswerType(new_item);
            this.$emit('on-save', new_item);
        });
    },
    newItem() {
        alert('New Item');
        this.item = _.cloneDeep(this.default);
    }
  },
  watch: {
    itemId() {
        this.showDialog = true;
        if (this.itemId === -1) {
            this.item = _.cloneDeep(this.default);
        }
        this.fetchItem();
    }
  },
  created() {
    this.fetchItem();
    this.$http.get('/answer-types/')
    .then(response => {
        this.answerTypes = response.data.items;
    });
  },
  data() {
    return {
        item: {},
        showDialog: false,
        formTitle: 'TEST',
        answerTypes: []
    }
  }
}
</script>
