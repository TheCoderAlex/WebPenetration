<template>
  <div class="form card grid grid-rows-none gap-4 mt-xxs ">
    <a-form ref="formRef" :model="formState" name="dynamic_rule" v-bind="formItemLayout">
      <a-form-item
        label="Username"
        name="username"
        :rules="[{ required: true, message: 'Please input your username!' }]"
      >
        <a-input v-model:value="formState.username" />
      </a-form-item>

      <a-form-item
        label="Nickname"
        name="nickname"
        :rules="[{ required: formState.checkNick, message: 'Please input your nickname!' }]"
      >
        <a-input v-model:value="formState.nickname" />
      </a-form-item>

      <a-form-item name="checkNick" v-bind="formTailLayout">
        <a-checkbox v-model:checked="formState.checkNick">Nickname is required</a-checkbox>
      </a-form-item>

      <a-form-item v-bind="formTailLayout">
        <a-button type="primary" @click="onCheck">Check</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>
<script lang="ts" setup>
import { reactive, ref, watch } from 'vue';
import type { FormInstance } from 'ant-design-vue';

interface FormState {
  username: string;
  nickname: string;
  checkNick: boolean;
}
const formRef = ref<FormInstance>();
const formState = reactive<FormState>({
  username: '',
  nickname: '',
  checkNick: false,
});
watch(
  () => formState.checkNick,
  () => {
    formRef.value.validateFields(['nickname']);
  },
  { flush: 'post' },
);
const onCheck = async () => {
  try {
    const values = await formRef.value.validateFields();
    console.log('Success:', values);
  } catch (errorInfo) {
    console.log('Failed:', errorInfo);
  }
};
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

