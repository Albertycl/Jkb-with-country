<template>
  <q-layout view="lHh Lpr lFf">
    <!-- <q-header elevated>
      <q-toolbar class="bg_color_allen_grey">
        <q-toolbar-title>
          <router-link to="/">
            <div class="text-grey text-h3 text-bold q-mt-md q-mb-md">
              KANBAN: Global ISP Status
            </div>
          </router-link>
        </q-toolbar-title>
      </q-toolbar>
    </q-header> -->

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
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
