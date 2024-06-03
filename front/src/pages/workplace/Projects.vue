<template>
  <div class="projects card">
    <div class="flex items-baseline justify-between w-full">
      <overview-title title="运行进程" subtitle="基本信息" />
    </div>
    <div>
      <a-table :columns="columns" :dataSource="dataSource" :pagination="false">
        <template #bodyCell="{ text, record, column }">
          <div v-if="column.dataIndex === 'progress'">
            <div class="flex items-center">
              <span class="ml-sm p-2">{{ record[column.dataIndex] }}</span>
                <a-radio-group>
                  <a-radio-button @click="terminateTask(record.pID)">终止</a-radio-button>
                </a-radio-group>
            </div>
          </div>

          <div v-else-if="column.dataIndex === 'result'">
            <div class="flex items-center">
              123
            </div>
          </div>

          <div v-else>
            {{ text }}
          </div>
        </template>
      </a-table>
      <a-button size="large" class="add-btn" type="dashed" @click="goToWorkplace">
        <template #icon>
        </template>
        添加新项目
      </a-button>
    </div>
  </div>
</template>
<script lang="ts" setup>
import OverviewTitle from '@/components/statistic/OverviewTitle.vue';

import {computed, onMounted, reactive, ref} from "vue";
import axios from "axios";
import router from "@/router";


const columns = [
  { title: '进程ID', dataIndex: 'pID' },
  { title: '运行结果', dataIndex: 'result'},
  { title: '相关操作', dataIndex: 'progress' },
];
const dataSource = ref([]);

const getAllTaskInfo = async () => {
  try {
    const response = await axios.get('/all_task_ids');
    dataSource.value = response.data.task_ids.map((id: string) => ({
      pID: id,
      progress: '运行中'
    }));
    console.log('查询成功:', response.data['task_ids']);
  } catch (error) {
    console.error('Failed to get ids', error);
  }
};
const terminateTask = async (taskId: string) => {
  try{
    const response = await axios.post('/terminate_task', {task_id: taskId});
    console.log(`终止任务成功： ${response.data}`);
    await getAllTaskInfo();
  }catch (error){
    console.error("Failed to terminate task:", error);
  }
}
const goToWorkplace = () =>{
  router.push('/workplace');
}

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
