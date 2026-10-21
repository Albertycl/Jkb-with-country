<template>
  <div class="row q-gutter-md q-mt-xs">
    <div
      v-for="b in banners"
      :key="b.infra"
      class="text-h4 text-bold text-white bg_allen_red q-px-md q-py-xs cursor-pointer"
      @click="open_reason(b.infra)"
    >
      {{ b.title }}
      <q-icon name="info" size="sm" class="q-ml-xs" />
      <q-tooltip>Click to see why this was triggered</q-tooltip>
    </div>

    <q-dialog v-model="show_dialog">
      <q-card style="min-width: 480px; max-width: 90vw">
        <q-card-section class="bg_allen_red text-white text-h5 text-bold">
          {{ dialog_title }}
        </q-card-section>
        <q-card-section>
          <div class="text-subtitle1 q-mb-sm">
            Triggered because
            <b>{{ dialog_total }}</b>
            alerting sensor row(s) were found on the {{ dialog_infra_label }}
            probe IPs below:
          </div>
          <q-markup-table flat dense>
            <thead>
              <tr>
                <th class="text-left">Probe</th>
                <th class="text-left">Target IP</th>
                <th class="text-right">Alerting sensors</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in dialog_rows" :key="r.which_isp">
                <td>{{ r.which_isp }}</td>
                <td>{{ probe_ip[r.which_isp] }}</td>
                <td
                  class="text-right text-bold"
                  :class="r.how_many_alerts > 0 ? 'text-red' : 'text-green'"
                >
                  {{ r.how_many_alerts }}
                </td>
              </tr>
            </tbody>
          </q-markup-table>
          <div class="q-mt-md">
            <div><b>Rule:</b> total 0 = no banner, total exactly 1 = "Incoming Issue", total 2 or more = "Outgoing Issue".</div>
            <div class="q-mt-xs">
              An alerting sensor is a row in the sensor table whose threshold result is 2 (triggered) and whose target is one of these probe IPs. The check runs on page load and every 60 seconds.
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed, watch } from "vue";
import { useCounterStore } from "src/stores/example-store";

const example_store = useCounterStore();
const rows = ref([]);
const show_dialog = ref(false);
const dialog_infra = ref("alpha");

const probe_ip = {
  "ALPHA_PCCW": "198.51.100.254",
  "ALPHA_TWG-G": "192.0.2.254",
  "ALPHA_CHIEF": "198.18.0.254",
  "BRAVO_Singtel": "198.19.0.254",
  "BRAVO_PCCW": "203.0.113.254",
  "BRAVO_TWG-G": "198.18.1.254",
};
const infra_name = { alpha: "Alpha", bravo: "Bravo" };

const total_for = (infra) =>
  rows.value
    .filter((r) => r.which_infra == infra)
    .reduce((sum, r) => sum + r.how_many_alerts, 0);

const banners = computed(() =>
  ["alpha", "bravo"]
    .map((infra) => ({ infra, total: total_for(infra) }))
    .filter((b) => b.total > 0)
    .map((b) => ({
      infra: b.infra,
      title: `Possible ${infra_name[b.infra]} ${b.total == 1 ? "Incoming" : "Outgoing"} Issue`,
    }))
);

const dialog_rows = computed(() =>
  rows.value.filter((r) => r.which_infra == dialog_infra.value)
);
const dialog_total = computed(() => total_for(dialog_infra.value));
const dialog_infra_label = computed(() => infra_name[dialog_infra.value]);
const dialog_title = computed(
  () =>
    banners.value.find((b) => b.infra == dialog_infra.value)?.title ??
    `${dialog_infra_label.value}: no active alert`
);

const open_reason = (infra) => {
  dialog_infra.value = infra;
  show_dialog.value = true;
};

const load = async () => {
  try {
    const response = await axios.get("/api/d90_a100_monitoring_specific_isp/");
    rows.value = response.data;
  } catch (error) {
    console.log(`error=${error}`);
  }
};
load();

watch(
  () => example_store.triggering_function_in_child_component,
  (newvalue, oldvalue) => {
    if (newvalue != oldvalue) load();
  }
);
</script>

<style lang="scss" scoped>
.bg_allen_red {
  background: #d65749 !important;
}
</style>
