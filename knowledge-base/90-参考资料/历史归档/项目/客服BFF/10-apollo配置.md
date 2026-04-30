##### 一、apollo地址
[https://apollo-test-kefu.myscrm.cn](https://apollo-test-kefu.myscrm.cn/)

项目权限申请找SM



##### 二、查看apollo配置
![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1672910610612-ee0658bd-5c69-42e9-ba02-a640a1c67b16.png)



##### 三、新增配置
点击【**新增配置**】按钮，在输入新增配置的`key` 和 `value`。

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1672910651161-90d92328-24f6-4ee8-8a9b-ebcc81da712b.png)

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1672910668889-4726b143-15f7-4983-b66e-c04d4299a075.png)



##### 四、发布配置
点击【**发布**】按钮，`Release Name`使用默认值即可。

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1672910745539-3ce4194c-50f0-46bd-937e-98e313a6e766.png)

![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1672910758520-5d8e03f2-6aa7-48a6-8237-91b9fd799309.png)



##### 五、项目中使用apollo配置
使用`getApolloConfig`获取`apollo`配置。

```typescript
import { Service, getApolloConfig } from '@yunke/yunfly';
import axios from 'axios';
import { GetUserInfoResponse } from '../types/user.type';

@Service()
export default class UserService {
  async getUserInfo(token: string, orgCode: string): Promise<GetUserInfoResponse> {
    try {
      const apolloConfig = await getApolloConfig();
      const res = await axios.get(`${apolloConfig['SiteUrl.KfApiSite']}/${orgCode}/bk/common-api/user/get-info?token=${token}`);
      return res.data;
    } catch (err) {
      throw err;
    }
  }
}

```



