<template>
  <div class="projects card">
    <div class="flex items-baseline justify-between w-full">
      <overview-title title="运行进程" subtitle="基本信息" />
    </div>
    <div>
      <a-table :columns="columns" :dataSource="dataSource" :pagination="false">
        <template #bodyCell="{ text, record, column }">
          <!-- 显示所有记录的 status 列 -->
          <div v-if="column.dataIndex === 'status'">
            {{ record[column.dataIndex] }}
          </div>

          <!-- 自定义 progress 列 -->
          <div v-else-if="column.dataIndex === 'progress'">
            <div class="flex items-center">
              <!-- 显示 progress 的值 -->
<!--              <span class="ml-sm p-2">{{ record[column.dataIndex] }}</span>-->
              <!-- 仅当 progress 存在时显示终止按钮 -->
              <a-radio-group v-if="record[column.dataIndex]">
                <a-radio-button @click="terminateTask(record.pID)">终止</a-radio-button>
              </a-radio-group>
            </div>
          </div>

          <!-- 其他列显示默认文本内容 -->
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
  { title: '运行状态', dataIndex: 'status'},
  { title: '相关操作', dataIndex: 'progress' },
];
const dataSource = ref([]);

const getAllTaskInfo = async () => {
  try {
    const response = await axios.get('/all_task_ids');

    const newEntries = response.data.task_ids.map((id: string) => ({
      pID: id,
      status: '运行中',
      progress: 'terminate'
    }));

    newEntries.forEach((entry: void) => {
      dataSource.value.push(entry);
    })
    console.log('runningTasks查询成功:', dataSource.value, '=======', response.data.task_ids);
  } catch (error) {
    console.error('Failed to get ids', error);
  }
};
const addTaskIdsDataSource = (response, status): void => {
  const newEntries = response.data.task_ids.map((id: string) => ({
      pID: id,
      status: status
    }));
  newEntries.forEach((entry: void) => {
    dataSource.value.push(entry);
  })
}
const getSuccessTaskInfo = async () => {
  try {
    const response = await axios.get('/success_task_ids');
    addTaskIdsDataSource(response, '运行成功');
    console.log('successTasks查询成功:', dataSource.value, '=======', response.data.task_ids);
  } catch (error) {
    console.error('Failed to get ids', error);
  }
};

const getFailedTaskInfo = async () => {
  try {
    const response = await axios.get('/failed_task_ids');
    addTaskIdsDataSource(response, '运行失败');
    console.log('failedTasks查询成功:', dataSource.value, '=======', response.data.task_ids);
  } catch (error) {
    console.error('Failed to get ids', error);
  }
};

const getTerminatedTaskInfo = async () => {
  try {
    const response = await axios.get('/terminated_task_ids');
    addTaskIdsDataSource(response, '已终止');
    console.log('terminatedTasks查询成功:', dataSource.value, '=======', response.data.task_ids);
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
  getTerminatedTaskInfo();
  getSuccessTaskInfo();
  getFailedTaskInfo();
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
