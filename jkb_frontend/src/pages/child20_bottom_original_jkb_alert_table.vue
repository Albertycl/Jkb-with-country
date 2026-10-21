<template>
  <div>
    <div class="row">
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

          <template v-slot:body-cell-task_name="props">
            <q-td key="task_name" :props="props">
              <div class="" v-if="props.row.two_means_hit_threshold == 1">
                <a target="_blank" :href="props.row.link_for_snapshot">{{
                  props.row.task_name
                }}</a>
              </div>
              <div class="" v-if="props.row.two_means_hit_threshold == 2">
                <a target="_blank" :href="props.row.link_for_snapshot"
                  ><div class="text-h3 q-mt-lg text_allen_red text-bold">
                    {{ props.row.task_name }}
                  </div>
                </a>
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-how_many_ct_not_available="props">
            <q-td :props="props">
              <div v-if="props.row.how_many_ct_not_available != 'default_none'">
                <q-avatar
                  size="50px"
                  font-size="30px"
                  class="text_allen_red"
                  text-color="white"
                  >{{ props.row.how_many_ct_not_available }}</q-avatar
                >
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-how_many_cu_not_available="props">
            <q-td :props="props">
              <div v-if="props.row.how_many_cu_not_available != 'default_none'">
                <q-avatar
                  size="50px"
                  font-size="30px"
                  class="text_allen_red"
                  text-color="white"
                  >{{ props.row.how_many_cu_not_available }}</q-avatar
                >
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-how_many_cm_not_available="props">
            <q-td :props="props">
              <div v-if="props.row.how_many_cm_not_available != 'default_none'">
                <q-avatar
                  size="50px"
                  font-size="30px"
                  class="text_allen_red"
                  text-color="white"
                  >{{ props.row.how_many_cm_not_available }}</q-avatar
                >
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-how_many_other_isp_not_available="props">
            <q-td :props="props">
              <div v-if="props.row.how_many_other_isp_not_available != 'default_none'">
                <q-avatar
                  size="50px"
                  font-size="30px"
                  class="text_allen_red"
                  text-color="white"
                  >{{ props.row.how_many_other_isp_not_available }}</q-avatar
                >
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-last_check_time_readable="props">
            <q-td :props="props">
              <div class="text-h3">{{ props.row.last_check_time_readable }}</div>
            </q-td>
          </template>
        </q-table>
      </div>
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
    name: "task_name",
    required: true,
    label: "Task Name",
    align: "center",
    field: (row) => row.task_name,
    sortable: true,
    headerStyle: {
      fontSize: "3em",
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
      fontSize: "3em",
    },
  },
  {
    name: "how_many_ct_not_available",
    required: true,
    label: "CT",
    align: "left",
    field: (row) => row.how_many_ct_not_available,
    sortable: true,
    headerStyle: {
      fontSize: "3em",
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
      fontSize: "3em",
    },
  },
  {
    name: "monitor_target_ip",
    required: true,
    label: "IP",
    align: "center",
    field: (row) => row.monitor_target_ip,
    sortable: true,
    headerStyle: {
      fontSize: "3em",
    },
  },

  {
    name: "belong_to_which_infra",
    required: true,
    label: "Infra",
    align: "left",
    field: (row) => row.belong_to_which_infra,
    sortable: true,
    headerStyle: {
      fontSize: "3em",
    },
  },
  {
    name: "group_name",
    required: true,
    label: "Country",
    align: "left",
    field: (row) => row.group_name,
    sortable: true,
    headerStyle: {
      fontSize: "3em",
    },
  },
  {
    name: "last_check_time_readable",
    required: true,
    label: "Time",
    align: "center",
    field: (row) => row.last_check_time_readable,
    sortable: true,
    headerStyle: {
      fontSize: "3em",
    },
  },

  // {
  //   name: "how_many_other_isp_not_available",
  //   required: true,
  //   label: "OTHERS",
  //   align: "left",
  //   field: (row) => row.how_many_other_isp_not_available,
  //   sortable: true,
  //   headerStyle: {
  //     fontSize: "3em",
  //   },
  // },
];

//

const url_for_getting_jkb_monitoring_items = ref(
  "/api/axios_query_db_all_monitoring_items_detail"
);
const list_all_jkb_monitoring_items = ref([]);
const pagination = ref({ rowsPerPage: 100, sortBy: "desc" });
const a10_get_jkb_monitor_items = async () => {
  try {
    let response = await axios.get(url_for_getting_jkb_monitoring_items.value);
    list_all_jkb_monitoring_items.value = response.data;
  } catch (error) {}
};
a10_get_jkb_monitor_items();

// setInterval(() => {
//   a10_get_jkb_monitor_items();
// }, 60000);

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

watch(
  () => example_store.triggering_function_in_child_component,
  (value) => {
    a10_get_jkb_monitor_items();
  }
);
</script>

<style lang="scss" scoped>
.custom-q-table .q-table__cell {
  font-size: 50px; /* Change this value to your desired font size */
}

a:link {
  color: #000000;
  text-decoration: none;
}

a:visited {
  color: #000000;
}

.text_allen_red {
  color: #d65749 !important;
}
</style>
