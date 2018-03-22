import Vue from 'vue';
import PictureInput from 'vue-picture-input'
import axios from 'axios';
import Datepicker from 'vuejs-datepicker';
import VueTimepicker from 'vue2-timepicker'
import VeeValidate from 'vee-validate';

Vue.use(VeeValidate);


var uploadFile =  function (file) {
  const url = '/upload-file/';
  const name = 'file1'
  const formData = new FormData();
  formData.append(name, file);
  const config = {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  };
  return axios.post(url, formData, config);
};



var app = new Vue({
    el: '#app',
    data: {
        workflow: null,
        cq: null,
        cq_idx: null

    },
    components: {
        PictureInput,
        Datepicker,
        VueTimepicker
    },
    created: function () {
        axios.get('/api/workflows/' + WORKFLOW_ID).then((response) => {
            this.workflow = response.data.workflow;
            this.cq_idx = 0;
            this.cq = this.workflow.questions[this.cq_idx];
        });
    },
    methods: {
        showMoreData(answer) {
            // if type for answer is not defined
            if (!answer.type) return false;

            // if question is multi
            if (answer.selected) return true;

            // if question is one
            if (this.cq.selected == answer.id) return true;

            return false;
        },
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
        onChanged(image) {
            if (image) {
                this.image = this.$refs.pictureInput[0].file;
                // this.image = image;
            } else {
                console.log("Old browser. No support for Filereader API");
            }
        },
        attemptUpload: function (image) {
            uploadFile(this.image);
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


