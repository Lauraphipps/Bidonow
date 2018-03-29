<template>
    <div class="question-edit">
      <v-dialog v-model="showDialog" max-width="500px">
      <v-btn color="primary" dark slot="activator" class="mb-2" @click="newItem">New Question</v-btn>
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
                <v-select label="Type" v-model="item.question_type" :items="questionTypes" required>
                    <template slot="selection" slot-scope="data">{{ data.item.name }}</template>
                    <template slot="item" slot-scope="data">
                        <v-list-tile-content v-text="data.item.name"></v-list-tile-content>
                    </template>
                </v-select>
              </v-flex>
              <v-flex xs12 sm12 md12>
                <v-text-field label="More Info" v-model="item.more_info" multi-line></v-text-field>
              </v-flex>
            </v-layout>
              <v-flex xs12 sm12 md12>
                <v-checkbox
                    label="Optional"
                    v-model="item.optional"
                ></v-checkbox>
              </v-flex>
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
        if (this.itemId === null || this.itemId == -1) return;
        this.$http.get('question/' + this.itemId +'/')
        .then(response => {
            this.item = response.data
            this.attachQuestionType(this.item);
        });
    },
    attachQuestionType(item) {
        var question_type = _.find(this.questionTypes, (o) => o.id === item.question_type_id);
        item.question_type = question_type;
    },
    close () {
        this.showDialog = false
        setTimeout(() => {
          // this.editedItem = Object.assign({}, this.defaultItem)
          // this.editedIndex = -1
        }, 300)
    },
    save() {
        if (!_.isNil(this.item.question_type)) {
            this.item.question_type_id = this.item.question_type.id;
        }
        this.$http.post('/question/save', this.item)
        .then(response => {
            alert('Saved!');
            this.showDialog = false;
            var new_item = response.data;
            this.attachQuestionType(new_item);
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
        this.fetchItem();
    }
  },
  created() {
    this.fetchItem();
    this.$http.get('/question-types/')
    .then(response => {
        this.questionTypes = response.data.question_types;
    });
  },
  data() {
    return {
        item: {},
        showDialog: false,
        formTitle: 'TEST',
        questionTypes: []
    }
  }
}
</script>
