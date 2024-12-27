import redis
from flask import Flask
from rediscluster import RedisCluster

import settings

app = Flask(__name__)
"""
    1、参考资料：https://huaweicloud.csdn.net/637f7af4dacf622b8df85a16.html
    2、需先安装：
        pip install redis-py-cluster
        pip install redis
        pip install configparser
"""


class RedisTool:
    # def __init__(self, cluster=False, sentinel=False):
    def __init__(self):
        """
            调用方式：
            1、初始化 RedisTool： redis_tool = RedisTool().get_client()
            2、删除：redis_tool.delete(key)
            3、String 类型
                redis_tool.set(key, value)
                redis_tool.get(key)
            4、set集合
                redis_tool.sadd(key, value1, value2...)
                redis_tool.smembers(key)
            5、list列表
                redis_tool.lpush(key, value1, value2,...)
                redis_tool.lrange(key, start, end)  # 比如列出所有conn.lrange("key_name", 0, -1)
            6、hash哈希
                redis_tool.hset(key, field, value)
                redis_tool.hget(key, filed)
                redis_tool.hgetall(key)
            7、sorted set有序集合
                # 注意：有序集合键值对是与redis中操作相反的，redis中：zadd key score value
                # python中，分值对应的是字典中的值
                redis_tool.zadd(key, {value1: score1, value2: score2})
                redis_tool.zrange(key, start, end)
        """
        try:
            # 第一步：获取 redis 配置
            host = settings.Config.host
            port = settings.Config.port
            password = settings.Config.password
            db = settings.Config.db
            model = settings.Config.model
            startup_nodes = settings.Config.startup_nodes
            sentinel_list = settings.Config.sentinel_list
            # print(f"host={host},port={port},db={db}, startup_nodes={startup_nodes}")

            # 第二步:初始化 client
            if model == 'cluster':
                # 集群
                """
                    写入值，获取值
                    client.set("key_name", "value")
                    client.get("key_name")
                """
                # client = StrictRedisCluster(startup_nodes=startup_nodes, decode_response=True, password=password,max_connection=300)
                self.client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, password=password)
                print("====================redis 集群登录成功====================", flush=True)
            elif model == 'sentinel':
                """
                    # 使用master进行写的操作，使用slave进行读的操作
                    master.hset("key_name", "filed", "value")
                    slave.hget("key_name", "filed")
                    slave.hgetall("key_name")
                """
                mySentinel = redis.Sentinel(sentinel_list)
                master = mySentinel.master_for("mymaster", db=0)
                slave = mySentinel.slave_for("mymaster", db=0)
                print("====================redis 哨兵登录成功====================", flush=True)
            else:
                # 单机
                """
                    string类型的写入读取
                    client.set("key_name", "value")
                    client.get("key_name")
                """
                self.client = redis.StrictRedis(host=host, port=port, db=0, decode_responses=True, password=password)
                print("====================redis 单机登录成功====================", flush=True)
        except Exception as e:
            print(f"Redis 初始化异常: {e}")

    # 开启连接池
    def get_client(self):
        return self.client

    # 关闭连接池
    def close(self):
        if hasattr(self.client, 'connection_pool'):
            self.client.connection_pool.disconnect()
            print("====================redis 连接已关闭====================")
