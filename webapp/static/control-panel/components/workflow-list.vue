<template>
  <div class="workflow-list">
                  <v-data-table
                        :headers="headers"
                        :items="items"
                        hide-actions
                    >
                        <template slot="items" slot-scope="props">
                        <tr @click="onRowClick(props.item)">
                            <td>{{ props.item.name }}</td>
                            <td class="text-xs-right">{{ props.item.category_name }}</td>
                        </tr>
                        </template>
                    </v-data-table>
  </div>
</template>
<script>
export default {
  name: 'workflow-list',
  props: {
    items: Array
  },
  data() {
    return {
        headers: []
    }
  },
  methods: {
    onRowClick(item) {
        this.$emit('select-item', item);
    }
  }
}
</script>
