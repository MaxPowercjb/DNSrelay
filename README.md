# DNSrelay
中国科学技术大学 计算机学院 计算机网络实验
## 使用方法：
### 使用环境
windows
### 步骤
- 1.将首选dns服务器地址设置为`127.0.0.1` 
- 2.执行`python server.py`
## 特征说明
- 1 可以阻拦或重定向特定的域名。
若要阻拦该域名，将其加入`hosts`文件，格式为
```
0.0.0.0 {blocked_domain_name}
例:
0.0.0.0 www.baidu.com
```
若要特定的域名定向到特定的ip，格式为
```
{redirect_ip} {redirect_domain_name}
例:将www.baidu.com定向到202.38.64.8 
202.38.64.8 www.baidu.com
注:重定向域名后，有些服务器会无法访问。这是服务器的设置的问题
```
- 2 该本地DNS服务器只会对type A和单条查询进行相应，其余类型会访问上级DNS服务器获取数据

- 3 更新上级服务器ip
在`settings.json`中`RemoteDnsServer`的条目中放入你要加入的ip


