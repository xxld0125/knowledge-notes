### 一、作用
通过给`async await`的异步方法包裹一层`promise`来捕捉`error`， 来实现`async await`更简单的`error`处理。

### 二、源码
```typescript
/**
 * @param { Promise } promise
 * @param { Object= } errorExt - Additional Information you can pass to the err object
 * @return { Promise }
 */
export function to<T, U = Error> (
  promise: Promise<T>,
  errorExt?: object
): Promise<[U, undefined] | [null, T]> {
  return promise
    .then<[null, T]>((data: T) => [null, data])
    .catch<[U, undefined]>((err: U) => {
      if (errorExt) {
        const parsedError = Object.assign({}, err, errorExt);
        return [parsedError, undefined];
      }

      return [err, undefined];
    });
}

export default to;
```



### 三、js实现
```javascript
export function to (promise, errorExt) {
 return promise
  .then((data) => [null, data]);
  .catch((err) => {
    if (errorExt) {
      const parsedError = Object.assign({}, err, errorExt);
      return [parsedError, undefined];
    }
    return [err, undefined];
  })
}

export default to;
```



### 四、测试用例
```javascript
import { to } from '../src/await-to-js'

describe('Await to test', async () => {
  it('should return a value when resolved', async () => {
    const testInput = 41;
    const promise = Promise.resolve(testInput);

    const [err, data] = await to<number>(promise);

    expect(err).toBeNull();
    expect(data).toEqual(testInput);
  });

  it('should return an error when promise is rejected', async () => {
    const testInput = 41;
    const promise = Promise.reject('Error');

    const [err, data] = await to<number>(promise);

    expect(err).toEqual('Error');
    expect(data).toBeUndefined();
  });

  it('should add external properties to the error object', async () => {
    const promise = Promise.reject({ error: 'Error message' });

    const [err] = await to<
      string,
      { error: string; extraKey: number }
    >(promise, {
      extraKey: 1
    });

    expect(err).toBeTruthy();
    expect((err as any).extraKey).toEqual(1);
    expect((err as any).error).toEqual('Error message')
  });

  it('should receive the type of the parent if no type was passed', async () => {
    let user: { name: string };
    let err: Error;

    [err, user] = await to(Promise.resolve({ name: '123' }));

    expect(user.name).toEqual('123');
  });
});

```



### 参考资料
+ [https://github.com/scopsy/await-to-js](https://github.com/scopsy/await-to-js)
+ [https://blog.grossman.io/how-to-write-async-await-without-try-catch-blocks-in-javascript/](https://blog.grossman.io/how-to-write-async-await-without-try-catch-blocks-in-javascript/)



