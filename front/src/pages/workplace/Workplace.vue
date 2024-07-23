<template>
  <div class="workplace grid grid-rows-none gap-4 mt-xxs">
    <div class="bg-container p-base rounded-b-lg rounded-tr-lg pt-8 flex items-center justify-start">
      <a-form ref="formRef" :model="formState" class="form-full">
        <a-form-item label="Target Hosts: " name="hosts_content" class="form-item">
          <a-textarea v-model:value="formState.hosts_content" placeholder="eg. http 192.168.1.1 8080 /" class="textarea-full" />
        </a-form-item>
        <a-form-item class="form-item">
          <a-button type="primary" @click="onSubmit">Save</a-button>
        </a-form-item>
      </a-form>

        <a-steps :current="progressId">
          <a-step title="准备" description="更新数据库" />
          <a-step title="分析" description="爬取并分析Web服务" />
          <a-step title="渗透" description="对Web服务进行攻击" />
        </a-steps>

    </div>

    <div class="bg-container p-base rounded-b-lg rounded-tr-lg pt-8 flex items-end justify-between">
      <TerminalInfo class="col-span-12 sm:col-span-12 md:col-span-10 lg:col-span-8 xl:col-span-6 xlx:col-span-7 xxlx:col-span-8 drop-shadow-sm"/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue';
import { useUnbounded } from '@/utils/useTheme';
import TerminalInfo from '@/components/terminal/terminalInfo.vue';
import { progressId } from '@/components/terminal/shared.js';
import axios from 'axios';

interface FormState {
  hosts_content: string;
}
const formRef = ref();
const formState = reactive<FormState>({
  hosts_content: '',
});

const loadHostsFile = async () => {
  try {
    const response = await axios.get('/get_hosts');
    formState.hosts_content = response.data;
  } catch (error) {
    console.error('Failed to load hosts file:', error);
  }
};

const saveHostsFile = async () => {
  try {
    await axios.post('/write_hosts', formState);
    console.log('Hosts file saved successfully');
  } catch (error) {
    console.error('Failed to save hosts file:', error);
  }
};

const onSubmit = () => {
  formRef.value.validate()
    .then(() => {
      saveHostsFile();
    })
    .catch(error => {
      console.log('Validation error:', error);
    });
};

const resetForm = () => {
  formRef.value.resetFields();
};

onMounted(() => {
  loadHostsFile();
});

useUnbounded();
</script>

<style scoped lang="less">
.workplace {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bg-container {
  display: flex;
  flex: 1;
  flex-direction: row;  /* 水平排列 */
  align-items: center;  /* 垂直居中 */
  justify-content: space-between;  /* 均匀分布 */
}

.form-full {
  display: flex;
  flex-direction: row;
  align-items: center;
  max-width: 800px;  /* 限制表单的最大宽度，使其在较大屏幕上不会过宽 */
  width: 100%;  /* 使表单在较小屏幕上占据全部宽度 */
  margin-right: 0.1rem;  /* 调整右边距以缩短与 h3 的距离 */
}

.form-item {
  flex: 1;
  margin-right: 1rem; /* 缩小表单项之间的间距 */
}

.textarea-full {
  width: 100%;
  resize: vertical; /* 可以根据需要设置是否允许用户调整文本区域的大小 */
}

a-form-item {
  display: flex;
  align-items: center;
}

</style>
