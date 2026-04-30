# validate-npm-package-name源码阅读学习


#### 一、介绍


_**<u>Give me a string and I'll tell you if it's a valid </u>**_`_**<u>npm</u>**_`_**<u> package name.</u>**_



**<u>This package exports a single synchronous function that takes a </u>**`**<u>string</u>**`**<u> as input and returns an object with two properties:</u>**



即校验npm package 名称是否有效,并导出一个同步函数,接受一个字符串作为输入并返回一个具有两个属性的对象:



+ `validForNewPackages` :: `Boolean`
+ `validForOldPackages` :: `Boolean`



#### 二、npm package 命名规则


Below is a list of rules that valid `npm` package name should conform to.



以下是有效的 npm 包名称应符合的规则列表。



+  package name length should be greater than zero  
包名长度应大于零 
+  all the characters in the package name must be lowercase i.e., no uppercase or mixed case names are allowed  
包名中的所有字符都必须是小写，即不允许大写或混合大小写的名称 
+  package name _can_ consist of hyphens  
包名可以由连字符组成 
+  package name must _not_ contain any non-url-safe characters (since name ends up being part of a URL)  
包名不得包含任何非 url 安全字符（因为名称最终成为 URL 的一部分） 
+  package name should not start with `.` or `_`  
包名不应以 . 或者 _为开头 
+  package name should _not_ contain any leading or trailing spaces  
包名首尾不应包含空格 
+  package name should _not_ contain any of the following characters: `~)('!*`  
包名不应包含以下任何字符：~)('!* 
+  package name cannot be the same as a node.js/io.js core module nor a reserved/blacklisted name. For example, the following names are invalid:  
包名称不能与 node.js/io.js 核心模块相同，也不能与保留/黑名单名称相同。 例如，以下名称无效： 
    - http
    - stream
    - node_modules
    - favicon.ico
+  package name length cannot exceed 214  
包名长度不能超过214 



#### 三、源码阅读


```javascript
'use strict'

var scopedPackagePattern = new RegExp('^(?:@([^/]+?)[/])?([^/]+?)$')

// builtins:包括node内置 module列表
var builtins = require('builtins')

// 定义的黑名单列表
var blacklist = [
  'node_modules',
  'favicon.ico'
]

/**
 * @ params name 传入的包名
 */
var validate = module.exports = function (name) {
  var warnings = [] // 警告列表
  var errors = [] // 错误列表
	
  // 包名不能为null
  if (name === null) {
    errors.push('name cannot be null')
    return done(warnings, errors)
  }
	
  // 包名不能为undefined
  if (name === undefined) {
    errors.push('name cannot be undefined')
    return done(warnings, errors)
  }
	
  // 包名必须为String类型
  if (typeof name !== 'string') {
    errors.push('name must be a string')
    return done(warnings, errors)
  }
	
  // 包名长度必须大于0
  if (!name.length) {
    errors.push('name length must be greater than zero')
  }
	
  // 包名不能以'.'开头
  if (name.match(/^\./)) {
    errors.push('name cannot start with a period')
  }
	
  // 包名不能以'_'开头
  if (name.match(/^_/)) {
    errors.push('name cannot start with an underscore')
  }
	
  // 包名首位不能有空格
  if (name.trim() !== name) {
    errors.push('name cannot contain leading or trailing spaces')
  }
	
  // 包名不能在黑名单中
  blacklist.forEach(function (blacklistedName) {
    if (name.toLowerCase() === blacklistedName) {
      errors.push(blacklistedName + ' is a blacklisted name')
    }
  })

	// 包名不应为node 内置module名
  builtins.forEach(function (builtin) {
    if (name.toLowerCase() === builtin) {
      warnings.push(builtin + ' is a core module name')
    }
  })

	// 包名长度不应超过214
  if (name.length > 214) {
    warnings.push('name can no longer contain more than 214 characters')
  }

	// 包名应为小写  
  if (name.toLowerCase() !== name) {
    warnings.push('name can no longer contain capital letters')
  }
	
  // 包包名不应包含以下特殊字符: ~\'!()*
  if (/[~'!()*]/.test(name.split('/').slice(-1)[0])) {
    warnings.push('name can no longer contain special characters ("~\'!()*")')
  }
	
  // 包名不能包含non-url-safe字符
  if (encodeURIComponent(name) !== name) {
    // Maybe it's a scoped package name, like @user/package
    // 处理 scope package name
    var nameMatch = name.match(scopedPackagePattern)
    if (nameMatch) {
      var user = nameMatch[1]
      var pkg = nameMatch[2]
      // 包名不应包含encodeURIComponent会转义的字符;
      // encodeURIComponent不转义字符:A-Z a-z 0-9 - _ . ! ~ * ' ( )
      if (encodeURIComponent(user) === user && encodeURIComponent(pkg) === pkg) {
        return done(warnings, errors)
      }
    }

    errors.push('name can only contain URL-friendly characters')
  }

  return done(warnings, errors)
}

validate.scopedPackagePattern = scopedPackagePattern

// 返回处理结果
var done = function (warnings, errors) {
  var result = {
    // 不能有错误和警告信息
    validForNewPackages: errors.length === 0 && warnings.length === 0,
    // 不能有错误,可以有警告信息
    validForOldPackages: errors.length === 0,
    warnings: warnings,
    errors: errors
  }
  if (!result.warnings.length) delete result.warnings
  if (!result.errors.length) delete result.errors
  return result
}
```



<font style="color:rgb(184, 191, 198);">正则可视化: '^(?:@([^/]+?)[/])?([^/]+?)$'</font>



![](https://cdn.nlark.com/yuque/0/2022/png/25743026/1641104833457-11ed5271-2255-466f-8f10-41c172b9ab9c.png)



依赖的builtins模块:



```javascript
'use strict'

var semver = require('semver')

module.exports = function (version) {
  // 获取node版本
  version = version || process.version

  var coreModules = [
    'assert',
    'buffer',
    'child_process',
    'cluster',
    'console',
    'constants',
    'crypto',
    'dgram',
    'dns',
    'domain',
    'events',
    'fs',
    'http',
    'https',
    'module',
    'net',
    'os',
    'path',
    'punycode',
    'querystring',
    'readline',
    'repl',
    'stream',
    'string_decoder',
    'sys',
    'timers',
    'tls',
    'tty',
    'url',
    'util',
    'vm',
    'zlib'
  ]

  if (semver.lt(version, '6.0.0')) coreModules.push('freelist')
  if (semver.gte(version, '1.0.0')) coreModules.push('v8')
  if (semver.gte(version, '1.1.0')) coreModules.push('process')
  if (semver.gte(version, '8.1.0')) coreModules.push('async_hooks')
  if (semver.gte(version, '8.4.0')) coreModules.push('http2')
  if (semver.gte(version, '8.5.0')) coreModules.push('perf_hooks')

  return coreModules
}
```



#### 四、使用场景


+  vue: vue create project-name  

```javascript
// ~/packages/@vue/cli/lib/create.js
const validateProjectName = require('validate-npm-package-name');

const result = validateProjectName(name)
  if (!result.validForNewPackages) {
    console.error(chalk.red(`Invalid project name: "${name}"`))
    result.errors && result.errors.forEach(err => {
      console.error(chalk.red.dim('Error: ' + err))
    })
    result.warnings && result.warnings.forEach(warn => {
      console.error(chalk.red.dim('Warning: ' + warn))
    })
    exit(1)
  }
```

+  react: create-react-app  

```javascript
// ~/packages/create-react-app/createReactApp.js
const validateProjectName = require('validate-npm-package-name');

function checkAppName(appName) {
  const validationResult = validateProjectName(appName);
  if (!validationResult.validForNewPackages) {
    console.error(
      chalk.red(
        `Cannot create a project named ${chalk.green(
          `"${appName}"`
        )} because of npm naming restrictions:\n`
      )
    );
    [
      ...(validationResult.errors || []),
      ...(validationResult.warnings || []),
    ].forEach(error => {
      console.error(chalk.red(`  * ${error}`));
    });
    console.error(chalk.red('\nPlease choose a different project name.'));
    process.exit(1);
  }
}
```

+  ... 



#### 五、npm scope介绍


1.  介绍  
所有的npm packages都有一个名字。一些 packages 名字也会有一个 scope , scope将相当于npm模块的命名空间.scope packages 命名既要遵循普通 package 命名规则，也要遵守scope packages 的命名规则,使用时要以 @ 符开头，后面跟 / ，例：   
npm-scope 是一种将一些互相有关联的包组合在一起的方式，同时 npm 处理这些 packages 的方式也不同。因此，npm-scope 是一些组织发布官方 packages 最好的方式。 

```plain
@scopename/packagename
```

2.  安装scoped packages  
scoped packages 会被安装到二级文件夹中，例如，某个 Unscoped packages 被安装至 node_modules/packagename ，scoped packages 则会被安装至 node_modules/@myorg/packagename 。[@myorg ](/myorg ) 是个文件夹，可以包含任意数量的 scoped packages 。   

```json
npm install @myorg/packagename

// package.json 
"dependencies": {
  "@myorg/mypackage": "^1.3.0"
}
```

3.  引入scoped packages  
由于 scoped packages 被安装在一个 scope 文件夹中，所以你在代码中引用它时，需要包含 scope 的名字  

```plain
require('@/myorg/mypackage');
```

