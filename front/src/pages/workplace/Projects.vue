<template>
  <div class="projects card ">
    <div class="flex items-baseline justify-between w-full">
      <overview-title title="运行进程" subtitle="本月进度" />
      <div class="extra">
        <a-radio-group>
          <a-radio-button>全部</a-radio-button>
          <a-radio-button>在线</a-radio-button>
          <a-radio-button>商店</a-radio-button>
        </a-radio-group>
      </div>
    </div>
    <a-table :columns="columns" :dataSource="dataSource" :pagination="false">
      <template #bodyCell="{ record, text, column }">
        <template v-if="column.dataIndex === 'pname'">
          <div class="flex items-center">
            <span class="ml-sm">{{ text }}</span>
          </div>
        </template>
        <template v-if="column.dataIndex === 'param'">
          <div class="flex items-center">
            <span class="ml-sm">{{ text }}</span>
          </div>
        </template>
        <template v-else-if="column.dataIndex === 'progress'">
          <a-progress size="small" :percent="text * 100" :status="mapStatus(record.status, text)" />
        </template>
      </template>
    </a-table>
    <a-button size="large" class="add-btn" type="dashed">
      <template #icon>
        <upload-outlinzed />
      </template>
      添加新项目
    </a-button>
  </div>
</template>
<script lang="ts" setup>
  import OverviewTitle from '@/components/statistic/OverviewTitle.vue';
  import { formatThousand } from '@/utils/formatter';

  function mapStatus(status: string, progress: number) {
    switch (status) {
      case 'normal':
        return progress < 1 ? 'active' : 'success';
      case 'canceled':
        return 'exception';
      default:
        return 'normal';
    }
  }

  const columns = [
    { title: '进程名称', dataIndex: 'pname' },
    { title: '进程参数', dataIndex: 'param' },
    { title: '结果详情', dataIndex: 'result' },
    { title: '进度', dataIndex: 'progress' },
  ];

  const dataSource = [
    {
      pname: 'process1',
      param: ['-i', '-t', '-a'],
      result: 123,
      progress: 0.23,
    }
  ];
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
