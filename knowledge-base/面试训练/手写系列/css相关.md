# css相关

### 一、三角型
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        /* 等腰三角形 */
        #app {
            width: 0;
            height: 0;
            border-left: 50px solid transparent;
            border-right: 50px solid transparent;
            border-bottom: 100px solid red;
        }
        /* 直角三角形 */
        #app1 {
            width: 0;
            height: 0;
            border-left: 100px solid transparent;
            border-bottom: 100px solid red;
        }
    </style>
</head>

<body>
    
    <div id='app'></div>
    <div id='app1'></div>

</body>
</html>
```

### 
### 二、垂直水平局中
```html
<!--
 * @Author: 徐凌峰
 * @Date: 2021-03-03 22:17:41
 * @LastEditTime: 2021-03-04 23:03:14
 * @FilePath: \02-css\01-垂直水平居中.html
-->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        /* 
            写出五种方法：
            1、已知宽高；
            2、flex；
            3、未知宽高；
            4、table
            5、grid
         */
         
    </style>

</head>
<body>
    <div id='box'>
        <div id='child'></div>
    </div>
    <style>
        /* 方法一：flex */
        /* #box {
            height: 1000px;
            display: flex;
            justify-content: center;
            align-items: center;
            
        }
        #child {
            width: 100px;
            height: 100px;
            background-color: red;
        } */

        /* 方法二:absolute */
        /* #box {
            height: 1000px;
            width: 1000px;
            background-color: yellow;

            position: relative;
        }
        #child {
            width: 100px;
            height: 100px;
            background-color: red;

            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%,-50%);
        } */

        /* 方法三:table */
        /* #box {
            height: 1000px;
            width: 1000px;
            background-color: yellow;

            display:table-cell;
            vertical-align: middle;
            text-align: center;行内元素
        }
        #child {
            width: 100px;
            height: 100px;
            background-color: red;
            margin: 0 auto; 块级元素
        } */

        /* 方法四:grid */
        /* #box {
            height: 1000px;
            width: 1000px;
            background-color: yellow;

            display: grid;
            justify-content: center;
            align-items: center;
        }
        #child {
            width: 100px;
            height: 100px;
            background-color: red;
        } */

         /* 方法五:已知宽高 */
        /* #box {
            height: 1000px;
            width: 1000px;
            background-color: yellow;

            position: relative;
        }
        #child {
            width: 100px;
            height: 100px;
            background-color: red;

            position: absolute;
            top: 50%;
            left: 50%;
            margin: -50px 0 0 -50px;
        } */

        /* 方法六  */
        /* #box {
            height: 1000px;
            width: 1000px;
            background-color: yellow;

            position: relative;
        }
        #child {
            width: 100px;
            height: 100px;
            background-color: red;

            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            margin: auto;
        } */
    </style>
</body>
</html>

```
