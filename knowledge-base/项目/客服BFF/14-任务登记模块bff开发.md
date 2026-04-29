#### 一、接口梳理
##### 1、公共接口
| **接口** | **功能描述** | **结论** | **完成情况** |
| --- | --- | --- | :---: |
| config-multi/kf-frontend/get-init-data | 获取动态域名 | 使用现接口 | |
| common-api/access/base-info | 获取登录账户信息、功能权限点、菜单列表 | 使用现接口 | |
| kf-api/common-api/common/config-list | 获取公共的一些配置项（灰开、页面配置开关、参数设置、配置设置等） | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/setting_config.SettingProcessFlowService.getList](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/setting_config.SettingProcessFlowService.getList) | |
| common-api/common/get-third-system-entrances | 获取多系统列表 | 使用原接口 | |
| common-api/user/get-info | 获取登录账号信息 | 使用原接口 | |
| common-api/common/get-guid | 获取guid方法 | 使用新的go服务登记接口，批量登记不需要上传uuid | |
| basic/sso-site/get-backend-site | 获取旧前端站点域名 | 使用原接口 | |
| common-api/common/get-service-config | 获取服务器配置-时间 | 使用原接口/bff层处理，返回时间 | |
| common-api/sts/document-sts-config | 获取oss配置 | 使用原接口 | |
| common-api/organization/search-by-proj-auth | 根据用户授权及应用授权，获取满足要求的所有项目列表，再反查出对应的公司数据（返回结构：树形） | 公共组接口，暂未提供，先用老的 | |
| common-api/project/list-by-corp-id | 根据`corp_id`获取项目列表 | 公共组接口，暂未提供，先用老的 | |
| common-api/building-unit/list | 根据`proj_id`获取楼栋单元列表， 支持搜索 | 公共组接口，暂未提供，先用老的 | |
| common-api/room/list | 根据`buildingId` & `unit`获取房间列表，支持搜索 | 公共组接口，暂未提供，先用老的 | |
|  |  |  | |




##### 2、参数设置
| **接口** | **功能描述** | **结论** | **请求参数** | **完成情况** |
| --- | --- | --- | --- | --- |
| parameter-api/repairs-duration/get-edit-status | 获取是否可以编辑任务处理时限状态 | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/parameter.ParameterService.getOne](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/parameter.ParameterService.getOne)<br/> | code=task_deadline_can_edit_status（php取的是title字段） |  |
| dailyservice-sso/engineer/get-function-push | 获取参数设置开关-task_deadline_flag（获取任务处理时限规则开关） | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/function_publish.FunctionPublishService.GetByCode](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/function_publish.FunctionPublishService.GetByCode) | code=task_deadline_flag |  |
| parameter-api/list-params/list | 获取参数设置开关-default_acceptor_settings(获取默认自己为受理人开关) | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/parameter.ParameterService.getOne](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/parameter.ParameterService.getOne) | code=default_acceptor_settings |  |
| parameter-api/promise-deadline/default-promise-deadline | 查询公司对应的默认任务回复时限设置（参数设置-<font style="color:rgb(34, 34, 34);">答复客户时限设置</font>） | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/deadline.DeadlineService.GetReplyPromiseDeadline](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/deadline.DeadlineService.GetReplyPromiseDeadline) |  |  |
| common-api/common/get-config-setting | 获取设置-isShowChoiceProblemClassEnd（问题分类是否需要选至末级） | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/setting_config.SettingProcessFlowService.getOne](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/setting_config.SettingProcessFlowService.getOne) | code=isShowChoiceProblemClassEnd |  |




##### 3、登记模块
| **接口** | **功能描述** | **结论** | **请求参数** | **完成情况** |
| --- | --- | --- | --- | :---: |
| task/task/get-init-data | 获取数据源（业务环节、投诉级别、问题部位、维修工期、请求来源、紧急程度等） | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/parameter.ParameterService.getOne](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/parameter.ParameterService.getOne) | code=business_step | |
| | | | code=complaint_level | |
| | | | code=problem_position | |
| | | | code=repairs_duration | |
| | | | code=task_urgency | |
| | | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/request_source.RequestSourceService.GetRequestSource](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/request_source.RequestSourceService.GetRequestSource) | 请求来源 | |
| task/task/base-info | 获取工单信息-400回填场景 | 待补充 |  | |
| tasks/get-default-task-operator | 查询房间对应的受理人 | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/operator.OperatorService.getAcceptOperatorList](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/operator.OperatorService.getAcceptOperatorList) |  | |
| task/task/get-next-operator | 查询房间对应的后续处理人 | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/operator.NextOperatorService.getNextAcceptOperatorList](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/operator.NextOperatorService.getNextAcceptOperatorList) |  | |
| tasks/get-guarantee-type | 查询房间对应的保修范围 | 待补充 |  | |
| dailyservice-sso/task-register/get-default-requester | 查询房间对应的请求人 | 公共组接口，暂未提供，先用老的 |  | |
| dailyservice-sso/task/get-assign-over-time-value | 查询任务指派时限（参数设置-<font style="color:rgb(34, 34, 34);">任务指派时限</font>） | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/deadline.DeadlineService.GetAssignDeadline](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/deadline.DeadlineService.GetAssignDeadline) |  | |
| engineer/get-problem-class | 获取问题分类 | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/problem_class.ProblemClassService.GetList](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/problem_class.ProblemClassService.GetList) |  | |
| dailyservice-sso/engineer/list-problem-with-group | 获取问题描述 | 待补充 |  | |
| task/task/get-accept-operator | 获取受理人列表 | [https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/operator.OperatorService.getAcceptOperatorList](https://api.myscrm.cn/project/17029/interface/api/f-20221130-task-core-setting/operator.OperatorService.getAcceptOperatorList) |  | |
| parameter/problem-lib/get-problem-ascription | 获取问题分类关联的任务归属 | 待补充 |  | |
| task/task/search-subject | 获取历史记录工单 | 待补充 |  | |
| ember-archives/member-assess/list | 获取评价详情 | [https://api.myscrm.cn/project/17144/interface/api/f-20221125-task-core-init/kefu_task_core_proto.MemberService.GetTagLogList](https://api.myscrm.cn/project/17144/interface/api/f-20221125-task-core-init/kefu_task_core_proto.MemberService.GetTagLogList) |  | |
| task/task/batch-save | 暂存接口 | [https://api.myscrm.cn/project/17144/interface/api/f-20221125-task-core-init/kefu_task_core_proto.TaskService.Create](https://api.myscrm.cn/project/17144/interface/api/f-20221125-task-core-init/kefu_task_core_proto.TaskService.Create) |  | |
| dailyservice/task-approve/check-task-approve | 校验任务异常审批 | 待补充 |  | |
| task/task/batch-assign | 提交接口 | [https://api.myscrm.cn/project/17144/interface/api/f-20221125-task-core-init/kefu_task_core_proto.TaskService.Create](https://api.myscrm.cn/project/17144/interface/api/f-20221125-task-core-init/kefu_task_core_proto.TaskService.Create) |  | |
| 暂无场景 | 获取请求人标签列表 | [https://api.myscrm.cn/project/17144/interface/api/f-20221125-task-core-init/kefu_task_core_proto.MemberService.GetTagByIds](https://api.myscrm.cn/project/17144/interface/api/f-20221125-task-core-init/kefu_task_core_proto.MemberService.GetTagByIds) |  | |


