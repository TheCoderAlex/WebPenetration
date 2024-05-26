<template>
  <div class="projects card ">
    <div class="flex items-baseline justify-between w-full">
      <overview-title title="运行进程" subtitle="基本信息" />
    </div>
    <div>
      <a-table :columns="columns" :dataSource="dataSource" :pagination="false">
        <div class="" v-for="items in dataSource" :key="items">
          <h3>{{ items }}</h3>
          <div class="flex items-center">
            <span class="ml-sm">{{ items }}</span>
          </div>
          <a-radio-group>
            <a-radio-button>终止</a-radio-button>
          </a-radio-group>
        </div>
      </a-table>
      <a-button size="large" class="add-btn" type="dashed">
        <template #icon>
        </template>
        添加新项目
      </a-button>
    </div>
  </div>
</template>
<script lang="ts" setup>
import OverviewTitle from '@/components/statistic/OverviewTitle.vue';
import { formatThousand } from '@/utils/formatter';
import {computed, onMounted, reactive, ref} from "vue";
import axios from "axios";

const columns = [
  { title: '进程ID', dataIndex: 'pID' },
  { title: '相关操作', dataIndex: 'progress' },
];
const dataSource = ref<string[]>([]);

const getAllTaskInfo = async () => {
  try {
    const response = await axios.get('/all_task_ids');
    dataSource.value = response.data['task_ids'];
    console.log('查询成功:', response.data['task_ids']);
  } catch (error) {
    console.error('Failed to start task:', error);
  }
};

onMounted(() => {
  getAllTaskInfo();
});


</script>
<style lang="less" scoped>
  .projects {
    :deep(.ant-table) {
      @apply -mx-md;

      .ant-table-thead {
        > tr > th:first-child {
          @apply pl-lg;
        }

        > tr > th:last-child {
          @apply pr-lg;
        }
      }

      .ant-table-tbody {
        > tr > td {
          @apply border-b-0 border-t;

          &:first-child {
            @apply pl-lg;
          }

          &:last-child {
            @apply pr-lg;
          }
        }
      }
    }

    :deep(.ant-table-thead > tr > th) {
      @apply border-none bg-transparent text-subtext;

      &:not(:last-child):not(.ant-table-selection-column):not(.ant-table-row-expand-icon-cell):not([colspan])::before {
        @apply bg-transparent;
      }
    }

    .add-btn {
      @apply justify-center flex items-center mt-md -mx-2;
      width: calc(100% + 16px);
    }
  }
</style>
