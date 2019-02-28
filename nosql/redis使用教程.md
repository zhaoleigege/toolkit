# redis使用教程

#### redis基本概念

1. redis的数据结构
   * string
     * raw
     * int
     * embstr
   * hash
     * hashtable
     * ziplist
   * list
     * linkedlist
     * ziplist
   * set
     * hashtable
     * intset
   * zset
     * skiplist
     * ziplist 
   * none

#### redis基本操作

1. 下载redis server

   ```shell
   docker run --name redis -v /Users/buse/Downloads/redis/data:/data -p 6379:6379 -d redis redis-server --appendonly yes --requirepass "redis"
   ```

2. 下载redis客户端

   ```shell
   brew install redis
   ```

3. 连接redis服务端

   ```shell
   redis-cli -h 127.0.0.1 -p 6379 -a redis
   ```

4. 基本操作

   * 字符串操作

     ```shell
     # 存储
     set <key> <value> # 存储一个数据，不管key存不存在
     setnx <key> <value> # key不存在才设置
     set <key> <value> xx # key存在才设置
     
     getset <key> <value> # 返回key旧的值，并设置新值为value
     append <key> <value> # 追加value到key原来的value后面
     strlen <key> # 计算value的长度
     
     mset <key1> <value1> <key2> <value2> # 一次存储多条数据
     mget <key1> <key2> # 一次检索多个值
     
     # 检索可以
     keys * # 检索所有的
     keys k* # 检索以k开头的key
     
     # 检索value
     get <key> # 获取key的value值
     
     # 删除key
     del <key> # 删除该key
     ```

     key自增操作

     ```shell
     incr <key> # key自增1，如果不存在则get <key>返回1
     
     decr <key> # key减1，如果不存在则get <key>返回-1
     
     incrby <key> 2 # key自增布长为2，如果不存在则get <key>返回2
     
     decrby <key> 2# key减2，如果不存在则get <key>返回-2
     ```

   * hash操作

     hash数据结构中，key为字符串但是value是hash结构的数据结构

     ```shell
     hset <key> <hashKey> <value> # 设置key的存储结构为为hash类型，其中该hash中存储为hashKey的值为value
     hget <key> <hashKey> # 返回这个key中hash的key为hashKey的value
     
     hdel <key> <hashKey> # 删除key中hash的key为hashKey的值
     
     hexists <key> <hashKey> # 判断是否存在
     
     hlen <key> # 返回该key中hash数据的多少
     
     hmset <key> <hashKey1> <value1> <hashKey2> <value2> ... # 一次设置多个值
     hmget <key> <hashKey1> <hashKey2>... # 一次获取多个值
     
     hincrby <key> <hashKey> <step> # 为key的hash表中健为hashKey的值加step
     
     hgetall <key> # 返回key中存储的hash数据集合，返回为
     # key1 
     # value1
     # key2
     # value2
     ...
     
     hkeys <key> # 只返回key中存储的hash数据集合的key值
     hvals <key> # 只返回key中存储的hash数据集合的value值
     ```

   * list操作

     ```shell
     lpush <key> <v1> <v2> <v3> #插入的结构为 v3-v2-v1
     rpush <key> <v1> <v2> <v3> #插入的结构为 v1-v2-v3
     
     linsert <key> before|after <value> <newValue> # 在value前面或者后面插入newValue
     
     lpop <key> # 从左边删除一个值
     rpop <key> # 从右边删除一个值
     
     ltrim <key> <start> <end> # 只保留列表中start到end的数据
     
     lrange <key> <start> <end> # 查询列表中start到end的数据
     lrange <key> 0 -1 # 查询列表中所有的数据
     
     lindex <key> <index> # 获取指定索引的值
     
     llen <key> # 算出列表的长度
     
     lset <key> <index> <newValue> # 设置列表对应索引处的值为newValue
     ```

   * set操作

     ```shell
     sadd <key> <element> # 向set中添加元素
     
     srem <key> <element> # 向set中删除元素
     
     scard <key> # 计算set的大小
     
     sismember <key> <element> # 判断element是否在此key对应的set中
     
     srandmember <key> # 随机返回一个元素
     
     spop <key> # 随机弹出一个元素
     
     smembers <key> # 返回所有的元素
     
     sdiff <key1> <key2> # 列出两个set集合的差集
     
     sinter <key1> <key2> # 列出两个set集合的交集
     
     sunion <key1> <key2> # 列出两个set集合的并集
     ```

   * zset（有序集合）操作

     ```shell
     zadd <key>  <score1> <element1> <score2> <element2>... # 添加一个元素，score只能是数字类型，score可以重复但是element不能重复，有序集合里面的元素按照score进行了升序排序
     
     zrem <key> <element1> <element2> ... # 删除元素
     
     zscore <key> <element> # 获取element的score
     
     zincrby <key> <scoreStep> <element> # 对element的socre增加scoreStep，scoreStep可以为负
     
     zcard <key> # 计算集合的大小，element的数量
     
     zrank <key> <element> # 获取element的排名，从0开始
     
     zrange <key> <start> <end> [withscores] # 按升序的方式显示start到end的集合中数据，添加withscores会同事打印出score
     
     zrangebyscore <key> <start> <end> # 显示score在start到end之间的数据
     
     zcount <key> <start> <end> # 显示score在start到end之间的数据有多少
     
     zremrangebyrank <key> <start> <end> # 删除序号start到end中的数据（包含）
     
     zremrangebyscore <key> <start> <end> # 删除score在start到end中的数据（包含）
     ```

   * 元数据

     ```shell
     dbsize # key的总数
     ```

   * 判断是否存在

     ```shell
     exists k1 # 是否存在该key
     ```

   * key存储时间设置

     ```shell
     expire k1 12 # 设置k1的过期时间为12秒
     ttl k1 # 查看k1还有多久会过期
     persist k1 # 去除k1的过期时间
     ```

   * 查看key的类型

     ```shell
     type k1 # 查看k1的类型
     ```

     