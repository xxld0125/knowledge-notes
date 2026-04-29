

```markdown

├── package.json
├── grpc-code-gen.config.js
├── grpc-service.dev.config.js
├── README.md
├── tsconfig.json  
├── Dockerfile
├── .gitignore
├── .gitlab-ci.yml
├── src
│    ├── config
│    │  └── config.default.ts
│    │  └── config.local.ts (可选)
│    │  └── config.test.ts  (可选)
│    │  └── config.release.ts (可选)
│    │  └── config.prod.ts (可选)
│    │  └── config.middleware.ts (可选)
│    ├── controller
│    │  └── MainController.ts
│    │  └── ProbeController.ts
│    │  └── UserController.ts
│    ├── middleware
│    │  └── ErrorMIddleware.ts
│    │  └── LogMIddleware.ts
│    ├── service
│    │  └── Example.ts
│    │  └── UserService.ts
│    ├── alone
│    │  └── alone1.ts
│    │  └── alone2.ts 
│    ├── schedule
│    │  └── task1.ts (一个文件即是一个定时任务)
│    │  └── task2.ts 
│    ├── socket
│    │  └── controller
│    │  │  └── MainController.ts
│    │  └── middleware
│    │  │  └── socketMiddleware.ts
│    ├── utils
│    │  └── util.ts
│    │  └── config.ts
│    ├── grpc-code-gen (grpc代码文件)
│    │  └── getGrpcClient.ts
│    │  └── grpcObj.ts
│    │  └── serviceWrapper.ts
│    │  └──yued (空间)
│    │  │  └── user (服务)
│    │  │  │  └── UserService.ts (grpc服务service)
│    │  │  └── types.ts
│    ├── plugin
│    │   └── yunfly-plugin-email
│    │       ├── src
│    │       │   ├── config
│    │       │   │   └── config.default.ts
│    │       │   └── app.ts
│    │       ├── .gitlab-ci.yml
│    │       ├── tsconfig.json
│    │       ├── README.md
│    │       └── package.json
│    └── app.ts
```

