<template>
  <div class="form card grid gap-10 mt-xxs">
    <a-form ref="formRef" :model="formState" name="dynamic_rule" v-bind="formItemLayout">
      <div class="" v-for="(items, category) in categorizedData" :key="category">
        <h1>{{ category }}</h1>
        <div v-for="(value, key) in categorizedData[category]" :key="key" class="p-4 rounded mb-4">
          <a-form-item :label="key" :name="key">
            <a-input v-model:value="formState[key]" />
          </a-form-item>
        </div>
        <hr/>
      </div>
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

axios.defaults.baseURL = '/api';

const formRef = ref<FormInstance>();
const formState = reactive<Record<string, string>>({});
const categorizedData = ref<Record<string, Record<string, string>>>({});

// 获取当前配置
const fetchConfig = async () => {
  try {
    const response = await axios.get('/config');
    const data = response.data;
    Object.assign(formState, data);

    //数据归类
    const categorized: Record<string, Record<string, string>> = {};
    for (const key in data){
      const category = key.split('_')[0];
      if (!categorized[category]){
        categorized[category] = {};
      }
      categorized[category][key] = data[key];
      // console.log(category + "=======" + data[key]);
    }
    categorizedData.value = categorized;
  } catch (error) {
    console.error('Failed to fetch config:', error);
  }
};

// 提交更新后的配置
const onSubmit = async () => {
  try {
    const formData = new URLSearchParams();
    for (const key in formState) {
      // console.log(key + " : " + formState[key]);
      formData.append(key, formState[key]);
    }

    const response = await axios.post('/update', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    if(response.status == 200){
      await fetchConfig();
    }
  } catch (error) {
    console.error('Failed to update config:', error);
  }
};

// 在组件挂载时获取配置
onMounted(() => {
  fetchConfig();
});

const formItemLayout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 10 },
};

const formTailLayout = {
  labelCol: { span: 15 },
  wrapperCol: { span: 10, offset: 4 },
};
</script>

<style>
.form {
  background-color: #fff;
  color: #333333; /* 修改字体颜色，使其在背景上更容易阅读 */
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  margin: 20px auto;
  max-width: calc(90%);
  height: calc(80%);
  display: grid;
  grid-template-columns: minmax(100px, 1fr);
}
</style>
