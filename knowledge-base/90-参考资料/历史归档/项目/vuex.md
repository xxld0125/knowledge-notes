### 一、根据state自定生成对应的mutations
#### 1、处理规则
+ 非对像类型的属性直接生成赋值操作，对象类型属性会通过扩展运算符重新生成对象
+ 且会递归处理内部对象的属性，扁平化的生成 `updateXXX` 方法挂载到 `mutations` 对象上



根据 state 对象属性自动生成 mutations 更新属性的方法，现有一个state对象。

```javascript
state: {
  projectId: '',
    searchParams: {
    batchId: ''
  }
}
```



按照上面的规则处理后

```javascript
{
  updateProjectId: (state, payload) => { state.projectId = payLoad }
  updateSearchParams: (state, payload) => { state.searchParams = {...state.searchParams, ...payload} }
  updateBatchId: (state, payload) => { state.searchParams.batchId = payload }
}
```



#### 2、代码
```javascript
export function generateMutationsByState(stateTemplate) {
  const handleInnerObjState = (parentKeyPath, innerState, obj) => {
    Object.keys(innerState).forEach(key => {
      const value = innerState[key];
      const updateKey = `update${key[0].toUpperCase()}${key.substr(1)}`;
      if (typeof value === 'object' && value != null && !Array.isArray(value)) {
        obj[updateKey] = (state, payload) => {
          let target = state;
          for (let i = 0; i < parentKeyPath.length; i++) {
            target = target[parentKeyPath[i]];
          }
          target[key] = { ...target[key], ...payload };
        };
        handleInnerObjState([...parentKeyPath, key], value, obj);
      } else {
        obj[updateKey] = (state, payload) => {
          let target = state;
          for (let i = 0; i < parentKeyPath.length; i++) {
            target = target[parentKeyPath[i]];
          }
          target[key] = payload;
        };
      }
    });
  };
  const mutations = {};
  Object.keys(stateTemplate).forEach(key => {
    const obj = {};
    const value = stateTemplate[key];
    const updateKey = `update${key[0].toUpperCase()}${key.substr(1)}`;
    if (typeof value === 'object' && value != null && !Array.isArray(value)) {
      obj[updateKey] = (state, payload) => {
        state[key] = { ...state[key], ...payload };
      };
      handleInnerObjState([key], value, obj);
    } else {
      obj[updateKey] = (state, payload) => {
        state[key] = payload;
      };
    }
    Object.assign(mutations, obj);
  });
  return mutations;
}
```





