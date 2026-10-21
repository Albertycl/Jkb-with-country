<template>
  <div class="bg_color_allen_grey">
    <!-- <q-btn
      color="yellow-10"
      label="trigger_all_the_child_components"
      @click="trigger_all_the_child_components()"
    /> -->
    <router-link to="/">
      <div class="text-grey-7 text-h3 text-bold q-mt-md q-ml-sm">
        KANBAN: Global ISP Status
      </div>
    </router-link>
    <child05_infra class="q-mb-sm"></child05_infra>
    <child10_top_country></child10_top_country>
    <child20_bottom_original_jkb_alert_table
      class="q-mt-md"
    ></child20_bottom_original_jkb_alert_table>
  </div>
</template>

<script setup>
import { ref } from "vue";
import child05_infra from "src/pages/child05_infra.vue";
import child10_top_country from "src/pages/child10_top_country.vue";
import child20_bottom_original_jkb_alert_table from "src/pages/child20_bottom_original_jkb_alert_table.vue";
import { useCounterStore } from "src/stores/example-store";
const example_store = useCounterStore();
setInterval(() => {
  example_store.triggering_function_in_child_component =
    example_store.triggering_function_in_child_component + 1;
}, 60000);

const trigger_all_the_child_components = () => {
  example_store.triggering_function_in_child_component++;
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

.bg_color_allen_grey {
  background: #f4f5f5 !important;
}
</style>
