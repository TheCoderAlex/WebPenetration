<template>
  <div class="projects card">
    <a-modal
      title="测试报告"
      centered=true
      okText="确认"
      cancelText="取消"
      :visible="visible"
      @ok="handleOk"
      @cancel="handleCancel"
      width="100%"
      wrapClassName="full-modal"
    >
      <a-table :columns="result_columns" :dataSource="resultTableData"  :scroll="{ x: 'max-content'}" :rowKey="record => record.id" />
    </a-modal>
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
              <a-radio-group>
                <a-radio-button v-if="record['status'] === '运行中'" @click="terminateTask(record.pID)">终止</a-radio-button>
                <a-radio-button v-if="record['status'] !== '运行中'" disabled>终止</a-radio-button>
              </a-radio-group>
            </div>
          </div>  
          <div v-else-if="column.dataIndex === 'download'">
            <div class="flex items-center">
              <a-radio-group>
                <a-radio-button v-if="record['status'] === '运行成功'" @click="showReport(record.filename)">查看</a-radio-button>
                <a-radio-button v-if="record['status'] !== '运行成功'" disabled>查看</a-radio-button>
              </a-radio-group>
            </div>
          </div>
          <div v-else-if="column.dataIndex === 'exploit'">
            <div class="flex items-center">
              <a-radio-group>
                <a-radio-button v-if="record['status'] === '运行成功'" @click="showExploit(record.filename)">查看</a-radio-button>
                <a-radio-button v-if="record['status'] !== '运行成功'" disabled>查看</a-radio-button>
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

const visible = ref(false);

const result_columns = [
  {
    title: 'Cloud Type',
    dataIndex: 'cloud_type',
    key: 'cloud_type',
  },
  {
    title: 'Date',
    dataIndex: 'date',
    key: 'date',
  },
  {
    title: 'Error Message',
    dataIndex: 'error_msg',
    key: 'error_msg',
  },
  {
    title: 'FQDN',
    dataIndex: 'fqdn',
    key: 'fqdn',
  },
  {
    title: 'IP Address',
    dataIndex: 'ip_addr',
    key: 'ip_addr',
  },
  {
    title: 'Log',
    dataIndex: 'log',
    key: 'log',
  },
  {
    title: 'Method',
    dataIndex: 'method',
    key: 'method',
  },
  {
    title: 'Origin Login',
    dataIndex: 'origin_login',
    key: 'origin_login',
  },
  {
    title: 'Origin Login Trigger',
    dataIndex: 'origin_login_trigger',
    key: 'origin_login_trigger',
  },
  {
    title: 'Origin URL',
    dataIndex: 'origin_url',
    key: 'origin_url',
  },
  {
    title: 'Port',
    dataIndex: 'port',
    key: 'port',
  },
  {
    title: 'Product Name',
    dataIndex: 'prod_name',
    key: 'prod_name',
  },
  {
    title: 'Product Trigger',
    dataIndex: 'prod_trigger',
    key: 'prod_trigger',
  },
  {
    title: 'Product Type',
    dataIndex: 'prod_type',
    key: 'prod_type',
  },
  {
    title: 'Product Version',
    dataIndex: 'prod_version',
    key: 'prod_version',
  },
  {
    title: 'Product Vulnerability',
    dataIndex: 'prod_vuln',
    key: 'prod_vuln',
  },
  {
    title: 'Server Header',
    dataIndex: 'server_header',
    key: 'server_header',
  },
  {
    title: 'URL',
    dataIndex: 'url',
    key: 'url',
  },
  {
    title: 'Vendor Name',
    dataIndex: 'vendor_name',
    key: 'vendor_name',
  },
  {
    title: 'Wrong Comment',
    dataIndex: 'wrong_comment',
    key: 'wrong_comment',
  },
];

const resultTableData = ref([])

const columns = [
  { title: '进程ID', dataIndex: 'pID' },
  { title: '运行状态', dataIndex: 'status'},
  { title: '进程操作', dataIndex: 'progress' },
  { title: '结果文件', dataIndex: 'filename' },
  { title: '文件大小', dataIndex: 'size' },
  { title: '测试结果', dataIndex: 'download' },
  { title: '攻击结果', dataIndex: 'exploit' },
];
const dataSource = ref([]);
const fileSource = ref([]);

const handleOk = () => {
  visible.value = false;
}

const handleCancel = () => {
  visible.value = false;
}

const showExploit = async (filename: string) => {
  const newFilename = filename.replace('report', 'exploit_report').replace('.csv', '.html');
  console.log(filename);
  try {
    const response = await axios.get(`/view_exploit_report/${newFilename}`);
    const htmlContent = response.data.html;
        
    const newWindow = window.open();
    newWindow.document.write(htmlContent);
    newWindow.document.close();
  } catch (error) {
    console.error('Error loading HTML:', error);
  }
}

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
const getAllReports = async () => {
  try {
    const response = await axios.get('/reports');

    fileSource.value = response.data;

    console.log('reports查询成功:', fileSource.value, '=======', response.data);
  } catch (error) {
    console.error('Failed to get ids', error);
  }
};
const addTaskIdsDataSource = (response, status): void => {
  // console.log("addMethod===============", fileSource.value)
  const filteredData = fileSource.value.find(item => item.filename.includes("12345"));
  console.log("find=============", filteredData)
const newEntries = response.data.task_ids.map((id: string) => {
  const foundItem = fileSource.value.find(item => item.filename.includes(id)) || { filename: 'null', size: '0 B' };

  return {
    pID: id,
    status: status,
    filename: foundItem.filename,
    size: foundItem.size
  };
});

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

const showReport = async (filename: string) => {
  try{
    // const response = await axios.get(`/download/${filename}`);
    // console.log(`下载成功： ${response.data}`);
    const response = await axios.get(`/get_result/${filename}`)

    resultTableData.value = response.data;

    visible.value = true;

  }catch (error){
    console.error("Failed to get report:", error);
  }
}

const downloadReport = async (filename: string) => {
  try{
    // const response = await axios.get(`/download/${filename}`);
    // console.log(`下载成功： ${response.data}`);
    const response = await axios({
      url: `/download/${filename}`,
      method: 'GET',
      responseType: 'blob',  // 设置 responseType 为 blob 来接收文件数据
    });

    // 创建一个URL链接并用于创建一个下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename); // 设置下载文件名
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(url);  // 清理 blob URL

    console.log(`下载成功：文件已触发下载`);
  }catch (error){
    console.error("Failed to terminate task:", error);
  }
}
const goToWorkplace = () =>{
  router.push('/workplace');
}

onMounted(async() => {
  await getAllReports();
  await getAllTaskInfo();
  await getTerminatedTaskInfo();
  await getSuccessTaskInfo();
  await getFailedTaskInfo();
});
</script>

<style lang="less" scoped>

.full-modal {
    .ant-modal {
      max-width: 100%;
      top: 0;
      padding-bottom: 0;
      margin: 0;
    }
    .ant-modal-content {
      display: flex;
      flex-direction: column;
      height: calc(100vh);
    }
    .ant-modal-body {
      flex: 1;
    }
}

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
