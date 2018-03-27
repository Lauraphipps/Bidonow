<template>
  <div class="workflow-item-view">
    <h3>This is workflow item view</h3>
    <div v-if="item">
        <div>Id: {{ item.id }}</div>
        <div>Name: {{ item.name }}</div>

          <v-data-table
            :headers="headers"
            :items="item.questions"
            hide-actions
            item-key="id"
        >
            <template slot="items" slot-scope="props">
            <tr @click="props.expanded = !props.expanded">
                <td>{{ props.item.text }}</td>
            </tr>
            </template>
            <template slot="expand" slot-scope="props">
                <ul v-if="props.item.answers">
                    <li v-for="a in props.item.answers">{{ a.text }}</li>
                </ul>
            </template>
        </v-data-table>
    </div> <!-- item -->
    <div v-else>
        Load data
        <v-progress-linear :indeterminate="true"></v-progress-linear>
    </div>
  </div>
</template>

<script>
export default {
  name: 'workflow-item-view',
  props: {
    id: Number
  },
  methods: {
    fetchWorkFlow() {
        this.$http.get('workflow/' + this.id +'/')
        .then(response => {
            console.log(response.data);
            this.item = response.data.workflow
        });
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
        item: null,
        headers: []
    }
  }
}
</script>
