<template>
  <div class="workplace grid grid-rows-none gap-4 mt-xxs">
    <div class="button-container grid grid-cols-2 gap-6"> <!-- 使用 grid 布局和 gap 设置间距 -->
      <mini-statistic-card
        v-for="(item, i) in statisticList"
        :key="i"
        :title="item.title"
        :value="item.value"
        :url="item.url"
        :class="['button', item.value ? 'bg-green-500' : 'bg-red-500']"
      >
        <template #icon>
          <component
            :class="`text-[96px] translate-x-[25%] translate-y-[25%] opacity-75 ${item.iconClass}`"
            v-bind:is="item.icon"
          />
        </template>
      </mini-statistic-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue';
import MiniStatisticCard from "@/components/statistic/MiniStatisticCard.vue";

const statisticList = reactive([
  {
    value: 'Ping',
    title: 'Checking...',
    url: '/ping',
    icon: 'dollar-circle-filled',
    iconClass: 'text-blue-100',
  },
  {
    value: 'python packages',
    title: 'Checking...',
    url: '/check_python_packages',
    icon: 'smile-add-outlined',
    iconClass: 'text-purple-100',
  },
  {
    value: 'node version',
    title: 'Checking...',
    url: '/check_node_version',
    icon: 'success-add-outlined',
    iconClass: 'text-purple-100',
  },
  {
    value: 'network connectivity',
    title: 'Checking...',
    url: '/check_network_connectivity',
    icon: 'usergroup-add-outlined',
    iconClass: 'text-purple-100',
  }
]);
</script>
