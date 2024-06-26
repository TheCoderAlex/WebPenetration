<template>
  <a-config-provider :getPopupContainer="getPopupContainer">
    <ThemeProvider is-root v-bind="themeConfig" :apply-style="false">
      <stepin-view
        system-name="SEU Tool"
        logo-src="@/assets/logo/SEU-logo.svg"
        :class="`${contentClass}`"
        :navMode="navigation"
        :useTabs="useTabs"
        :themeList="themeList"
        :menuList="menuList"
        v-model:show-setting="showSetting"
        v-model:theme="theme"
        @themeSelect="configTheme"
      >
        <template #headerActions>
          <HeaderActions @showSetting="showSetting = true" />
        </template>
        <template #pageFooter>
          <PageFooter />
        </template>
        <template #themeEditorTab>
          <a-tab-pane tab="其它" key="other">
            <Setting />
          </a-tab-pane>
        </template>
      </stepin-view>
    </ThemeProvider>
  </a-config-provider>
</template>

<script lang="ts" setup>
  import { reactive, ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAccountStore, useMenuStore, useSettingStore, storeToRefs } from '@/store';
  import { PageFooter, HeaderActions } from '@/components/layout';
  import Setting from './components/setting';
  import { configTheme, themeList } from '@/theme';
  import { StepinView, ThemeProvider } from 'stepin';
  import { computed } from 'vue';

  console.log('App.vue: before profile fetch');


  const menuList = ref([
    { title: '工作台', path: '/workplace', meta: { icon: 'DashboardOutlined' } },
    { title: '环境测试', path: '/environment', meta: { icon: 'SettingOutlined' }, },
    { title: '参数配置', path: '/param', meta: { icon: 'SolutionOutlined' } },
    { title: '进程管理', path: '/process', meta: { icon: 'SmileOutlined' } },
    { title: '结果查看', path: '/report', meta: { icon: 'FormOutlined'} },
  ])


  const menuStore = useMenuStore();
  const startTime = performance.now();

  menuStore.getMenuList().then(() => {
    const endTime = performance.now();
    console.log(`Menu data fetch time: ${endTime - startTime} ms`);
  });


  const showSetting = ref(false);
  const router = useRouter();


  const { navigation, useTabs, theme, contentClass } = storeToRefs(useSettingStore());
  const themeConfig = computed(() => themeList.find((item) => item.key === theme.value)?.config ?? {});

  function getPopupContainer() {
    return document.querySelector('.stepin-layout');
  }
</script>

<style lang="less">
  .stepin-view {
    ::-webkit-scrollbar {
      width: 4px;
      height: 4px;
      border-radius: 4px;
      background-color: theme('colors.primary.500');
    }

    ::-webkit-scrollbar-thumb {
      border-radius: 4px;
      background-color: theme('colors.primary.400');

      &:hover {
        background-color: theme('colors.primary.500');
      }
    }

    ::-webkit-scrollbar-track {
      box-shadow: inset 0 0 1px rgba(0, 0, 0, 0);
      border-radius: 4px;
      background: theme('backgroundColor.layout');
    }
  }

  html {
    height: 100vh;
    overflow-y: hidden;
  }

  body {
    margin: 0;
    height: 100vh;
    overflow-y: hidden;
  }
  .stepin-img-checkbox {
    @apply transition-transform;
    &:hover {
      @apply scale-105 ~"-translate-y-[2px]";
    }
    img {
      @apply shadow-low rounded-md transition-transform;
    }
  }
</style>
