# 版本更新记录

* **2023.12.19 v0.1.0版本发布**：[Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.1.0)
  * 初始版本发布，基础云组件支持包括BES；AI能力引擎语音、视觉类10个能力，大模型相关RAG、文本生成能力19个。
* **2024.01.03 v0.2.0版本发布** [Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.2.0)
  * 核心升级点GBI相关组件新增，v0.1.0遗留问题修复
* **2024.01.26 v0.3.0版本发布** [Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.3.0)
  * 新增组件：新增了百度搜索rag组件(RAGwithBaiduSearch)。[Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/rag_with_baidusearch.ipynb)
  * 模型列表获取：与千帆大模型平台模型名打通，可动态获取当前账号模型名，并在组件中使用[获取模型列表](/docs/basic_module/get_model_list.md)
  * 可通过官方镜像开发和运行实例代码[二次开发](/docs/develop_guide/README.md)
* **2024.02.27 v0.4.0版本发布** [Release Note](https://github.com/baidubce/app-builder/releases/tag/0.4.0)
  * AppBuilder Console SDK发布[知识集合Cookbook](/cookbooks/end2end_application/rag/console_dataset.ipynb)，[RAG调用Cookbook](/cookbooks/end2end_application/rag/rag.ipynb)
  * 大模型组件新增：Excel2Figure(基于Excel信息画图表)
  * AI能力引擎组件新增&更新：植物识别、动物识别、表格文字识别V2、手写文字识别、二维码识别、身份证混贴识别、文档矫正识别、图像内容理解、流式TTS
  * AgentRuntime：新增[Cookbook](/cookbooks/components/agent_runtime.ipynb)
* **2024.03.13 v0.4.1版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.4.1)
  * 支持以下功能进行FunctionCall调用：动植物识别、表格文字识别、条形码及二维码识别、身份证混贴识别、手写文字识别、text2image、excel2figure
* **2024.03.20 v0.5.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.5.0)
  * AgentBuilder ConsoleSDK发布 [Agent调用Cookbook](/cookbooks/end2end_application/agent/appbuilder_client.ipynb)
  * AI能力引擎组件新增：向量检索-VDB
  * 支持以下功能进行FunctionCall调用并新增[Cookbook](/cookbooks/components/general_ocr.ipynb)：文本翻译-通用版、通用物体和场景识别-高级版、通用文字识别-高精度版、短语音识别-极速版
* **2024.03.21 v0.5.1版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.5.1)
  * 问题修复：修复了在Python 3.8 及以下环境无法使用AgentBuilder ConsoleSDK的问题。同时，在即将发布的0.6.0版本中，将不再提供对Python 3.8及以下环境的支持，请升级Python版本到3.9
* **2024.04.12 v0.6.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.6.0)
  * AppBuilder Console SDK 支持 JAVA 语言 [AppBuilder Java ConsoleSDK](/java/)
  * AppBuilder Console SDK 支持 GO 语言 [AppBuilder GO ConsoleSDK](/go/)
  * 首页README更新，提供免费的公共试用TOKEN，方便开发者快速体验
* **2024.04.30 v0.7.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.7.0)
  * 提供Assistant SDK 功能，新增 [Cookbook](/cookbooks/pipeline/assistant_function_call.ipynb)，包含流程编排与FunctionCall，搭建个性化Agent应用
  * AgentBuilder组件更名为 AppBuilderClient, 后续版本将放弃对 `AgentBuilder` 的后向兼容支持
  * 首页Readme与文档结构优化
* **2024.05.21 v0.7.1版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.7.1)
  * 更新Assistant SDK 功能，为assistants/threads/messages/runs/files模块提供了完整的增删改查api, 新增`appbuilder.AssistantEventHandler`与`appbuilder.assistant.threads.runs.stream_run_with_handler`方法，更好的支持Assistant的流式调用
  * 支持AppBuilder Client通过chainlit进行可视化的服务化部署
  * 优化SDK的报错信息提示，方便开发者进行debug
  * 修复文档格式转换组件的域名错误问题
* **2024.06.11 v0.8.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.8.0)
  * 提供功能更强大的Debug模式
  * 支持AppBuilder Client通过chainlit进行可视化的服务化部署
  * 多个组件进行了效果优化与说明文档更新
* **2024.06.28 v0.9.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.0)
  * Python/Go/Jave Console SDK 上新，支持Token用量返回，支持`get_app_list`， 支持`KnowledgeBase`功能
  * 新增AppBuilder-SDK Depoly功能，支持用户使用SDK快速部署本地组件orAgent应用到百度智能云，并对外提供服务
  * 更新SDK超参，支持SDK在私有化部署环境的使用
  * 更新口语化组件，优化效果
* **2024.07.25 v0.9.1版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.1)
  * KnowledgeBase组件完整支持`知识库`、`知识库文档`及`文档切片`的增删改查
  * 新增appbuilder_trace_server与AppBuilderTracer功能，支持组件、AppBuilderClient、Assistant的链路追踪
* **2024.08.16 v0.9.2版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.2)
  * AppBuilderClient 新增ToolCall功能，支持开发者注册本地函数为组件，扩展Agent能力边界
  * 新增`PPTGenerationFromFile`、`PPTGenerationFromInstruction`、`PPTGenerationFromPaper`三个组件
* **2024.08.20 v0.9.3版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.3)
  * Text2Image组件接口及效果更新
  * ImageUnderstand组件接口及效果更新
* **2024.09.04 v0.9.4版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.4)
  * AppBuilderClient新增tool_choice / end_user_id功能
  * 增加VScode setting，优化开发者使用体验
* **2024.10.18 v0.9.5版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.5)
  * 更新KnowledgeBase组件，新增`切片详情`获取接口，新增切片关联的图片ID字段
  * AppBuilderTrace 支持SentrySDK
  * AppBuilder新增[Sphinx API文档](../../API-Reference/Python/modules.md)
* **2024.10.26 v0.9.6版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.6)
  * 更新AppBuilderClient，简化Java & Go语言使用ToolCall的方式
  * 新增长文档内容理解组件
  * 优化requirements，去除部分组件的版本限制
  * 简化报错堆栈，去除冗余的Trace信息
* **2024.11.27 v0.9.7版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.7)
  * 新增TreeMind组件
  * 新增工作流Agent回复“信息收集节点”功能，支持多轮对话事件处理
  * Python的ToolCall功能支持通过函数定义、装饰器的形式等生成ToolCall参数
* **2024.12.10 v0.9.8版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.9.8)
  * AppBuilderClient新增追问功能支持
  * TTS组件新增更多语音效果
  * 通用文字识别组件新增更多语言支持
  * 实时语音通话功能内测
* **2025.01.03 v1.0.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/1.0.0)
  * 工作流自定义组件支持SDK调用
  * 新增RAG检索SDK
  * Agent Python SDK支持Async调用
  * 新增滚动日志功能
* **2025.01.16 v1.0.1版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/1.0.1)
  * 修复1.0.0中的Python SDK流式调用慢问题
* **2025.01.24 v1.0.2版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/1.0.2)
  * 升级KnowledgebaseClient，同步更新OpenAPI的入参
  * 升级KnowledgebaseClient，同步更新知识库创建入参
  * 升级ComponentClient，同步更新OpenAPI的出参
* **2025.02.28 v1.0.3版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/1.0.3)
  * AppBuilderClient新增点踩点赞功能支持
  * 知识库支持配置目录、切片模糊搜索、文档状态信息等功能升级
  * MCP协议支持
* **2025.03.27 v1.0.4版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/1.0.4)
  * MCP Client新增SSE协议支持
  * 新增百度AI搜索的MCP Server
  * AppBuilderClient调用支持显示DeepSeek-R1思考过程
* **2025.04.05 v1.0.5版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/1.0.5)
* **2025.04.24 v1.0.6版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/1.0.6)
  * 组件MCP SSE Server支持多副本
  * 新增 AppBuilder RAG MCP服务
  * 新增 AppBuilder Agent MCP服务
  * MCP Server支持添加OpenAPI tools
* **2025.06.20 v1.1.0版本发布** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/1.1.0)
  * Python/Java 支持AI搜索V2，支持百度搜索
  * Python模型列表SDK切换v2接口，新增
  * Python/Go/Java 增加应用详情SDK，支持自主规划Agent、工作流Agent
  * Java SDK 流式响应支持手动中断
