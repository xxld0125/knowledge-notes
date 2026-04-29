#### 一、`php`接口与`bff`接口对比
+ php

`[https://kf-api-test-kefu.myscrm.cn/retesting/bk/task/task/batch-assign](https://kf-api-test-kefu.myscrm.cn/retesting/bk/task/task/batch-assign)`



+ bff

`[https://gateway-test-kefu.myscrm.cn/bff-kefu-task-web/task-register/batch-assign](https://gateway-test-kefu.myscrm.cn/bff-kefu-task-web/task-register/batch-assign)`



**差异点：**

1. **域名**
    1. **php： **[https://kf-api-test-kefu.myscrm.cn](https://kf-api-test-kefu.myscrm.cn)
    2. **bff：**[https://gateway-test-kefu.myscrm.cn](https://gateway-test-kefu.myscrm.cn)
2. **拼接参数**
    1. **php：retesting(租户code)/bk**
    2. **bff：bff-kefu-task-web(bff应用名)**
3. **路由**
    1. **php：/task/task/batch-assign**
    2. **bff：/task-register/batch-assign**



**相同点：**

1. **请求参数。**
2. **返回结构（部分不合理或未使用到的数据，会考虑不返回，但不会影响现有业务场景）。**

****

#### 二、前端站点接入BFF要求
##### 1、支持租户级接入BFF
##### 2、支持单个接口接入BFF


#### 三、kffrontend接入改造点
##### 1、获取域名接口改造(config-multi/kf-frontend/get-init-data)
**动态域名获取接口增加bff服务域名配置**

各环境接口地址

```typescript
{
  dev: 'https://yk-common.dev.myyscm.com',
  test: 'https://yk-common-test-kefu.myscrm.cn',
  beta: 'https://yk-common.beta.myyscm.com',
  product: 'https://yk-common.myysq.com.cn'
}
```



示例: 增加后的接口结构：

```json
{
  "retesting": {
    "site_url": {
      "customer_service_site": "https://kefu-test-kefu.myscrm.cn",
      "kf_api_site": "https://kf-api-test-kefu.myscrm.cn",
      "kf_bff_site": "https://gateway-test-kefu.myscrm.cn"
    }
  },
  "standard_tenant_code": {
    "site_url": {
      "customer_service_site": "https://kefu-test-kefu.myscrm.cn",
      "kf_api_site": "https://kf-api-test-kefu.myscrm.cn",
      "kf_bff_site": "https://gateway-test-kefu.myscrm.cn"
    }
  }
}
```



##### 2、前端站点改造
要求：支持单个接口配置调用bff。



接口配置：

```javascript
export function fetchProblemClass(params) {
  return axiosCommon.$GET('engineer/get-problem-class', params, {
    useBffSite: 1,
    bffUrl: 'problem-class/get-problem-class'
  });
}
```



axios请求方法：

```javascript
function $GET(url, params = {}, config = {}) {
  let promise;
  if (getApiUrl()) {
    promise = Promise.resolve();
  } else {
    promise = setApiUrls();
  }

  return promise.then(() => {
    const { useKfApiSite, useBffSite, bffUrl } = config;
    if (useKfApiSite || useBffSite) {
      url = apiPath(url, { useKfApiSite, useBffSite, bffUrl });
      delete config.useKfApiSite;
      delete config.useBffSite;
      delete config.bffUrl;
    } else {
      url = apiPath(url);
    }

    return axiosInstance.get(url, { params: params, ...config });
  });
}
```



接口路径拼接方法：

```javascript

```





