<template>
  <div class="workplace grid grid-rows-none gap-4 mt-xxs">
    <div class="bg-container p-base rounded-b-lg rounded-tr-lg pt-8 flex items-end justify-between">
      <TerminalInfo class="col-span-12 sm:col-span-12 md:col-span-10 lg:col-span-8 xl:col-span-6 xlx:col-span-7 xxlx:col-span-8 drop-shadow-sm"/>
    </div>

    <div class="bg-container p-base rounded-b-lg rounded-tr-lg pt-8 flex items-end justify-between">

    </div>

  </div>
</template>

<script lang="ts" setup>
  import { reactive } from 'vue';
  import MiniStatisticCard from '@/components/statistic/MiniStatisticCard.vue';
  import Projects from './Projects.vue';
  import { useUnbounded } from '@/utils/useTheme';
  import TerminalInfo from '@/components/terminal/terminalInfo.vue';

  useUnbounded();



</script>

<style scoped lang="less">
  .workplace {
  }
</style>
