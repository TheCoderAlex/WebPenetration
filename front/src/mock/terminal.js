import Mock from 'mockjs';

Mock.mock('/api/terminal', 'post', (options) => {

  console.log('收到提交的数据：', options.body);
  return {
    terminalInfo: options.body
  }
});
