<template>
  <div class="form card grid grid-rows-none gap-4 mt-xxs ">
    <a-form ref="formRef" :model="formState" name="dynamic_rule" v-bind="formItemLayout">
      <template v-for="(value, key) in formState" :key="key">
        <a-form-item :label="key" :name="key">
          <a-input v-model:value="formState[key]" />
        </a-form-item>
      </template>
      <a-form-item v-bind="formTailLayout">
        <a-button type="primary" @click="onSubmit">Submit</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue';
import axios from 'axios';
import type { FormInstance } from 'ant-design-vue';

const formRef = ref<FormInstance>();
const formState = reactive<Record<string, string>>({});

// 获取当前配置
const fetchConfig = async () => {
  try {
    const response = await axios.get('/api/config');
    Object.assign(formState, response.data);
  } catch (error) {
    console.error('Failed to fetch config:', error);
  }
};

// 提交更新后的配置
const onSubmit = async () => {
  try {
    const formData = new URLSearchParams();
    for (const key in formState) {
      formData.append(key, formState[key]);
    }
    const response = await axios.post('/api/update', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    console.log('Update Success:', response.data);
  } catch (error) {
    console.error('Failed to update config:', error);
  }
};

// 在组件挂载时获取配置
onMounted(() => {
  fetchConfig();
});

const formItemLayout = {
  labelCol: { span: 4 },
  wrapperCol: { span: 8 },
};

const formTailLayout = {
  labelCol: { span: 4 },
  wrapperCol: { span: 8, offset: 4 },
};
</script>

<style>
.form {
  background-color: #fffffd;
  color: #333333; /* 修改字体颜色，使其在背景上更容易阅读 */
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  margin: 20px auto;
  max-width: calc(90%);
  height: calc(80%);
}
</style>
