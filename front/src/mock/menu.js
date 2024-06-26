import Mock from 'mockjs';

const presetList = [
  {
    id: 1,
    name: 'workplace',
    title: '工作台',
    icon: 'DashboardOutlined',
    badge: 'new',
    target: '_self',
    path: '/workplace',
    component: '@/pages/workplace',
    renderMenu: true,
    parent: null,
    permission: null,
    cacheable: true,
  },
  {
    id: 2,
    name: 'param',
    title: '参数配置',
    icon: 'SolutionOutlined',
    badge: '',
    target: '_self',
    path: '/param',
    component: '@/pages/param',
    renderMenu: true,
    parent: null,
    permission: null,
    cacheable: true,
  },
  {
    id: 3,
    name: 'environment',
    title: '环境测试',
    icon: 'SettingOutlined',
    badge: '',
    target: '_self',
    path: '/environment',
    component: '@/pages/environment',
    renderMenu: true,
    parent: null,
    permission: null,
    cacheable: true,
  },
  {
    id: 4,
    name: 'process',
    title: '进程管理',
    icon: 'SettingOutlined',
    badge: '',
    target: '_self',
    path: '/process',
    component: '@/pages/process',
    renderMenu: true,
    parent: null,
    permission: null,
    cacheable: true,
  },
  {
    id: 5,
    name: 'report',
    title: '结果管理',
    icon: 'SettingOutlined',
    badge: '',
    target: '_self',
    path: '/report',
    component: '@/pages/report',
    renderMenu: true,
    parent: null,
    permission: null,
    cacheable: true,
  },
];

function getMenuList() {
  // const menuStr = localStorage.getItem('stepin-menu');
  // const menuList = presetList;
  // if (!menuStr) {
  //   menuList = presetList;
  //   localStorage.setItem('stepin-menu', JSON.stringify(menuList));
  // } else {
  //   menuList = JSON.parse(menuStr);
  // }
  return presetList;
}

function saveMenu(menu) {
  const menuList = getMenuList();
  if (!menu.id) {
    menu.id = menuList.map((item) => item.id).reduce((p, c) => Math.max(p, parseInt(c)), 0) + 1;
  }
  const index = menuList.findIndex((item) => item.id === menu.id);
  if (index === -1) {
    menuList.push(menu);
  } else {
    menuList.splice(index, 1, menu);
  }
  localStorage.setItem('stepin-menu', JSON.stringify(menuList));
}

Mock.mock('api/menu', 'get', ({}) => {
  let menuList = getMenuList();
  const menuMap = menuList.reduce((p, c) => {
    p[c.name] = c;
    return p;
  }, {});
  menuList.forEach((menu) => {
    menu.renderMenu = !!menu.renderMenu;
    if (menu.parent) {
      const parent = menuMap[menu.parent];
      parent.children = parent.children ?? [];
      parent.children.push(menu);
    }
  });
  return {
    message: 'success',
    code: 0,
    data: menuList.filter((menu) => !menu.parent),
  };
});

Mock.mock('api/menu', 'put', ({ body }) => {
  const menu = JSON.parse(body);
  saveMenu(menu);
  return {
    code: 0,
    message: 'success',
  };
});

Mock.mock('api/menu', 'post', ({ body }) => {
  const menu = JSON.parse(body);
  saveMenu(menu);
  return {
    code: 0,
    message: 'success',
  };
});

Mock.mock('api/menu', 'delete', ({ body }) => {
  const id = body.get('id')[0];
  let menuList = getMenuList();
  const index = menuList.findIndex((menu) => menu.id === id);
  const [removed] = menuList.splice(index, 1);
  localStorage.setItem('stepin-menu', JSON.stringify(menuList));
  return {
    code: 0,
    message: 'success',
    data: removed,
  };
});
