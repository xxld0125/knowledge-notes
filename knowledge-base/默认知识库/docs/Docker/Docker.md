#### 一、为什么基于 stream 的静态服务器拥有更高的性能
基于流（stream）的静态服务器拥有更高的性能，主要因为以下几个原因：

1.  减少内存占用： 基于流的服务器在处理请求时，将数据一块一块地读取，而不是把整个文件读入内存中，这样可以大大减少内存的占用，减少服务器的内存压力，提高服务器的性能。 
2.  提高响应速度： 基于流的服务器可以在读取数据时，边读边发送响应，而不是等待整个文件读取完毕后再发送响应，这样可以大大提高响应速度。 
3.  支持大文件处理： 基于流的服务器可以处理非常大的文件，因为它只需要一小块一小块地读取文件，而不是一次性将整个文件读入内存中。 
4.  支持多个并发请求： 基于流的服务器可以同时处理多个请求，因为它可以将每个请求都看作一次流式读取，而不是需要等待一个请求处理完毕后才能处理下一个请求。 



综上所述，基于流的静态服务器可以大大提高服务器的性能，特别是在处理大文件和并发请求时更加明显



#### 二、为什么基于 stream 后，serve 等静态资源服务器仍然会计算 Content-Length
即使基于流的静态资源服务器采用了分块传输（chunked transfer），也会在响应头部设置Content-Length字段。这是因为不是所有的客户端都支持分块传输，一些老版本的HTTP客户端可能无法理解分块传输的响应，并且Content-Length字段是HTTP/1.0协议中必需的字段之一，即使是HTTP/1.1中也建议包含Content-Length字段，以便于客户端可以准确地判断响应体的长度。

因此，即使采用了基于流的方式处理静态资源服务器的响应，也建议在响应头部设置Content-Length字段，以确保所有客户端都能够正确地解析响应。当然，如果客户端支持分块传输，服务器也可以通过设置Transfer-Encoding: chunked字段来告知客户端响应采用了分块传输的方式。



#### 三、继续完善静态服务器，使其基于 stream，并能给出正确的 Content-Length
要完善静态服务器，使其基于流并能正确地给出Content-Length，可以采取以下几个步骤：

1. 采用流式读取方式： 在服务器端使用流式读取方式，即在读取文件时，每次只读取一部分数据，然后立即发送响应。这样可以避免将整个文件读取到内存中，从而减少内存压力，并且能够边读边发送响应，提高响应速度。
2. 确定响应内容长度： 在服务器端确定响应内容的长度，包括响应头部和响应体的长度。在基于流的方式中，由于响应体是分块发送的，所以需要计算出每个块的长度，并将这些长度相加，以得到响应体的总长度。然后将响应头部中的Content-Length字段设置为响应体的总长度。
3. 采用分块传输编码： 在服务器端采用分块传输编码（chunked transfer encoding）方式传输响应体。这种方式可以让服务器在发送响应时，将响应体分成多个块进行发送，每个块都有一个头部，用于指定该块的长度。客户端在接收响应时，会按照块的长度进行接收和处理。这种方式可以避免在发送响应前确定响应体的长度，从而更加灵活。
4. 确定适当的块大小： 在采用分块传输编码方式时，需要确定适当的块大小。如果块的大小过小，会增加HTTP头部的开销；如果块的大小过大，会降低响应速度。一般来说，块的大小应该在1KB到4KB之间，可以根据实际情况进行调整。

综上所述，完善静态服务器可以采用流式读取、确定响应内容长度、采用分块传输编码、确定适当的块大小等技术手段，以实现更加高效、可靠、灵活的响应。



#### 四、继续完善静态服务器，使其作为一个命令行工具，支持指定端口号、读取目录、404、stream (甚至 trailingSlash、cleanUrls、rewrite、redirect 等)。可参考 serve-handler。
该静态服务器使用Node.js提供的http模块来创建服务器，通过监听请求的URL来读取对应的文件，返回对应的响应。静态文件的读取使用stream来进行，可以提升性能和响应速度。同时，该服务器支持trailingSlash、cleanUrls、rewrite和redirect等功能，可以根据实际需要进行配置。

```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const mime = require('mime');
const { promisify } = require('util');
const stat = promisify(fs.stat);

// trailingSlash选项表示是否自动添加斜杠，cleanUrls选项表示是否开启cleanUrls，rewriteRules选项表示rewrite规则，redirectRules选项表示redirect规则
function serve({ port, rootDir, trailingSlash, cleanUrls, rewriteRules, redirectRules }) {
  const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = decodeURIComponent(parsedUrl.pathname);

    // 拼接请求的文件路径
    const filePath = path.join(rootDir, pathname);

    try {
      // 检查文件是否存在
      await stat(filePath);
      // 如果请求的是一个目录，则自动添加斜杠
      if (trailingSlash && fs.statSync(filePath).isDirectory()) {
        res.writeHead(302, {
          Location: `${pathname}/${parsedUrl.search || ''}`,
        });
        res.end();
        return;
      }

      // 检查文件类型
      const contentType = mime.getType(filePath) || 'application/octet-stream';
      res.setHeader('Content-Type', contentType);

      // 如果开启了cleanUrls，且请求的是一个html文件，则自动去掉文件名后缀
      if (cleanUrls && contentType === 'text/html') {
        const parts = pathname.split('/');
        const lastPart = parts[parts.length - 1];
        const hasExtension = /\.[a-z]+$/i.test(lastPart);
        if (hasExtension) {
          const newUrl = `${pathname.replace(/\/$/, '')}/${lastPart.replace(/\.[a-z]+$/, '')}/`;
          res.writeHead(302, {
            Location: `${newUrl}${parsedUrl.search || ''}`,
          });
          res.end();
          return;
        }
      }

      // 如果存在rewrite规则，应用规则
      if (rewriteRules) {
        const rewrite = rewriteRules.find((rule) => rule.from.test(pathname));
        if (rewrite) {
          const newPathname = pathname.replace(rewrite.from, rewrite.to);
          const newUrl = `${newPathname}${parsedUrl.search || ''}`;
          req.url = newUrl;
          serveStaticFile(req, res, `${rootDir}${newPathname}`);
          return;
        }
      }

      // 如果存在redirect规则，应用规则
      if (redirectRules) {
        const redirect = redirectRules.find((rule) => rule.from === pathname);
        if (redirect) {
          res.writeHead(301, {
            Location: redirect.to,
          });
          res.end();
          return;
        }
      }

      // 返回文件内容
      serveStaticFile(req, res, filePath);
    } catch (err) {
      // 返回404
      res.writeHead(404, {
        'Content-Type': 'text/plain',
      });
      res.end('Not found');
    }
  });

  server.listen(port, () => {
    console.log(`Server listening on port ${port}`);
  });

  function serveStaticFile(req, res, filePath) {
    const stream = fs.createReadStream(filePath);
    let headersSent = false;
    // 如果文件读取出错，则返回500
    stream.on('error', (err) => {
      if (!headersSent) {
        headersSent = true;
        res.writeHead(500, {
          'Content-Type': 'text/plain',
        });
      	res.end('Internal Server Error');
      }
    });

    // 读取文件的chunk，并将其写入响应
    stream.on('data', (chunk) => {
      if (!headersSent) {
        headersSent = true;
        const contentLength = fs.statSync(filePath).size;
        res.writeHead(200, {
          'Content-Type': mime.getType(filePath) || 'application/octet-stream',
          'Content-Length': contentLength,
        });
      }
      res.write(chunk);
    });

    // 当文件读取结束时，结束响应
    stream.on('end', () => {
      res.end();
    });

  }
}

module.exports = serve;
```



#### 五、什么是 rewrite 和 redirect
Rewrite是一种在服务器端进行URL重写的技术，它通过修改客户端请求的URL，使得服务器能够正确地处理请求并返回正确的响应。Rewrite可以对URL进行很多种不同的操作，例如替换URL中的路径、添加查询参数、删除查询参数等等。Rewrite通常是在服务器端进行配置，可以使用Apache、Nginx等常见的Web服务器进行配置。

Redirect是一种在客户端进行URL重定向的技术，它通过将客户端请求的URL重定向到一个新的URL上，来实现请求的处理和响应。Redirect可以将客户端重定向到同一服务器上的不同URL，也可以将客户端重定向到其他服务器上的URL。Redirect通常是通过在服务器端设置响应头部的Location字段来实现的，客户端在收到这个响应后会根据Location字段的值进行重定向。

总的来说，Rewrite是一种更加灵活、功能更加强大的URL重写技术，它可以对URL进行很多种不同的操作。而Redirect则是一种更加直接、简单的URL重定向技术，它可以将客户端重定向到新的URL上。在实际应用中，Rewrite和Redirect经常被同时使用，来实现更加复杂的URL处理和重定向需求。



#### 六、为什么可以直接在 node 镜像中使用 yarn 命令行工具
在 Node 官方镜像中，预先安装了 Yarn 工具，因此可以直接在容器中使用 Yarn 命令行工具，无需再安装。

这是因为在 Node 官方 Dockerfile 中，已经包含了 Yarn 的安装指令。具体来说，在 Dockerfile 中会使用 curl 命令下载 Yarn 的安装脚本，然后运行该脚本安装 Yarn。因此，在使用 Node 镜像时，我们就可以直接使用 Yarn 命令行工具。



#### 七、docker-compose
Docker Compose 是 Docker 官方提供的用于定义和运行多容器 Docker 应用程序的工具。Docker Compose 使用 YAML 文件来配置应用程序的服务，并管理这些服务的运行、构建和停止。

使用 Docker Compose，可以通过一个命令快速启动多个容器，这些容器可以相互协作，以构建一个完整的应用程序。Docker Compose 可以管理容器的生命周期，包括创建、启动、停止和删除容器。此外，Docker Compose 还提供了一些高级功能，如服务发现、负载均衡、容器间的通信等。

Docker Compose 的核心概念是服务（Service）和项目（Project）。服务是一个容器的定义，包括镜像、容器名称、端口映射、环境变量等配置。项目则是由多个服务组成的应用程序，定义在一个 docker-compose.yml 文件中。

docker-compose.yml 文件是 YAML 格式的文本文件，用于描述应用程序中的服务和它们的配置。在这个文件中，可以定义多个服务，并指定它们的镜像、端口映射、环境变量、依赖关系等配置。在文件中定义完服务后，可以使用 Docker Compose 命令来创建、启动、停止和删除整个项目。



#### 八、为什么基础镜像 tag 总是携带 alpine
基础镜像 tag 中携带 alpine，通常指的是使用 Alpine Linux 作为基础镜像。Alpine Linux 是一款轻量级的 Linux 发行版，它的主要特点是体积小、安全性高和速度快。由于其体积小，基于 Alpine Linux 构建的 Docker 镜像也会更小，因此被广泛用于构建容器化应用。

在使用 Dockerfile 构建镜像时，可以选择不同的基础镜像，如 Ubuntu、Debian、CentOS、Alpine 等。选择哪种基础镜像，取决于应用程序的需求和依赖关系。

使用 Alpine Linux 作为基础镜像时，可以通过减少镜像中的无用文件和库，使得镜像的大小减小。因此，Alpine Linux 是构建轻量级容器的首选操作系统。

在基础镜像 tag 中携带 alpine 的好处是，可以很容易地区分不同的基础镜像。例如，node:14-alpine 表示使用 Node.js 14 版本的基础镜像，同时基于 Alpine Linux。这样的命名规范可以方便用户快速了解基础镜像的特点和版本信息。

####   
九、前端项目的构建缓存优化
主要分为两个阶段的优化

+ 构建时间优化：构建缓存

一个前端项目的耗时时间主要集中在两个命令：

    1. npm i (yarn)
    2. npm run build

在本地环境中，如果没有新的 npm package 需要下载，不需要重新 npm i。

在 Dockerfile 中，对于 ADD 指令来讲，如果添加文件内容的 checksum 没有发生变化，则可以利用构建缓存。

而对于前端项目而言，如果 package.json/yarn.lock 文件内容没有变更，则无需再次 npm i。

将 package.json/yarn.lock 事先置于镜像中，安装依赖将可以获得缓存的优化，优化如下。

```plain
FROM node:14-alpine as builder

WORKDIR /code

# 单独分离 package.json，是为了安装依赖可最大限度利用缓存
ADD package.json yarn.lock /code/
# 此时，yarn 可以利用缓存，如果 yarn.lock 内容没有变化，则不会重新依赖安装
RUN yarn

ADD . /code
RUN npm run build

CMD npx serve -s build
EXPOSE 3000
```

进行构建时，若可利用缓存，可看到 CACHED 标记。

```plain
$ docker-compose up --build
...
 => CACHED [builder 2/6] WORKDIR /code                                                                            0.0s
 => CACHED [builder 3/6] ADD package.json yarn.lock /code/                                                        0.0s
 => CACHED [builder 4/6] RUN yarn                                                                                 0.0s
...
```



+ 构建体积优化：多阶段构建

<font style="color:rgb(44, 62, 80);">我们的目标是提供静态服务（资源），完全</font>**<font style="color:rgb(44, 62, 80);">不</font>**<font style="color:rgb(44, 62, 80);">需要依赖于 node.js 环境进行服务化。node.js 环境在完成构建后即完成了它的使命，它的继续存在会造成极大的资源浪费。</font>

<font style="color:rgb(44, 62, 80);">我们可以使用多阶段构建进行优化，最终使用 nginx 进行服务化。</font>

1. <font style="color:rgb(44, 62, 80);">第一阶段 Node 镜像：使用 node 镜像对单页应用进行构建，生成静态资源。</font>
2. <font style="color:rgb(44, 62, 80);">第二阶段 Nginx 镜像：使用 nginx 镜像对单页应用的静态资源进行服务化。</font>



```plain
FROM node:14-alpine as builder

WORKDIR /code

# 单独分离 package.json，是为了安装依赖可最大限度利用缓存
ADD package.json yarn.lock /code/
RUN yarn

ADD . /code
RUN npm run build

# 选择更小体积的基础镜像
FROM nginx:alpine
COPY --from=builder code/build /usr/share/nginx/html
```



#### 十、为什么我们前端需要使用多阶段构建，多阶段构建还有什么场景
使用Docker的多阶段构建（multi-stage build）可以帮助我们减少Docker镜像的体积，提高构建速度和部署效率。具体来说，多阶段构建将一个完整的构建流程拆分为多个阶段，每个阶段都可以使用不同的基础镜像和构建命令，以便在最终的Docker镜像中只包含必要的组件和文件。

在前端开发中，使用多阶段构建可以带来以下好处：

1. 减少镜像体积：前端开发中，通常需要构建和打包多个静态资源文件，如HTML、CSS、JavaScript等。这些文件可以通过多阶段构建中的多个阶段进行处理，将生成的中间文件和不必要的依赖项在后续阶段中移除，从而减少最终Docker镜像的体积。
2. 提高构建速度：在前端开发中，构建过程可能会非常复杂，需要执行多个步骤和依赖项的安装。使用多阶段构建可以将构建过程拆分为多个阶段，每个阶段都可以复用之前的依赖项和中间文件，从而加快构建速度。
3. 简化部署过程：使用多阶段构建可以将生成的中间文件和最终的静态资源文件分离开来，使部署过程更加简化和可控。在部署时，可以只部署最终的静态资源文件，而不需要部署构建过程中的中间文件和依赖项。

除了前端开发之外，多阶段构建在其他场景中也具有重要作用。例如，在后端开发中，可以使用多阶段构建来拆分应用程序的构建和部署过程；在机器学习和数据科学领域，可以使用多阶段构建来处理数据和模型，并将生成的结果部署到生产环境中。总之，多阶段构建是一种非常实用和灵活的构建和部署工具，可以帮助我们更高效地开发和部署应用程序。



#### 十一：对比镜像体积优化前后的提示
优化前dockerfile

```plain
FROM node:14-alpine

WORKDIR /code

ADD . /code
RUN yarn && npm run build

CMD npx serve -s build
EXPOSE 3000
```

优化后dockerfile

```plain
FROM node:14-alpine as builder

WORKDIR /code

# 单独分离 package.json，是为了安装依赖可最大限度利用缓存
ADD package.json yarn.lock /code/
RUN yarn

ADD . /code
RUN npm run build

# 选择更小体积的基础镜像
FROM nginx:alpine
COPY --from=builder code/build /usr/share/nginx/html
```



优化前后镜像体积

|  | 体积 |
| --- | --- |
| 优化前 | 640MB |
| 优化后 | 41.6MB |


![](https://cdn.nlark.com/yuque/0/2023/png/25743026/1683707801346-c14309f5-f3aa-4632-bc35-f472f365b111.png)



#### 十二、为什么带有 hash 值的资源可设置为长期缓存
有hash值的资源可以设置为长期缓存，有以下几个原因：

1. 版本管理：带有hash值的资源可以唯一标识一个特定版本的资源，这意味着当我们更新应用程序时，每个版本的资源都会有不同的hash值，从而避免了浏览器缓存的问题。这样一来，我们可以轻松地管理应用程序的不同版本，而不会受到缓存问题的影响。
2. 强缓存：带有hash值的资源可以通过设置强缓存来提高网站的性能。强缓存是指在浏览器缓存中保存静态资源的副本，并在缓存期间不再向服务器请求资源。由于带有hash值的资源可以唯一标识一个特定版本的资源，因此在更新应用程序时，每个版本的资源都会有不同的hash值，从而使浏览器强制请求新的版本，从而避免了缓存问题。
3. 网络性能：带有hash值的资源可以提高网站的网络性能。因为每个版本的资源都有不同的hash值，所以如果我们只更新应用程序的部分资源，浏览器只会下载新版本的资源，而不会重新下载整个资源文件。这可以大大减少网络请求和传输的数据量，从而提高网站的性能和响应速度。

总之，带有hash值的资源可以帮助我们更好地管理应用程序的版本和静态资源，同时提高网站的性能和网络性能。因此，在前端项目中，我们通常会将带有hash值的资源设置为长期缓存。



### 参考：
+ [https://q.shanyue.tech/deploy](https://q.shanyue.tech/deploy/)

