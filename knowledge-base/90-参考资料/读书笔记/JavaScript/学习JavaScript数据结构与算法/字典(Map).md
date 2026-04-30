### 一、散列算法
散列算法的作用是尽可能快地在数据结构种找到一个值.



代码参考下方实现的散列字典

```javascript
// 数据转化为字符串;
function defaultToString (item) {
	if (item == null) {
  	return 'NULL';
  } else if (item === undefined) {
  	return 'UNDEFINED';
  } else if (typeof item === 'string' || item instanceof String) {
  	return `${item}`;
  }
  return item.toString();
}

class ValuePair {
	constructor(key, value){
  	this.key = key;
    this.value = value;
  }
  toString() {
  	return `[#${this.key}: ${this.value}]`
  }
}

class HashTable {
	constructor(toStrFn = defaultToString) {
  	this.toStrFn = toStrFn;
    this.table = {};
  }
  // 将键转化为字串, 再取其ASCII值作为其存储地址
  loseloseHashCode(key) {
   	if (typeof key === 'number') {
    	return key;
    }
    const tableKey = this.toStrFn(key);
    
    let hash = 0;
    
    for (let i = 0;i < tableKey.length; i++) {
    	hash = tableKey.charCodeAt(i);
    }
    return hash % 37;
  }
  hashCode(key) {
  	return this.loseloseHashCode(key);
  }
  put(key, value) {
   	if (key != null && value != null) {
    	const position = this.hashCode(key);
      this.table[position] = new ValuePair(key, value);
      return true;
    }
    return false;
  }
 get(key) {
 	const valuePair = this.table[this.hashCode(key)];
  return valuePair == null ? undefined : valuePair.value;
 }
 remove(key) {
 	const hash = this.hashCode(key);
  const valuePair = this.talbe[hash];
  if (valuePair != null) {
   	delete this.table[hash];
    return true;
  }
  return false;
 }
}
  
```

##### 
#### 二、处理散列表中的冲突
##### 1、什么是处理散列表中的冲突
有时候, 一些键会有相同的散列值. 不同的值在散列表中对应相同的位置的时候, 我们称其为冲突.



##### 2、如何解决冲突
解决冲突有集中方法: 分离链接法、线性探查和双散列法.



**分离链接法:**

**为散列表的每一个位置创建一个链表, 并将元素存储在里面, 它是解决冲突的最简单方法, 但是在HashTable实例之外还需要额外的存储空间.**

**对于分离链接和线性查找, 只需要重新三个方法: put、get和remove.**

****

```javascript
class HashTableSeparateChaining {
	constructor(toStrFn = defaultToString) {
  	this.toStrFn = toStrFn;
    this.table = {};
  }
  put(key, value) {
  	if (key != null && value != null) {
    	const position = this.hashCode(key);
      if (this.table[position] == null) {
      	this.table[position] = new LinkedList();
      }
      this.table[position].push(new LinkedList(key, value));
      return true;      
    }
  }
}
```

