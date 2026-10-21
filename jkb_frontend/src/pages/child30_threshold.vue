<template>
  <div>
    <router-link :to="`/`">&lt; Back </router-link>
    <div class="row q-mt-md">
      <div class="col-3"></div>
      <div class="col">
        <q-table
          class="my-table"
          :rows="list_all_jkb_monitoring_items"
          :columns="columns_for_jkb_alerts"
          row-key="name"
          :filter="filter"
          v-model:pagination="pagination"
          auto-width
        >
          <template v-slot:top-right>
            <q-input
              borderless
              dense
              debounce="300"
              v-model="filter"
              placeholder="Search"
              class="bg-amber-5"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          <!-- task_name -->
          <template v-slot:body-cell-task_name="props">
            <q-td key="task_name" :props="props">
              <a target="_blank" :href="props.row.link_for_edit_threshold">{{
                props.row.task_name
              }}</a>
            </q-td>
          </template>
        </q-table>
      </div>
      <div class="col-3"></div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from "vue";
import axios from "axios";
import { useQuasar } from "quasar";
import { Notify } from "quasar";
import { useCounterStore } from "src/stores/example-store";
const example_store = useCounterStore();
const filter = ref("");
const $q = useQuasar();

const columns_for_jkb_alerts = [
  {
    name: "task_id",
    required: true,
    label: "Task_ID",
    align: "center",
    field: (row) => row.task_id,
    sortable: true,
  },
  {
    name: "task_name",
    required: true,
    label: "Task Name",
    align: "center",
    field: (row) => row.task_name,
    sortable: true,
  },

  {
    name: "alert_threshold",
    required: true,
    label: "Alert_threshold",
    align: "center",
    field: (row) => row.alert_threshold,
    sortable: true,
  },
];

//

const url_for_getting_jkb_monitoring_items = ref(
  "/api/axios_threshold"
);
const list_all_jkb_monitoring_items = ref([]);
const pagination = ref({ rowsPerPage: 1000, sortBy: "desc" });
const a10_get_jkb_monitor_items = async () => {
  try {
    let response = await axios.get(url_for_getting_jkb_monitoring_items.value);
    list_all_jkb_monitoring_items.value = response.data;
  } catch (error) {}
};
a10_get_jkb_monitor_items();
</script>

<style lang="scss" scoped>
.q-table-container {
  box-shadow: none;
}
</style>
