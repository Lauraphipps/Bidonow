<template>
  <div class="workflow-item-view">
  <v-btn color="primary" dark class="mb-2" @click="$emit('back')">Back</v-btn>
  <v-container fluid>
        <v-layout row wrap>
            <v-flex xs12>
    <h3>Workflow {{ item.name }} ({{ item.id }})</h3>
    <div v-if="item">
          <v-data-table
            :headers="headers"
            :items="item.questions"
            hide-actions
            item-key="id"
        >
            <template slot="items" slot-scope="props">
            <tr>
                <td >
                    <v-icon v-if="!props.expanded" @click="props.expanded = !props.expanded">keyboard_arrow_right</v-icon>
                    <v-icon v-else @click="props.expanded = !props.expanded">keyboard_arrow_down</v-icon>
                </td>
                <td>{{ props.item.question_type }}</td>
                <td>{{ props.item.text }}</td>
                <td>
                    <v-icon v-if="props.item.optional">check_box</v-icon>
                    <v-icon v-else>check_box_outline_blank</v-icon>
                </td>
                <td>{{ props.item.more_info }}</td>
                <td class="justify-center layout px-0">
                    <v-btn icon class="mx-0" @click="editQuestion(props.item)">
                        <v-icon color="teal">edit</v-icon>
                    </v-btn>
                    <v-btn icon class="mx-0" @click="deleteQuestion(props.item)">
                        <v-icon color="pink">delete</v-icon>
                    </v-btn>
                </td>
            </tr>
            </template>
            <template slot="expand" slot-scope="props">
                <v-flex xs10 offset-xs1>
                <v-data-table
                    :headers="answer_headers"
                    :items="props.item.answers"
                    hide-actions
                    item-key="id"
                    class="question-answers-table"
                >
                    <template slot="items" slot-scope="props1">
                        <tr>
                            <td><div v-if="props1.item.answer_type">{{ props1.item.answer_type }}</div><div v-else>None</div></td>
                            <td>{{ props1.item.text }}</td>
                            <td>{{ props1.item.next_question_text }}</td>
                            <td class="justify-center layout px-0">
                                <v-btn icon class="mx-0" @click="editAnswer(props1.item)">
                                    <v-icon color="teal">edit</v-icon>
                                </v-btn>
                                <v-btn icon class="mx-0" @click="deleteAnswer(props1.item)">
                                    <v-icon color="pink">delete</v-icon>
                                </v-btn>
                            </td>
                        </tr>
                    </template>
                </v-data-table>
                <v-btn class="mx-0" @click="addAnswer(props.item)">
                    Add Answer
                </v-btn>
                </v-flex>
            </template>
        </v-data-table>
        <question-edit :itemId="editedItemId" :default="{'bundle_id': item.id}" @on-save="onQuestionSaved"/>
        <answer-edit :itemId="editedAnswerId" :default="defaultAnswer" @on-save="onAnswerSaved"/>
    </div> <!-- item -->
    <div v-else>
        Load data
        <v-progress-linear :indeterminate="true"></v-progress-linear>
    </div>
    </v-flex>
    </v-layout>
    </v-container>
  </div>
</template>

<script>
import QuestionEdit from './question-edit.vue';
import AnswerEdit from './answer-edit.vue';
import _ from 'lodash';

export default {
  name: 'workflow-item-view',
  props: {
    id: Number
  },
  components: {
    QuestionEdit, AnswerEdit
  },
  methods: {
    fetchWorkFlow() {
        this.$http.get('workflow/' + this.id +'/')
        .then(response => {
            this.item = response.data.workflow
        });
    },
    onQuestionSaved(updated_item) {
        if (this.editedItemId !== null) {
            var idx = _.findIndex(this.item.questions, (o) => o.id == this.editedItemId);
            var old_item = this.item.questions[idx];
            var new_item = _.extend(old_item, updated_item);
            new_item.question_type = updated_item.question_type.name;
            Object.assign(this.item.questions[idx], new_item);
        } else {
            updated_item.question_type = updated_item.question_type.name;
            updated_item.question_type_id = updated_item.question_type.id;
            this.item.questions.push(updated_item)
        }
    },
    editQuestion(item) {
        this.editedItemId = item.id;
    },
    deleteQuestion(item) {
        const index = this.item.questions.indexOf(item)
        if (confirm('Are you sure you want to delete this item?')) {
            this.$http.post('/question/delete', {id: item.id})
            .then(response => {
                alert('Deleted');
                this.item.questions.splice(index, 1);
            });
        };
    },
    editAnswer(item) {
        this.defaultAnswer = {question_id: item.question_id}
        this.editedAnswerId = item.id;
    },
    deleteAnswer(item) {
        const questionIdx = _.findIndex(this.item.questions, (o) => o.id == item.question_id);
        const answers = this.item.questions[questionIdx].answers;
        const idx = answers.indexOf(item)
        if (confirm('Are you sure you want to delete this item?')) {
            this.$http.post('/answer/delete', {id: item.id})
            .then(response => {
                alert('Deleted');
                answers.splice(idx, 1);
            });
        };
    },
    addAnswer(question) {
        this.defaultAnswer = {question_id: question.id};
        this.editedAnswerId = -1;
    },
    onAnswerSaved(item) {
        const questionIdx = _.findIndex(this.item.questions, (o) => o.id == item.question_id);
        const answers = this.item.questions[questionIdx].answers;
        if (this.editedAnswerId !== null && this.editedAnswerId !== -1) {
            const idx = _.findIndex(answers, (o) => o.id == item.id);
            var old_item = answers[idx];
            var new_item = _.extend(old_item, item);
            if (!_.isNil(item.answer_type)) {
                new_item.answer_type = item.answer_type.name;
                new_item.answer_type_id = item.answer_type.id;
            } else {
                new_item.answer_type = 'None';
                new_item.answer_type_id = -1;
            }
            Object.assign(answers[idx], new_item);
        } else {
            if (!_.isNil(item.answer_type)) {
                item.answer_type = item.answer_type.name;
                item.answer_type_id = item.answer_type.id;
            } else {
                item.answer_type = 'None';
                item.answer_type_id = -1;
            }
            answers.push(item)
        }
    }
  },
  watch: {
    id() {
        this.fetchWorkFlow();
    }
  },
  created() {
    this.fetchWorkFlow();
  },
  data() {
    return {
        item: {},
        editedItemId: null,
        editedAnswerId: null,
        defaultAnswer: {},
        headers: [
            { text: '', sortable: false},
            {
                text: 'Type',
                value: 'question_type',
                sortable: false
            },
            { text: 'Text', value: 'text', sortable: false },
            { text: 'Optional', value: 'optional', sortable: false },
            { text: 'More Info', value: 'more_info', sortable: false },
            { text: 'Actions', value: 'name', sortable: false }
        ],
        answer_headers: [
            { text: 'Type', sortable: false},
            {text: 'Text', value: 'text', sortable: false},
            { text: 'next_question_text', value: 'text', sortable: false },
            { text: 'Actions', value: 'name', sortable: false }
        ]
    }
  }
}
</script>
