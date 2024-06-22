<template>
  <button
    class="mini-statistic-card overflow-hidden relative bg-container
    inline-flex items-center justify-between drop-shadow-sm p-md border-border rounded-lg"
    :class="cardColorClass"
    @click="handleClick"
  >
    <div class="statistic-main">
      <div class="statistic-title text-subtext text-xs">{{ title }}</div>
      <div class="statistic-content flex items-baseline">
        <span class="value text-title text-xxl font-bold">{{ value }}</span>
      </div>
      <div v-if="cardMsgClass" class="statistic-content flex items-baseline mt-2">
        <span class="value text-title text-xl">{{ cardMsgClass }}</span>
      </div>
    </div>
    <div class="statistic-icon absolute bottom-0 right-0"><slot name="icon"></slot></div>
  </button>
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'MiniStatisticCard',
  props: {
    title: String,
    value: [String, Number] as PropType<string | number>,
    url: String, // URL for the GET request
    result: String
  },
  setup(props) {
    const success = ref(false);
    const result = ref("");

    const handleClick = async () => {
      if (props.url) {
        try {
          const response = await axios.get(props.url);
          console.log(response.data);
          success.value = response.data.status; // 假设返回的响应包含 success 布尔值
          result.value = response.data.result;
        } catch (error) {
          console.error('Failed to fetch data:', error);
          success.value = false; // 请求失败时设为 false
        }
      }
    };

    const cardColorClass = computed(() => {
      return success.value ? 'bg-green-500' : 'bg-red-500';
    });
    const cardMsgClass = computed(() => {
      return result.value;
    });

    return {
      handleClick,
      cardColorClass,
      cardMsgClass,
    };
  },
});
</script>

<style lang="less" scoped>
.mini-statistic-card {
  cursor: pointer;
  transition: background-color 0.3s, height 0.3s, width 0.3s;
  min-width: 200px; /* 设置一个最小宽度，避免太窄 */
  padding: 1rem; /* 内边距 */
  display: inline-flex; /* 使其内部内容影响外部尺寸 */
  flex-direction: column; /* 使内容按列排列 */
  align-items: flex-start; /* 左对齐内容 */
}

.bg-green-500 {
  background-color: #38a169; /* Tailwind的绿色 */
}

.bg-red-500 {
  background-color: #e53e3e; /* Tailwind的红色 */
}

/* 通过取消默认按钮样式确保外观一致 */
button {
  border: none;
  background: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
  display: flex; /* 确保按钮的内容影响其尺寸 */
  width: 100%; /* 让按钮撑满外部容器的宽度 */
}
</style>
