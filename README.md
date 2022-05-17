# django bootstrap template

A template for django startproject and startapp.

一份django项目启动模板，使用 startproject 和 startapp 命令创建

## 使用示例

    # 使用 startproject_template 创建django项目模板
    django-admin startproject --template=startproject_template my_project .

    # 使用 app_name 创建django app模板
    django-admin startapp --template=app_name my_app

## startproject_template 模板说明

```
│  .env.example     # 环境变量示例
├─config            # 项目配置文件夹
│  ├─django         # 项目环境的配置
│  └─settings       # 框架及插件的配置
├─requirements      # 依赖包
└─scripts           # 脚本
```

## app_name 模板说明

```
├─admin         # 本app的admin管理端
├─apis          # 本app的api代码
├─forms         # 本app的表单代码
├─management    
│  └─commands   # 本app的django命令
├─migrations    # 本app的数据库迁移文件
├─models        # 本app的模型代码
├─resources     # 和import_export插件相关的导入导出类
├─selectors     # 存放从数据库读取的业务代码
├─serializers   # 和API相关，序列化和反序列化的代码
├─services      # 存放写入数据库的业务代码
├─templates     # django 前端模板
│   └─admin     # app的django admin的模板
├─__init__.py   # 使本目录作为python包
├─tests.py      # 测试代码
├─urls.py       # 本app的URL路由
└─views.py      # 本app的视图代码
```

## 参考资料

- https://docs.djangoproject.com/en/2.2/ref/django-admin/#startapp
- https://docs.djangoproject.com/en/2.2/ref/django-admin/#startproject
- https://github.com/HackSoftware/Django-Styleguide
- [Dan Palmer - Scaling Django to 500 apps](https://www.youtube.com/watch?v=NsHo-kThlqI)
