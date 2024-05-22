<script setup lang="ts">

import Projects from '@/pages/workplace/Projects.vue';
import MiniStatisticCard from '@/components/statistic/MiniStatisticCard.vue';
import { useUnbounded } from '@/utils/useTheme';
import { reactive } from 'vue';

  useUnbounded();


  const statisticList = reactive([
    {
      title: '正在运行',
      value: '100',
      icon: 'dollar-circle-filled',
      iconClass: 'text-blue-100',
    },
    {
      title: '正在运行',
      value: '138',
      icon: 'usergroup-add-outlined',
      iconClass: 'text-purple-100',
    },
    {
      title: '正在运行',
      value: '5000',
      icon: 'heart-filled',
      iconClass: 'text-primary-100',
    },
    {
      title: '正在运行',
      value: '3200',
      icon: 'shopping-filled',
      iconClass: 'text-green-100',
    },
  ]);
</script>



<template>
  <div class="workplace grid grid-rows-none gap-4 mt-xxs">
    <div class="grid grid-cols-12 gap-6">
      <mini-statistic-card
        class="card col-span-12 mdx:col-span-6 xlx:col-span-3"
        v-for="(item, i) in statisticList"
        :key="i"
        :title="item.title"
        :value="item.value"
      >
        <template #icon>
          <component
            :class="`text-[96px] translate-x-[25%] translate-y-[25%] opacity-75 ${item.iconClass}`"
            v-bind:is="item.icon"
          />
        </template>
      </mini-statistic-card>
    </div>

    <div class="workplace grid grid-rows-none gap-4 mt-xxs">
      <div class="project-list grid grid-cols-12 gap-4">
        <projects class="col-span-12 xlx:col-span-12 xxlx:col-span-20 drop-shadow-sm" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">

</style>