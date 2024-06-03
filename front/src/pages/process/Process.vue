<script setup lang="ts">

import Projects from '@/pages/workplace/Projects.vue';
import MiniStatisticCard from '@/components/statistic/MiniStatisticCard.vue';
import { useUnbounded } from '@/utils/useTheme';
import { reactive } from 'vue';

  useUnbounded();


</script>



<template>
  <div class="workplace grid grid-rows-none gap-4 mt-xxs">

    <div class="workplace grid grid-rows-none gap-4 mt-xxs">
      <div class="project-list grid grid-cols-12 gap-4">
        <projects class="col-span-12 xlx:col-span-12 xxlx:col-span-20 drop-shadow-sm" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">

</style>