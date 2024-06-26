<script setup lang="ts">

import { useUnbounded } from '@/utils/useTheme';
import Results from "@/pages/report/Results.vue";

  useUnbounded();


</script>



<template>
  <div class="workplace grid grid-rows-none gap-4 mt-xxs">

    <div class="workplace grid grid-rows-none gap-4 mt-xxs">
      <div class="project-list grid grid-cols-12 gap-4">
        <Results class="col-span-12 xlx:col-span-12 xxlx:col-span-20 drop-shadow-sm" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">

</style>