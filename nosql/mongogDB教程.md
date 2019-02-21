# mongogDB教程

1. 下载`mongo`

   ```shell
   docker pull mongo
   ```

2. 启动`mongo`

   ```shell
   docker run --name mongo \
   -e MONGO_INITDB_ROOT_USERNAME=mongo \              # 设置root账户
   -e MONGO_INITDB_ROOT_PASSWORD=mongo  \			   # 设置root账户的密码
   -v .../mongo/data:/data/db \	   				   # 数据存储放在本地
   -d mongo
   ```

3. 基本命令

   ```shell
   db.runCommand({"ping": 1}) # 查看数据库是否连接成功
   db.runCommand({"buildInfo":1})  # 显示数据库的基本信息
   show dbs # 查看数据库信息
   use admin # 进入某一个数据库
   
   show collections # 显示该库有哪些集合
   db # 查看当前位于哪个数据库
   db.mongo.stats() # 查看集合信息
   
   db.runCommand({"collStats": "<collection>"}) # 查看集合的具体信息
   
   use mongo # 创建mongo数据库(如果mongo数据库已开始不存在)
   db.mongo.insert({"name": "mongo","age": 20}) # 插入一条数据
   # 批量插入数据
   db.mongo.insert([{"name": "mongo","age": 20, "score": {"chinese": 90, "math": 100}}, {"name": "mongo1","age": 21, "score": {"chinese": 78, "math": 99}}])
   db.mongo.find() # 查询所有的数据
   db.mongo.find({"name": "mongo"}) # 查找名字为mongo的数据
   db.mongo.findOne() # 查找第一条数据
   # 更新一条数据，前面是条件，后面是数据
   db.mongo.update({"name": "mongo1"}, {"name": "mongo1", "age": "22"})
   db.mongo.remove({"name": "mongo1"}) # 删除一条数据
   db.mongo.drop() # 删除所有的数据
   db.dropDatabase() # 删除当前的数据库
   ```

4. mongo修改数据的值

   1. `$set`修改器

      ```shell
      # 只修改name为mongo的数据中age的值变为23
      db.mongo.update({"name": "mongo"},{"$set": {"age": "23"}})
      ```

   2. 修改内嵌数据

      ```shell
      # 修改socre对象里面chinese的值
      db.mongo.update({"name": "mongo"},{"$set": {"score.chinese": "100"}})
      ```

   3. 删除其中某一个值

      ```shell
      # 删除score中chinese这一项
      db.mongo.update({"name": "mongo"},{"$unset": {"score.chinese": ""}})
      ```

   4. 添加某一项

      ```shell
      # 因为score对象不存在chinese，所以新添加一项
      db.mongo.update({"name": "mongo"},{"$set": {"score.chinese": "89"}})
      ```

   5. 批量更新

      ```shell
      # 给集合的所有数据都添加一个array字段，这个字段是一个数组
      db.mongo.update({},{"$set": {"array": []}}, {"multi": "true"})
      ```

   6. 如果更新时不存在此数据，则添加

      ```shell
      # 数据库本来不存在mongo2的数据，添加upsert就可以更新时插入一条新的数据
      db.mongo.update({"name": "mongo2"},{"$set": {"age": "24"}}, {"upsert": "true"})
      ```

5. 数组操作

   1. 数组添加一个数据

      ```shell
      # 向array字段(数组)中添加一个对象
      db.mongo.update({"name": "mongo"},{"$push": {"array": {"param1": "test"}}})
      ```

   2. 向数组中添加多个值

      ```shell
      db.mongo.update({"name": "mongo2"}, {"$push": {"array": {"$each": ["test2", "test3"]}}})
      ```

   3. 查找

      ```shell
      db.mongo.find({"array":["test2"]}) # 完全匹配
      
      db.mongo.find({"array":"test2"}) # 只要包含test2就算一条数据
      
      db.mongo.find({"array": {"$all":["test2", "test4"]}}) # 即得包含test2也得包含test4
      
      db.mongo.find({"array": {"$in":["test2", "test4"]}}) # 包含test2或者包含test4
      
      db.mongo.find({"array": {"$size":1}}) # 查找数组大小给1的数据
      
      # 只显示array数组的第一项
      db.mongo.find({"name": "mongo2"}, {"array": {"$slice":1}, "_id": false})
      ```

6. findAndModify

   ```js
   db.runCommand({
       findAndModify: "mongo",				// 查找的集合
       query: {"name": "mongo"},			// 查找的条件
       update: {"$set": {"age": 24}},		// 更新操作
       new: true							// 返回更新后的值
   })
   ```

7. 查找

   1. 查找某一项并显示其中的几项

      ```javascript
      db.mongo.find({"name": "mongo"}, {"age": true, "_id": false})
      ```

   2. 判断符

      ```shell
      $lte # 小于等于
      $gte # 大于等于
      ```

   3. 一个key多个value

      ```shell
      db.mongo.find({"age": {"$in": [24, 26]}}); # 查找age为24和26的数据
      
      db.mongo.find({"age": {"$nin": [24]}}); # 查看age不为24的数据
      ```

   4. 且

      ```shell
      db.mongo.find({"$and":[{"age": {"$gt": 20}}, {"name": "mongo"}]}); # age大于20并且name为mongo
      ```

   5. 或

      ```shell
      db.mongo.find({"$or":[{"age": {"$gt": 28}}, {"name": "mongo"}]}); # age大于28或者name为mongo
      ```

   6. 否则

      ```shell
      db.mongo.find({"age": {
          "$not":{
              "$gt": 23
              }
          }
      }); # 只显示age不大于23的数据
      ```

   7. 分页查找

      ```shell
      # 每次显示1个数据，跳过0个数据，按照age降序显示
      db.mongo.find({}, {"name": true, "age": true}).limit(1).skip(0).sort({"age": -1})
      ```

   8. `$where`查询

      ```shell
      db.mongo.find({"$where": "this.age < 30"})
      ```

8. mongo建索引

   1. 建立一个2百万数据的集合

      ```javascript
      use user
      
      function randomNum(min, max){
          return Math.round((max - min) * Math.random()) + min;
      }
      
      function randomName(min, max){
          let str = "1234567890poiuytrewqazxsdcvfgbnhjmkl".split("");
          var name = "";
          for(let i = 0; i < randomNum(min, max); i++){
              name = name + str[randomNum(0, str.length - 1)]
              }
              
          return name;
      }
      
      var users = [];
      for(let i = 0; i < 2000000; i++){
          users.push({
              "name": randomName(5, 10),
              "age": randomNum(20, 60),
              "score": {
                  "math": randomNum(60, 100),
                  "chinese": randomNum(50, 90)
                  }
              })
      }
      
      db.user.insert(users);
      
      db.user.find()
      
      db.user.stats()
      ```

   2. 查询集合的索引

      ```shell
      db.user.getIndexes()
      ```

   3. 建立索引

      ```shell
      db.user.ensureIndex({"name": 1})
      ```

      `复合索引`：两条以上的索引，**mongodb的复合查询是按照索引顺序进行查询的**

      使用`hint`设置优先索引的字段

      ```shell
      db.user.find({"name": "ogd1c5k", "age": 60}).hint({"age": 1})
      ```
      **参考建议**

      不使用索引的情况

      * 数据不超万条时，不需要使用索引。性能的提升并不明显，而大大增加了内存和硬盘的消耗。
      * **查询数据超过表数据量30%时，不要使用索引字段查询。实际证明会比不使用索引更慢，因为它大量检索了索引表和我们原表。**
      * 数字索引，要比字符串索引快的多，在百万级甚至千万级数据量面前，使用数字索引是个明确的选择。
      * 把你经常查询的数据做成一个内嵌数据（对象型的数据），然后集体进行索引。

   4. 删除索引

      ```shell
      # 根据db.user.getIndexes()查询索引的name并填入dropIndex方法中
      db.user.dropIndex("age_1")
      ```

   5. 全文索引

      ```shell
      # 存储数据的集合创建
      var contexts = [];
      for(let i = 0; i < 10000; i++){
          contexts.push({"context": randomName(1000, 5000)});
      }
      db.text.insert(contexts);
      
      # 建立全文索引，注意为text
      db.text.ensureIndex({"context": "text"})
      
      # $text是进行全文检索的标识，$search表示要查找的内容
      db.text.find({"$text": {"$search": "rdf8m"}})
      ```

9. mongo用户管理

   1. 登录到`mongo`

      ```shell
      docker exec -it 3719 /bin/sh # 进入docker的命令行
      
      mongo -u mongo -p mongo 127.0.0.1:27017/admin # 连接到mongo
      ```

   2. 创建账户

      ```shell
      db.createUser({ 
      	user: 'buse', 
      	pwd: 'buse', 
      	roles: [{ 
      		role: "readWrite", 
      		db: "user" 
      	}] 
      });
      ```

   3. 使用新建的账户连接`mongo`

      ```shell
      mongo -u buse -p buse 127.0.0.1:27017/admin # 连接到mongo
      ```

   **注意**

   生产环境中不要使用有`root`权限的账户，使用新创建的权限较小的账户，**一定要设置密码**。

#### 参考资料

* [技术胖免费mongodb视频](https://jspang.com/post/mongodb.html)
* [docker版mongo的安装](https://www.jianshu.com/p/2181b2e27021)
* [Docker MongoDB 数据库备份 并复制到宿主 恢复](https://segmentfault.com/a/1190000012330284)