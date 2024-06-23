<template>
  <div class="terminal card workplace grid grid-rows-none gap-4 mt-xxs" v-bind="$attrs">
    <div class="terminal-header card flex-auto h-16">
      <div class="buttons">
        <span class="button red"></span>
        <span class="button yellow"></span>
        <span class="button green"></span>
      </div>
      <div class="title">Terminal</div>
    </div>
    <div class="terminal-body flex-auto break-all">
      <div class="pre font-bold" v-html="formattedTerminalInfo"></div>
    </div>
  </div>

  <div class="form-container workplace grid grid-rows-none gap-4 mt-xxs space-y-2">
    <a-form @submit.prevent="startTask">
      <overview-title title="params" subtitle="测试目标" />
      <hr />
      <a-form-item>
        <a-checkbox v-model:checked="options.s">Examine cloud service</a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="options.m">Analyze HTTP response for identify product/version using Machine Learning</a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="options.g">Google Custom Search for identify product/version:</a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="options.e">Explore default path of product</a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="options.c">Discover open ports and wrong ssl server certification using Censys</a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="options.p">Execute exploit module using Metasploit</a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="options.l">Analyze log based HTTP response for identify product/version</a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="options.i">Explore relevant FQDN with the target FQDN</a-checkbox>
      </a-form-item>
      <a-form-item>
        <a-checkbox v-model:checked="options.no_update_vulndb">--no-update-vulndb</a-checkbox>
      </a-form-item>

      <a-form-item>
        <a-button type="primary" html-type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold rounded">start</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import OverviewTitle from '@/components/statistic/OverviewTitle.vue';

axios.defaults.baseURL = '/api';
export default {
  inheritAttrs: false,
  components: { OverviewTitle },
  data() {
    const terminalInfo = ref('null');
    const loading = ref(true);
    const options = ref({
      s: false,
      m: false,
      g: false,
      e: false,
      c: false,
      p: false,
      l: false,
      i: false,
      no_update_vulndb: false
    });

    const startTask = async () => {
      try {
        const response = await axios.post('/start_task', options.value);
        const taskId = response.data.task_id;
        alert(`Task started with id: ${taskId}`);
        this.statusTaskId = taskId;
        await pollTaskStatus(taskId);
        console.log('提交成功:', response.data);
      } catch (error) {
        console.error('Failed to start task:', error);
        terminalInfo.value = 'Error fetching terminal information.';
      } finally {
        loading.value = false;
      }
    };

    const terminateTask = async () => {
      try {
        const response = await axios.post('/terminateTask', { task_id: this.terminateTaskId});
        alert(response.data.status);
      }catch (error){
        console.error('Failed to terminate task:', error);
      }
    }

    const getTaskStatus = async () => {
      try {
        const response = await axios.get(`/task_status/${this.statusTaskId}`);
        this.taskStatus = response.data;
        alert(response.data.status);
      }catch (error){
        console.error('Failed to get task status:', error);
      }
    }

    const pollTaskStatus = async (taskId) => {
      console.log(`polling.....: ${taskId}`);
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
      }

      this.pollingInterval = setInterval(async () => {
        try {
          const response = await axios.get(`/task_status/${taskId}/`);
          terminalInfo.value += response.data;
          // console.log("polling....." + response.data);
          if (response.data.includes('Task completed') || response.data.includes('Task terminated') || response.data.includes('Task is not running')) {
            clearInterval(this.pollingInterval);
          }
        }catch (error){
          console.log('Error polling task status: ', error);
          clearInterval(this.pollingInterval);
        }
      }, 1500);
    }

    const formattedTerminalInfo = computed(() => {
      return terminalInfo.value;
        // .split('\n')
        // .map((line, index) => `<span class="line-number">${index + 1}</span> ${line}`)
        // .join('\n');
    });

    return {
      parameters: {
        options
      },
      terminateTaskId: '',
      statusTaskId: '',
      taskStatus: '',
      pollingInterval: null,
      terminalInfo,
      loading,
      formattedTerminalInfo,
      startTask,
      options
    };

  },
};
</script>

<style scoped>
.terminal {
  background-color: #2d2d2d;
  color: #cccccc;
  font-family: 'Courier New', Courier, monospace;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  margin: 20px auto;
  width: calc(78%);
  height: 115vh;
  flex-direction: column;
}

.terminal-header {
  justify-content: space-between;
  align-items: center;
  background-color: #44475a;
  padding: 10px;
  color: #ffffff;
}

.buttons {
  display: flex;
  align-items: center;
}

.button {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
}

.red {
  background-color: #ff5f56;
}

.yellow {
  background-color: #ffbd2e;
}

.green {
  background-color: #27c93f;
}

.title {
  flex-grow: 1;
  text-align: center;
  font-weight: bold;
}

.terminal-body {
  height: calc(100%);
  padding: 10px;
  white-space: pre-wrap; /* 保持换行 */
  overflow-y: auto; /* 垂直滚动条 */
  flex-grow: 1;
}

.pre {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
}

.line-number {
  display: inline-block;
  width: 30px;
  color: #888888;
  user-select: none;
  margin-right: 10px;
}

.form-container {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: calc(18%);
  @apply justify-center items-center mt-md -mx-2;
}
</style>
