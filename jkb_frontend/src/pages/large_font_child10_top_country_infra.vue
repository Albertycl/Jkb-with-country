<template>
  <div>
    <child05_infra class="q-mb-sm"></child05_infra>
    <div class="row">
      <div class="col-12">
        <!-- for country_list -->
        <div class="row justify-left">
          <!-- <div class="row"> -->
          <q-card
            v-for="(element_is_country_name, index) in list_country_list"
            :key="index"
            class="col-2 q-ma-sm"
          >
            <div class="text-h3 text-center q-pt-md">
              <router-link
                :to="{
                  name: 'alert_for_each_folder',
                  params: { id: `${element_is_country_name}` },
                }"
                >{{ element_is_country_name }}
                <q-card-section>
                  <div class="row">
                    <!-- alpha -->
                    <div class="col">
                      <!-- Alpha no alerts, but only showing ALPHA LOGO -->
                      <div
                        v-for="(item, index) in list_monitoring_which_infra_which_isp"
                        :key="index"
                      >
                        <div
                          class=""
                          v-if="
                            item.which_country == element_is_country_name &&
                            item.how_many_alerts == 0 &&
                            item.which_infra == 'alpha'
                          "
                        >
                          <div class="q-pt-lg q-mr-sm text-center text-h3">ALPHA</div>
                          <div
                            class="bg-orange text-h5 q-mt-lg q-mr-md"
                            v-if="example_store.true_show_isp === true"
                          >
                            {{ item.which_isp }}
                          </div>
                        </div>
                      </div>

                      <!-- when have alert, will show ALPHA LOGO -->
                      <div
                        v-for="(item, index) in list_monitoring_which_infra_which_isp"
                        :key="index"
                      >
                        <div
                          class=""
                          v-if="
                            item.which_country == element_is_country_name &&
                            item.how_many_alerts != 0 &&
                            item.which_infra == 'alpha'
                          "
                        >
                          <div class="text-h3 q-pt-lg q-mr-sm text-center q-mb-md">
                            ALPHA
                          </div>
                          <div
                            class="bg-orange text-h5 q-mt-lg q-mr-md"
                            v-if="example_store.true_show_isp === true"
                          >
                            {{ item.which_isp }}
                          </div>
                        </div>
                      </div>

                      <!-- showing the number for alpha how many alerts -->
                      <div
                        v-for="(item, index) in list_monitoring_which_infra_which_isp"
                        :key="index"
                      >
                        <div
                          class="text-red text-bold text-h3"
                          v-if="
                            item.which_country == element_is_country_name &&
                            item.how_many_alerts != 0 &&
                            item.which_infra == 'alpha'
                          "
                        >
                          {{ item.how_many_alerts }}
                        </div>
                        <div
                          class="text-green text-bold text-h3 q-mt-md"
                          v-if="
                            item.which_country == element_is_country_name &&
                            item.how_many_alerts == 0 &&
                            item.which_infra == 'alpha'
                          "
                        >
                          Good
                        </div>
                      </div>
                    </div>

                    <!------------------------- BRAVO----------- -->
                    <!-- showing the number for alpha how many alerts  -->
                    <div class="col">
                      <!-- no alerts, only showing bravo log -->
                      <div
                        v-for="(item, index) in list_monitoring_which_infra_which_isp"
                        :key="index"
                      >
                        <div
                          class=""
                          v-if="
                            item.which_country == element_is_country_name &&
                            item.how_many_alerts == 0 &&
                            item.which_infra == 'bravo'
                          "
                        >
                          <div class="q-pt-lg q-mr-sm text-center text-h3">BRAVO</div>
                          <div
                            class="bg-yellow text-h5 q-mt-lg q-ml-md"
                            v-if="example_store.true_show_isp === true"
                          >
                            {{ item.which_isp }}
                          </div>
                        </div>
                      </div>

                      <!--  -->
                      <div
                        v-for="(item, index) in list_monitoring_which_infra_which_isp"
                        :key="index"
                      >
                        <div
                          class=""
                          v-if="
                            item.which_country == element_is_country_name &&
                            item.how_many_alerts != 0 &&
                            item.which_infra == 'bravo'
                          "
                        >
                          <div class="text-h3 q-pt-lg q-mr-sm text-center q-mb-md">
                            BRAVO
                          </div>
                          <div
                            class="bg-yellow text-h5 q-mt-lg q-ml-md"
                            v-if="example_store.true_show_isp === true"
                          >
                            {{ item.which_isp }}
                          </div>
                        </div>
                      </div>

                      <!--  -->
                      <div
                        v-for="(item, index) in list_monitoring_which_infra_which_isp"
                        :key="index"
                      >
                        <div
                          class="text-red text-bold text-h3"
                          v-if="
                            item.which_country == element_is_country_name &&
                            item.how_many_alerts != 0 &&
                            item.which_infra == 'bravo'
                          "
                        >
                          {{ item.how_many_alerts }}
                        </div>

                        <div
                          class="text-green text-bold text-h3 q-mt-md"
                          v-if="
                            item.which_country == element_is_country_name &&
                            item.how_many_alerts == 0 &&
                            item.which_infra == 'bravo'
                          "
                        >
                          Good
                        </div>
                      </div>
                    </div>
                  </div>
                </q-card-section>
              </router-link>
            </div>
          </q-card>
        </div>
      </div>
    </div>
    <div class="text-right q-mr-md q-mt-sm">
      <div class="row">
        <div class="col-6"></div>
        <div class="col">
          <child15_top_right_possilbe_incoming_or_outgoing></child15_top_right_possilbe_incoming_or_outgoing>
          <q-btn
            color="primary"
            icon="traffic"
            label="ISP"
            class="q-mb-md q-mr-md"
            size="lg"
            @click="example_store.true_show_isp = !example_store.true_show_isp"
          />
          <!-- <router-link to="child30_threshold">
        <q-btn
          color="primary"
          icon="monitor_heart"
          label="Threshold"
          class="q-mb-md q-mr-md"
          size="lg"
      /></router-link> -->

          <q-btn
            class="q-mb-md"
            color="primary"
            label="show_template"
            @click="c40_which_country_and_isp_are_impacted()"
            size="lg"
          />
        </div>
      </div>
    </div>
    <q-dialog v-model="confirm_true_will_show_dialog_for_alert_notification_template">
      <q-card>
        <q-card-section class="row items-center">
          <!-- <span class="q-ml-sm">{{ message_to_show_in_dialog }}</span> -->
          <div v-html="show_the_templated"></div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="copy" color="primary" @click="func_to_copy_to_clipboard()" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import axios from "axios";
import { computed, reactive, ref, watchEffect, watch, onMounted } from "vue";
import { useQuasar } from "quasar";
import { Notify } from "quasar";
import { copyToClipboard } from "quasar";
import child05_infra from "src/pages/child05_infra.vue";
import { useCounterStore } from "src/stores/example-store";
import child15_top_right_possilbe_incoming_or_outgoing from "src/pages/child15_top_right_possilbe_incoming_or_outgoing.vue";
const example_store = useCounterStore();
const $q = useQuasar();
const str_country_list = ref("");
const list_country_list = ref([]);
const confirm_true_will_show_dialog_for_alert_notification_template = ref(false);
const top_a10_get_country_list = async () => {
  try {
    let resposne = await axios.get("/api/axios_get_country_list");
    str_country_list.value = resposne.data;
    list_country_list.value = str_country_list.value.split(",");
  } catch (error) {
    a75_notification(`in function top_a10_get_country_list / error=${error}`);
  }
};
top_a10_get_country_list();

// setInterval(() => {
//   top_a10_get_country_list()
// }, 60000);

// how many alerts
// which country
// which infra
const list_monitoring_which_infra_which_isp = ref([]);
const d60_get_country_name_and_how_many_alerts = async () => {
  try {
    let resposne = await axios.get(
      "/api/d60_count_how_many_alert_for_this_country_for_this_infra"
    );
    list_monitoring_which_infra_which_isp.value = resposne.data;
  } catch (error) {
    a75_notification(
      `in function d60_get_country_name_and_how_many_alerts / error=${error}`
    );
  }
};
d60_get_country_name_and_how_many_alerts();

// this is for alert template
const str_current_time = ref("");
const c30_get_current_time = async () => {
  try {
    let resposne = await axios.get("/api/c30_get_current_time");
    str_current_time.value = resposne.data;
  } catch (error) {
    a75_notification(`in function c30_get_current_time / error=${error}`);
  }
};

// this is for alert template
const str_current_time_add_10m = ref("");
const c50_current_time_add_10_mins = async () => {
  try {
    let resposne = await axios.get("/api/c50_current_time_add_10_mins");
    str_current_time_add_10m.value = resposne.data;
  } catch (error) {
    a75_notification(`in function c50_current_time_add_10_mins / error=${error}`);
  }
};

const list_country_and_infra_that_is_impacted = ref([]);
// Hi All,

// We want to provide you with an update regarding to an ISP issue that occurred on [Date and Time]

// Symptom: multiple alarms regarding to ISP: [PCCW, TWGATE, CM, CT, CU, Chief]
// Impact Scope: the ISP incident has affected [ALPHA, BRAVO, 188, SBK, LDR,NBG] in [CN, SEA, NEA]

//
const show_the_templated = computed(() => {
  let message_for_the_template = `Hi All,<br><br>We want to provide you with an update regarding to an ISP issue that occurred on ${str_current_time.value} <br><br>Symptom: Multiple alarms regarding to ISP: ${list_which_isp_now_have_problem.value}<br><br>Impact Scope: the ISP incident has affected ${list_isp_that_are_impacted.value} in ${list_country_that_are_impacted.value} <br><br>We are woking on addressing the root cause and resolving the issue, the next checkpoint for an update will be provided on ${str_current_time_add_10m.value}.`;
  return message_for_the_template;
});

const list_country_that_are_impacted = ref([]);
const list_isp_that_are_impacted = ref([]);
const c40_which_country_and_isp_are_impacted = async () => {
  list_country_that_are_impacted.value = [];
  list_isp_that_are_impacted.value = [];
  confirm_true_will_show_dialog_for_alert_notification_template.value = !confirm_true_will_show_dialog_for_alert_notification_template.value;
  c30_get_current_time();
  c50_current_time_add_10_mins();

  try {
    let resposne = await axios.get(
      "/api/c40_which_country_and_isp_are_impacted"
    );
    list_country_and_infra_that_is_impacted.value = resposne.data;
    // console.log(`list_country_and_infra_that_is_impacted=${JSON.stringify(list_country_and_infra_that_is_impacted.value)}`)
    let str_country_that_are_impact = resposne.data.country_that_are_impact;
    let str_isp_that_are_impact = resposne.data.isp_that_are_impact;

    // if multiple isp are impacted
    if (str_isp_that_are_impact.includes(",")) {
      list_isp_that_are_impacted.value = str_isp_that_are_impact.split(",");
    } else {
      // for handling when there's only 1 isp that's impacted
      list_isp_that_are_impacted.value.push(str_isp_that_are_impact);
    }
    if (str_country_that_are_impact.includes(",")) {
      list_country_that_are_impacted.value = str_country_that_are_impact.split(",");
    } else {
      // for handling when there's only 1 country that's impacted
      list_country_that_are_impacted.value.push(str_country_that_are_impact);
    }
  } catch (error) {
    a75_notification(
      `in function c40_which_country_and_isp_are_impacted / error=${error}`
    );
  }
};

// this is for handling the template this --> Impact Scope: the ISP incident has affected
// list_which_isp_now_have_problem.value is the wording that will show in the template
const list_which_isp_now_have_problem = ref("");
watch(
  () => example_store.list_which_isp_have_alert,
  (newvalue_list_which_isp_have_alert) => {
    list_which_isp_now_have_problem.value = "";
    example_store.list_which_isp_have_alert.forEach((element) => {
      list_which_isp_now_have_problem.value =
        list_which_isp_now_have_problem.value + "," + element;
    });
    // remove the "," that's in the front
    if (list_which_isp_now_have_problem.value.startsWith(",")) {
      list_which_isp_now_have_problem.value = list_which_isp_now_have_problem.value.slice(
        1
      );
    }
  }
);

const func_to_copy_to_clipboard = () => {
  const textWithLineBreak = show_the_templated.value.replace(/<br>/g, "\n");
  // copyToClipboard is quasar build in function
  copyToClipboard(textWithLineBreak);
};

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
    d60_get_country_name_and_how_many_alerts();
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

.my-table th {
  font-size: 200px;
}

.my-table td {
  font-size: 106px;
}
</style>
