<template>
  <div class="results card">
    <div class="flex items-baseline justify-between w-full">
      <overview-title title="运行结果" subtitle="基本信息" />
    </div>
    <div>
      <a-table :columns="columns" :dataSource="dataSource" :pagination="false">
        <template #bodyCell="{ text, record, column }">

          <!-- 自定义 progress 列 -->
          <div v-if="column.dataIndex === 'progress'">
            <div class="flex items-center">
              <a-radio-group>
                <a-radio-button @click="downloadReport(record.filename)">下载</a-radio-button>
              </a-radio-group>
            </div>
          </div>

          <!-- 其他列显示默认文本内容 -->
          <div v-else>
            {{ text }}
          </div>
        </template>
      </a-table>

<!--      <a-button size="large" class="add-btn" type="dashed" @click="goToWorkplace">-->
<!--        <template #icon>-->
<!--        </template>-->
<!--        添加新项目-->
<!--      </a-button>-->
    </div>
  </div>
</template>
<script lang="ts" setup>
import OverviewTitle from '@/components/statistic/OverviewTitle.vue';

import {computed, onMounted, reactive, ref} from "vue";
import axios from "axios";
import router from "@/router";


const columns = [
  { title: '文件名', dataIndex: 'filename' },
  { title: '创建时间', dataIndex: 'creation_date' },
  { title: '文件大小', dataIndex: 'size' },
  { title: '相关操作', dataIndex: 'progress' },
];
const dataSource = ref([]);

const getAllReports = async () => {
  try {
    const response = await axios.get('/reports');

    dataSource.value = response.data;

    console.log('reports查询成功:', dataSource.value, '=======', response.data);
  } catch (error) {
    console.error('Failed to get ids', error);
  }
};

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

onMounted(() => {
  getAllReports();
});
</script>

<style lang="less" scoped>
.results {
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
