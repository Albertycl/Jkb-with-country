<template>
  <div class="row no-wrap infra-columns">
    <div v-for="infra in infras" :key="infra" class="col-6 infra-col">
      <template v-if="cellFor(infra)">
        <div class="text-h5 text-center">{{ infra.toUpperCase() }}</div>
        <div class="isp-area">
          <div v-if="example_store.true_show_isp === true" class="isp-list">
            <span
              v-for="(isp, i) in cellFor(infra).which_isp || []"
              :key="i"
              class="isp-chip text-h6"
              :class="infra === 'alpha' ? 'bg-orange' : 'bg-yellow'"
              >{{ isp }}</span
            >
          </div>
        </div>
        <div
          v-if="cellFor(infra).how_many_alerts != 0"
          class="text-red text-bold text-h3 text-center"
        >
          {{ cellFor(infra).how_many_alerts }}
        </div>
        <div v-else class="text-green text-bold text-h3 text-center">Good</div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from "src/stores/example-store";

const props = defineProps({
  country: { type: String, required: true },
  items: { type: Array, default: () => [] },
});
const infras = ["alpha", "bravo"];
const example_store = useCounterStore();

const cellFor = (infra) =>
  props.items.find((i) => i.which_country == props.country && i.which_infra == infra);
</script>

<style scoped>
.infra-col {
  display: flex;
  flex-direction: column;
  padding: 0 4px;
}
.isp-area {
  flex: 1;
  min-height: 24px;
}
.isp-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  margin: 6px 0;
}
.isp-chip {
  display: inline-block;
  max-width: 100%;
  padding: 0 6px;
  border-radius: 4px;
  line-height: 1.5;
  text-align: center;
  overflow-wrap: anywhere;
}
</style>
