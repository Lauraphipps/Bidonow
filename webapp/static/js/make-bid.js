import Vue from 'vue';
import VueResource from 'vue-resource'
Vue.use(VueResource);


Vue.component('answer', {
    props: ['answer', 'question'],
    render: function (createElement) {
        var childs = [];
        var answer_id = 'id_answer_' + this.answer.id
        var question_control_type = 'radio';
        if (this.question.type == 'multi') {
            question_control_type = 'checkbox'
        }
        childs.push(
            createElement(
                'input',
                {
                    attrs: {
                        type: question_control_type,
                        value: this.answer.id,
                        name: 'test',
                        id: answer_id
                    }
                },
                []
            )
        );
        childs.push(
            createElement(
                'label',
                {
                    attrs: {
                        'for': answer_id
                    }
                },
                [this.answer.text]
            )
        );
        if (this.answer.type == 'text') {
            var answer_data_id = 'answer_data_' + this.answer.id
            childs.push(
                createElement(
                    'input',
                    {
                        attrs: {
                            type: 'text',
                            name: answer_data_id,
                            id: answer_data_id,
                            placeholder: 'Enter: ' + this.answer.text
                        }
                    }
                )
            )
            childs.push(
                createElement(
                    'label',
                    {
                        attrs: {
                            'for': answer_data_id,
                        }
                    }
                )
            )
        }
        if (this.answer.type == 'date') {
            childs.push(createElement('div','Show date picker'))
        }
        if (this.answer.type == 'time') {
            childs.push(createElement('div','Show time picker'))
        }
        if (this.answer.type == 'image') {
            childs.push(createElement('div','Show image uploader'))
        }
        return createElement(
            'li', 
            {},
            childs
        )
  }
});



var app = new Vue({
    el: '#app',
    data: {
        workflow: null,
        cq: null,
        cq_idx: null

    },
    created: function () {
        this.$http.get('/api/workflows/1').then((response) => {
            this.workflow = response.data.workflow;
            this.cq_idx = 0;
            this.cq = this.workflow.questions[this.cq_idx];
        });
    },
    methods: {
        goNext(event) {
            event.preventDefault();
            this.cq_idx += 1;
            this.cq = this.workflow.questions[this.cq_idx];
        },
        goBack(event) {
            event.preventDefault();
            this.cq_idx -= 1;
            this.cq = this.workflow.questions[this.cq_idx];
        },
        reverseMessage: function () {
        }

    },
    computed: {
        // a computed getter
        hasPrev: function () {
            return this.cq_idx > 0;
        },
        hasNext: function () {
            return this.cq_idx < (this.workflow.questions.length - 1);
        }
    }
});


