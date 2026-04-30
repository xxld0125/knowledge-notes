主要是接入[云客前端规范](https://yued.myscrm.cn/standard-doc/#/)。



#### 一、BFF服务命名格式：
前缀：bff-（Backend For Frontend）

客服PC端bff服务（bff-kefu-customerservice）



#### 二、代码风格
eslint配置问题需要确认。

接入`prettier`。





#### 三、Commit规范
1. 具体规范内容参考：[云客commit规范](https://yued.myscrm.cn/standard-doc/#/docs/common/commit)



2. 接入项目：

云客BFF脚手架默认接入husky和lint-stage做commit-message校验。

补充`.commitlintrc.js`

```javascript
module.exports = {
  // 继承默认配置
  extends: ['@commitlint/config-angular'] // or ['@commitlint/config-conventional']
};

```



#### 四、命名规范
具体规范内容参考： [云客命名规范](https://yued.myscrm.cn/standard-doc/#/docs/common/naming)

接入`cspell`进行单词校验。



#### 五、ci规范
具体规范内容参考： [云客CI规范](https://yued.myscrm.cn/standard-doc/#/docs/npm/ci)



#### 六、单元测试规范
业务项目不接入单元测试。

