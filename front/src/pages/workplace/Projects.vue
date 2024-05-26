<template>
  <div class="projects card">
    <div class="flex items-baseline justify-between w-full">
      <overview-title title="运行进程" subtitle="基本信息" />
    </div>
    <div>
      <a-table :columns="columns" :dataSource="dataSource.value" :pagination="false">
        <template #bodyCell="{ text, record, column }">
          <div v-if="column.dataIndex === 'progress'">
            <div class="flex items-center">
              <span class="ml-sm">{{ record[column.dataIndex] }}</span>
              <a-radio-group>
                <a-radio-button>终止</a-radio-button>
              </a-radio-group>
            </div>
          </div>
          <div v-else>
            {{ text }}
          </div>
        </template>
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
import { ref, onMounted } from 'vue';
import axios from 'axios';

const columns = [
  { title: '进程ID', dataIndex: 'pID' },
  { title: '相关操作', dataIndex: 'progress' },
];

const dataSource = ref([]);

const getAllTaskInfo = async () => {
  try {
    const response = await axios.get('/all_task_ids');
    dataSource.value = response.data.task_ids.map((id: string) => ({
      pID: id,
      progress: '运行中'  // 这里可以根据需要修改
    }));
    console.log('查询成功:', dataSource.value);
  } catch (error) {
    console.error('Failed to get ids', error);
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
