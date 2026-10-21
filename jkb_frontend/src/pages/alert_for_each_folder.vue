<template>
  <div class="">
    <div class="row">
      <div class="col">
        <router-link to="/">&lt; Back</router-link>

        <q-table
          class="q-ma-md"
          :title="current_folder"
          :rows="list_all_monitor_items_for_this_country"
          :columns="columns_for_jkb_alerts"
          row-key="name"
          :filter="filter"
          v-model:pagination="pagination"
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

          <template v-slot:body-cell-task_name="props">
            <q-td key="task_name" :props="props">
              <div class="" v-if="props.row.two_means_hit_threshold == 1">
                <a target="_blank" :href="props.row.link_for_snapshot">{{
                  props.row.task_name
                }}</a>
              </div>
              <div class="" v-if="props.row.two_means_hit_threshold == 2">
                <a target="_blank" :href="props.row.link_for_snapshot"
                  ><div class="text-h5 q-mt-lg text-red text-bold">
                    {{ props.row.task_name }}
                  </div>
                </a>
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-how_many_ct_not_available="props">
            <q-td :props="props">
              <div v-if="props.row.how_many_ct_not_available != 'default_none'">
                <q-avatar size="50px" font-size="30px" color="red" text-color="white">{{
                  props.row.how_many_ct_not_available
                }}</q-avatar>
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-how_many_cu_not_available="props">
            <q-td :props="props">
              <div v-if="props.row.how_many_cu_not_available != 'default_none'">
                <q-avatar size="50px" font-size="30px" color="red" text-color="white">{{
                  props.row.how_many_cu_not_available
                }}</q-avatar>
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-how_many_cm_not_available="props">
            <q-td :props="props">
              <div v-if="props.row.how_many_cm_not_available != 'default_none'">
                <q-avatar size="50px" font-size="30px" color="red" text-color="white">{{
                  props.row.how_many_cm_not_available
                }}</q-avatar>
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-how_many_other_isp_not_available="props">
            <q-td :props="props">
              <div v-if="props.row.how_many_other_isp_not_available != 'default_none'">
                <q-avatar size="50px" font-size="30px" color="red" text-color="white">{{
                  props.row.how_many_other_isp_not_available
                }}</q-avatar>
              </div>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, reactive } from "vue";
import { useRoute } from "vue-router";
import { useQuasar } from "quasar";
import { Notify } from "quasar";
const $q = useQuasar();
const route = useRoute();
const current_folder = ref(route.params.id);
const list_all_monitor_items_for_this_country = ref([]);
const filter = ref("");
// qtable col
const columns_for_jkb_alerts = [
  {
    name: "task_name",
    required: true,
    label: "Task Name",
    align: "left",
    field: (row) => row.task_name,
    sortable: true,
    style: "width: 30px;",
  },

  {
    name: "how_many_ct_not_available",
    required: true,
    label: "CT",
    align: "left",
    field: (row) => row.how_many_ct_not_available,
    sortable: true,
    headerStyle: {
      fontSize: "2em",
    },
  },
  {
    name: "how_many_cu_not_available",
    required: true,
    label: "CU",
    align: "left",
    field: (row) => row.how_many_cu_not_available,
    sortable: true,
    headerStyle: {
      fontSize: "2em",
    },
  },
  {
    name: "how_many_cm_not_available",
    required: true,
    label: "CM",
    align: "left",
    field: (row) => row.how_many_cm_not_available,
    sortable: true,
    headerStyle: {
      fontSize: "2em",
    },
  },
  {
    name: "monitor_target_ip",
    required: true,
    label: "Monitor_target_ip",
    align: "center",
    field: (row) => row.monitor_target_ip,
    sortable: true,
  },

  {
    name: "belong_to_which_infra",
    required: true,
    label: "Infra",
    align: "center",
    field: (row) => row.belong_to_which_infra,
    sortable: true,
  },
  {
    name: "group_name",
    required: true,
    label: "Country",
    align: "left",
    field: (row) => row.group_name,
    sortable: true,
  },

  {
    name: "last_check_time_readable",
    required: true,
    label: "last_check_time",
    align: "center",
    field: (row) => row.last_check_time_readable,
    sortable: true,
  },
];

const pagination = ref({ rowsPerPage: 100, sortBy: "desc" });

// qtable row
const get_the_monitor_items = async () => {
  try {
    let response_all_monitor_items_for_this_country = await axios.get(
      `/api/all_the_monitor_items_for_this_country/${current_folder.value}`
    );
    list_all_monitor_items_for_this_country.value =
      response_all_monitor_items_for_this_country.data;
  } catch (error) {
    a75_notification(`in route get_the_monitor_items, error =${error}`);
  }
};
get_the_monitor_items();

const a75_notification = (input_message) => {
  $q.notify({
    message: `${input_message}`,
    color: "purple-5",
    position: "bottom-right",
    timeout: 5000,
    actions: [
      {
        icon: "close",
        color: "white",
        handler: () => {
          /* ... */
        },
      },
    ],
  });
};
</script>

<style lang="scss" scoped>
a:link {
  color: #000000;
  text-decoration: none;
}

a:visited {
  color: #000000;
}
</style>
