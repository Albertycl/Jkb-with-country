<template>
  <div>
    <div class="q-ml-sm text-h5 text-grey">Infra</div>
    <div class="row q-ml-sm">
      <q-card
        class="col-2 text-center q-mr-sm my-card"
        v-for="(item, index) in list_outgoing_monitoring_which_infra_which_isp"
        :key="index"
      >
        <!-- item={{ item }} -->
        <router-link :to="`/alert_for_incoming_isp_monitoring/${item.which_isp}`">
          <q-card-section class="text-h4 text-center">
            {{ item.which_isp }}
          </q-card-section>
          <q-card-section
            class="bg_allen_green text-bold text-h4 text-white"
            v-if="item.how_many_alerts == 0"
          >
            {{ item.how_many_alerts }}
            <!-- <q-card-section class="bg_allen_green" v-if="item.how_many_alerts == 0"> -->
          </q-card-section>
          <q-card-section
            class="bg_allen_red text-bold text-h4 text-white"
            v-if="item.how_many_alerts != 0"
          >
            {{ item.how_many_alerts }}
          </q-card-section>
        </router-link>
      </q-card>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";

import { ref, watch, reactive } from "vue";
import { useQuasar } from "quasar";
import { Notify } from "quasar";

import { useCounterStore } from "src/stores/example-store";
const example_store = useCounterStore();

const $q = useQuasar();
const list_outgoing_monitoring_which_infra_which_isp = ref([]);
const d90_a100_monitoring_specific_isp = async () => {
  try {
    let resposne = await axios.get(
      `/api/d90_a100_monitoring_specific_isp/`
    );
    list_outgoing_monitoring_which_infra_which_isp.value = resposne.data;
  } catch (error) {
    a75_notification(`in function d90_a100_monitoring_specific_isp / error=${error}`);
  }
};

d90_a100_monitoring_specific_isp();

const child05_which_isp_have_alert = () => {
  example_store.list_which_isp_have_alert = [];
  list_outgoing_monitoring_which_infra_which_isp.value.forEach((element) => {
    if (element.how_many_alerts > 0) {
      example_store.list_which_isp_have_alert.push(element.which_isp);
    }
  });
};

watch(
  () => list_outgoing_monitoring_which_infra_which_isp.value,
  (newvalue) => {
    child05_which_isp_have_alert();
  }
);

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
  (newvalue, oldvalue) => {
    if (newvalue != oldvalue) {
      d90_a100_monitoring_specific_isp();
    }
  }
);
</script>

<style lang="scss" scoped>
a:link {
  color: #000000;
  text-decoration: none;
}

a:visited {
  color: #000000;
}

.my-card {
  width: 100%;
  max-width: 305px;
}

.bg_allen_red {
  background: #d65749 !important;
}

.bg_allen_green {
  background: #2dad42 !important;
}
</style>
