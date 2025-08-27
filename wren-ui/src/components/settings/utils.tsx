import { SETTINGS } from '@/utils/enum';
import ProjectOutlined from '@ant-design/icons/ProjectOutlined';

export const getSettingMenu = (menu: SETTINGS) =>
  ({
    [SETTINGS.PROJECT]: {
      icon: ProjectOutlined,
      label: 'Project Settings',
    },
  })[menu] || null;
