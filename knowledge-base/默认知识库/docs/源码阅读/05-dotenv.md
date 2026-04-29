### 一、作用
`<font style="color:rgb(37, 37, 37);">Dotenv</font>`<font style="color:rgb(37, 37, 37);"> 是一个零依赖模块，它将环境变量从 </font>`<font style="color:rgb(37, 37, 37);">.env</font>`<font style="color:rgb(37, 37, 37);"> 文件加载到 </font>`<font style="color:rgb(37, 37, 37);">process.env</font>`<font style="color:rgb(37, 37, 37);">。</font>

<font style="color:rgb(37, 37, 37);"></font>

<font style="color:rgb(37, 37, 37);">如果需要使用变量，则配合如下</font>[dotenv-expand](https://github.com/motdotla/dotenv-expand)<font style="color:rgb(37, 37, 37);">使用。</font>

### 二、.env文件
当我们的项目需要声明很多环境变量的时候，命令行声明的形式显然过于繁琐，而且难以管理。

`.env`文件允许我们将所有项目需要的环境变量放在一个单独的文件中，然后一并加载进`process.env`。

我们可以自己编写脚本去加载`.env`文件，不过更加简便和推荐的方式是使用[dotenv](https://link.juejin.cn?target=https%3A%2F%2Fwww.npmjs.com%2Fpackage%2Fdotenv)。

### 三、dotenv方法
#### 1、config
`<font style="color:rgb(37, 37, 37);">config</font>`<font style="color:rgb(37, 37, 37);"> 将读取您的 </font>`<font style="color:rgb(37, 37, 37);">.env</font>`<font style="color:rgb(37, 37, 37);"> 文件，解析内容，将其分配给 </font>`<font style="color:rgb(37, 37, 37);">process.env</font>`<font style="color:rgb(37, 37, 37);">，返回一个包含已加载内容的</font>`<font style="color:rgb(37, 37, 37);">parsed</font>`<font style="color:rgb(37, 37, 37);">key的对象，如果失败则返回一个</font>`<font style="color:rgb(37, 37, 37);">error</font>`<font style="color:rgb(37, 37, 37);">key。</font>

```javascript
const result = dontenv.config();

if (result.error) {
  throw result.error;
}

console.log(result.parsed);
```



<font style="color:rgb(37, 37, 37);">也可以将选项传递给配置， 具体见</font>[文档](https://github.com/motdotla/dotenv)。



#### 2、parse	
<font style="color:rgb(37, 37, 37);">可以使用解析包含环境变量的文件内容的引擎，它接受一个</font>`<font style="color:rgb(37, 37, 37);">String</font>`<font style="color:rgb(37, 37, 37);">或</font>`<font style="color:rgb(37, 37, 37);">Buffer</font>`<font style="color:rgb(37, 37, 37);">，并将返回一个带有解析的键和值的对象。</font>

```javascript
const dotenv = require('dotenv');

const buf = Buffer.from('BASIC=basic');

const config = dotenv.parse(buf); // 返回对象

console.log(typeof config, config); // object {	BASIC: basic };
```

<font style="color:rgb(37, 37, 37);"></font>

<font style="color:rgb(37, 37, 37);">也可以将选项传递给配置， 具体见</font>[文档](https://github.com/motdotla/dotenv)。



### 四、源码
`dotenv`代码中核心内容就是`config` 和 `parse`两个方法， 下面我们介绍这两个方法的实现逻辑。

#### 1、config
`config`方法的作用上面已经介绍了，就是<font style="color:rgb(37, 37, 37);">读取 </font>`<font style="color:rgb(37, 37, 37);">.env</font>`<font style="color:rgb(37, 37, 37);"> 文件，解析内容，将其分配给 </font>`<font style="color:rgb(37, 37, 37);">process.env</font>`<font style="color:rgb(37, 37, 37);">，并支持配置。</font>

<font style="color:rgb(37, 37, 37);">可配置项有：</font>

    - `<font style="color:rgb(37, 37, 37);">path</font>`<font style="color:rgb(37, 37, 37);">:		可指定</font>`<font style="color:rgb(37, 37, 37);">.env</font>`<font style="color:rgb(37, 37, 37);">文件的地址。</font>
    - `<font style="color:rgb(37, 37, 37);">encoding</font>`<font style="color:rgb(37, 37, 37);">:	可指定</font>`<font style="color:rgb(37, 37, 37);">.env</font>`<font style="color:rgb(37, 37, 37);">文件的编码格式。</font>
    - `<font style="color:rgb(37, 37, 37);">debug</font>`<font style="color:rgb(37, 37, 37);">:	可打开日志记录。</font>
    - `<font style="color:rgb(37, 37, 37);">override</font>`<font style="color:rgb(37, 37, 37);">:	可将</font>`<font style="color:rgb(37, 37, 37);">.env</font>`<font style="color:rgb(37, 37, 37);">文件上的变量覆盖</font>`<font style="color:rgb(37, 37, 37);">process.env</font>`<font style="color:rgb(37, 37, 37);">上的环境变量。</font>

<font style="color:rgb(37, 37, 37);"></font>

<font style="color:rgb(37, 37, 37);">首先初始化可配置项的默认值</font>

```typescript
function config() {
  // 默认.env路径, 与当前文件同级
  let dotenvPath = path.resolve(process.cwd(), '.env')
  
  // 默认编码格式
  let encoding = 'utf8'
  
  // 获取 debug 和 override 配置值
  const debug = Boolean(options && options.debug)
  const override = Boolean(options && options.override)
}
```



获取传入的配置配置值

```typescript
function config() {
  // ...
  
  // 获取 debug 和 override 配置值
  const debug = Boolean(options && options.debug)
  const override = Boolean(options && options.override)
  
  
  // 获取 path 和 encoding 配置值
  if (options) {
    if (options.path != null) {
      dotenvPath = _resolveHome(options.path)
    }
    if (options.encoding != null) {
      encoding = options.encoding
    }
  }
  
  // ...
}
```



这块就是`dotenv`库的核心逻辑， 通过`parse`方法将`.env`中的环境变量存储到对象中，并返回。再将`.env`文件中的环境变量逐个添加到`process.env`上。

```typescript
function config() {
  // ...
  try {
    // 指定编码返回string而不是buffer
    // 解析.env文件, 并返回一个对象
    const parsed = DotenvModule.parse(fs.readFileSync(dotenvPath, { encoding }))
    
    // 将.env文件中的环境变量添加到process.env上
    Object.keys(parsed).forEach(function (key) {
      // process.env上没有的变量, 直接绑定
      if (!Object.prototype.hasOwnProperty.call(process.env, key)) {
        process.env[key] = parsed[key]
      } else {
        // process.env上没有的变量, 判断override覆盖配置是否开启, 开启则覆盖process.env上的变量
        if (override === true) {
          process.env[key] = parsed[key]
        }
        
        // 判断debug配置是否开启, 开启则输出日志
        if (debug) {
          if (override === true) {
            _log(`"${key}" is already defined in \`process.env\` and WAS overwritten`)
          } else {
            _log(`"${key}" is already defined in \`process.env\` and was NOT overwritten`)
          }
        }
      }
    })

    return { parsed }
  } catch (e) {
    // 失败则返回错误信息
    if (debug) {
      _log(`Failed to load ${dotenvPath} ${e.message}`)
    }

    return { error: e }
  }
  // ...
}
```

<font style="color:rgb(37, 37, 37);"></font>

`<font style="color:rgb(37, 37, 37);">config</font>`<font style="color:rgb(37, 37, 37);">方法全部代码</font>

```javascript
function _log (message) {
  console.log(`[dotenv][DEBUG] ${message}`)
}

function _resolveHome (envPath) {
  return envPath[0] === '~' ? path.join(os.homedir(), envPath.slice(1)) : envPath
}

function config (options) {
  // 默认.env路径, 与当前文件同级
  let dotenvPath = path.resolve(process.cwd(), '.env')
  
  // 默认编码格式
  let encoding = 'utf8'
  
  // 获取 debug 和 override 配置值
  const debug = Boolean(options && options.debug)
  const override = Boolean(options && options.override)
  
  
  // 获取 path 和 encoding 配置值
  if (options) {
    if (options.path != null) {
      dotenvPath = _resolveHome(options.path)
    }
    if (options.encoding != null) {
      encoding = options.encoding
    }
  }

  try {
    // 指定编码返回string而不是buffer
    // 解析.env文件, 并返回一个对象
    const parsed = DotenvModule.parse(fs.readFileSync(dotenvPath, { encoding }))
    
    // 将.env文件中的环境变量添加到process.env上
    Object.keys(parsed).forEach(function (key) {
      // process.env上没有的变量, 直接绑定
      if (!Object.prototype.hasOwnProperty.call(process.env, key)) {
        process.env[key] = parsed[key]
      } else {
        // process.env上没有的变量, 判断override覆盖配置是否开启, 开启则覆盖process.env上的变量
        if (override === true) {
          process.env[key] = parsed[key]
        }
        
        // 判断debug配置是否开启, 开启则输出日志
        if (debug) {
          if (override === true) {
            _log(`"${key}" is already defined in \`process.env\` and WAS overwritten`)
          } else {
            _log(`"${key}" is already defined in \`process.env\` and was NOT overwritten`)
          }
        }
      }
    })

    return { parsed }
  } catch (e) {
    // 失败则返回错误信息
    if (debug) {
      _log(`Failed to load ${dotenvPath} ${e.message}`)
    }

    return { error: e }
  }
}
```



#### 2、parse
<font style="color:rgb(37, 37, 37);">将字符串解析为对象</font>

```javascript
const LINE = /(?:^|^)\s*(?:export\s+)?([\w.-]+)(?:\s*=\s*?|:\s+?)(\s*'(?:\\'|[^'])*'|\s*"(?:\\"|[^"])*"|\s*`(?:\\`|[^`])*`|[^#\r\n]+)?\s*(?:#.*)?(?:$|$)/mg

function parse (src) {
  const obj = {}

  // 将buffer转换为string
  let lines = src.toString()
  
  // 将换行符转换为相同的格式
  lines = lines.replace(/\r\n?/mg, '\n')

  let match
  while ((match = LINE.exec(lines)) != null) {
    const key = match[1]

    // 默认 undefined 或 null 为空字符串
    let value = (match[2] || '')

    // 删除空格
    value = value.trim()

    // 检查是否双引号
    const maybeQuote = value[0]

    // 删除引号
    value = value.replace(/^(['"`])([\s\S]*)\1$/mg, '$2')

    // 若有双引号，则展开换行符
    if (maybeQuote === '"') {
      value = value.replace(/\\n/g, '\n')
      value = value.replace(/\\r/g, '\r')
    }

    // 添加到对象
    obj[key] = value
  }

  return obj
}
```



### 五、总结
`dotenv`的原理，就是通过`fs.readFileSync`方法读取`.env`文件，再通过`parse`方法读取`.env`文件中的变量并存储到对象中， 最后再添加到`process.env`上。



### 参考
[https://github.com/motdotla/dotenv](https://github.com/motdotla/dotenv)

[https://juejin.cn/post/7045057475845816357](https://juejin.cn/post/7045057475845816357)

