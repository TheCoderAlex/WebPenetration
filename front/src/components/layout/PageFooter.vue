<script lang="ts" setup></script>
<template>
  <div class="page-footer">
    <div class="links">
      <a class="link" href="https://www.seu.edu.cn" target="_blank"> 东南大学官网 </a>
    </div>
    <div class="copyright">
      Copyright
      <CopyrightOutlined class="icon-copyright" /> 2024 SEU 东南大学
    </div>
  </div>
</template>

<style scoped lang="less">
  .page-footer {
    text-align: center;
    @apply text-gray-400;

    .links {
      display: flex;
      justify-content: center;

      .link {
        @apply hover:text-gray-400 pl-4 pr-4;
      }
    }

    .copyright {
      margin-top: 8px;

      .icon-copyright {
        margin: 0;
      }
    }
  }
</style>
