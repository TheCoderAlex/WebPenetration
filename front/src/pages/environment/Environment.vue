<template>
<div class="workplace grid grid-rows-none gap-4 mt-xxs">
    <div class="card grid grid-cols-12 gap-6">
      <mini-statistic-card
        class="card col-span-12 mdx:col-span-6 xlx:col-span-3"
        v-for="(item, i) in statisticList"
        :key="i"
        :title="item.title"
        :value="item.value"
      >
        <template #icon>
          <component
            :class="`text-[96px] translate-x-[25%] translate-y-[25%] opacity-75 ${item.iconClass}`"
            v-bind:is="item.icon"
          />
        </template>
      </mini-statistic-card>
    </div>
</div>
</template>
<script lang="ts" setup>
import { reactive, ref, watch } from 'vue';
import type { FormInstance } from 'ant-design-vue';
import MiniStatisticCard from "@/components/statistic/MiniStatisticCard.vue";

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

  const statisticList = reactive([
    {
      title: '正在运行',
      value: '100',
      icon: 'dollar-circle-filled',
      iconClass: 'text-blue-100',
    },
    {
      title: '正在运行',
      value: '138',
      icon: 'usergroup-add-outlined',
      iconClass: 'text-purple-100',
    },
    {
      title: '正在运行',
      value: '5000',
      icon: 'heart-filled',
      iconClass: 'text-primary-100',
    },
    {
      title: '正在运行',
      value: '3200',
      icon: 'shopping-filled',
      iconClass: 'text-green-100',
    },
  ]);
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
  labelCol: { span: 8 },
  wrapperCol: { span: 10 },
};
const formTailLayout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 10, offset: 4 },
};
</script>

