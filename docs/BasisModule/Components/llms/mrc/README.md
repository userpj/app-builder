# 阅读理解问答（MRC）

## 简介
阅读理解问答（MRC）组件是基于生成式大模型的阅读理解问答系统。该组件支持拒答、澄清、重点强调、友好性提升、溯源等多种功能，可用于回答用户提出的问题。

### 功能介绍
MRC（阅读理解问答模块）是一项先进的自然语言处理功能，旨在使机器能够理解、分析文本内容，并基于这些内容回答相关问题。 本模块基于大语言模型，提供对文本内容的深入理解和精确回答能力。

### 特色优势
我们的MRC模块，基于百度自研的先进语言模型文新一言，提供了一系列强大的阅读理解问答功能。在保持文本理解和问题回答的高精度的同时，
我们特别强调了答案的质量和交互体验。以下是我们MRC模块的几个主要功能特色：
 - 1.多版本模型支持：我们的MRC模块包括不同版本的文新一言大模型，Erniebot 4.0、Qianfan-Agent-Speed-8K等，每个版本都针对特定的应用场景进行了优化。 用户可以根据自己的需求选择最适合的模型版本，以获得最佳的性能。
 - 2.答案格式的多样性：
   - 拒答功能：当问题超出模型知识范围或不具体时，模型可以选择不回答，避免提供误导性信息。
   - 澄清功能：对于模棱两可或含糊的问题，模型可以请求更多信息或对问题进行澄清，以确保答案的准确性。
   - 重点内容强调：模型可以识别并强调答案中的关键信息，使答案更清晰、更易于理解。
   - 友好度提升：模型可以以更自然、更亲切礼貌的方式呈现答案，且必要时对答案进行分点论述，改善用户体验。
   - 答案溯源：模型能提供答案的来源信息，增强答案的可信度和透明度。

 - 3.灵活的功能开关：每项功能都配备了开关，用户可以根据不同的应用场景和需求，灵活地启用或关闭某些功能。这种可定制性确保了MRC模块能够在各种环境下提供最优化的表现。

### 应用场景
我们的MRC模块，凭借文心大模型强大的文本理解能力，以及多功能性，已在多个领域展现出显著的价值。
 - 政务服务：在政务领域，MRC模块可以帮助构建智能问答系统，为公民提供关于政策、法规和服务程序的即时信息。它可以通过理解复杂的政府文件和公文，准确回答与政策相关的查询，极大地提高政府服务的效率和透明度。
 - 法律咨询：法律领域充满了专业术语和复杂的概念。我们的MRC模块能够深入理解法律文献和案例，为法律专业人士和普通民众提供准确的法律咨询。无论是寻找相关法条还是理解特定法律案例，MRC模块都能提供快速、可靠的帮助。
 - 医疗健康：在医疗健康领域，准确的信息至关重要。MRC模块能够解析医学文献、病例报告和临床试验数据，为医生和研究人员提供支持，帮助他们在诊断、治疗和研究中做出更明智的决策。此外，它也能在患者咨询中发挥作用，为患者提供关于疾病、治疗方案和药物的详细信息。
 - 教育和研究：MRC模块可以作为学习和研究的强大工具，帮助学生和研究人员快速找到他们需要的信息。无论是解答学术问题，还是提供详细的背景资料，MRC模块都能提供卓越的支持。
 - 企业客户服务：企业可以利用MRC模块构建高效的客服系统，提供24/7的咨询服务。从产品详情到服务流程的解释，MRC模块都能提供准确、及时的答案，提升客户满意度并减轻人工客服的压力。
 - 金融咨询：在金融领域，MRC模块可以帮助用户理解复杂的金融产品、市场趋势和投资策略。通过提供准确的数据解读和市场分析，MRC模块能够辅助投资者和金融专业人士做出更明智的决策。
除上述场景以外，还可应用于其他更多生产生活的场景中。

## 基本用法

### 快速开启

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

# 创建MRC对象
mrc_component = appbuilder.MRC(model="Qianfan-Agent-Speed-8K")

# 初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)
context_list = appbuilder.Message(["""如何办理残疾人通行证一、残疾人通行证办理条件：
1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）""",
                    """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
北京市无障碍环境建设促进中心"""])

# 模拟运行MRC基本组件
result = mrc_component.run(msg, context_list)

# 输出运行结果
print(result)
```

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
import os
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
- `model`: 模型名称，用于指定要使用的千帆模型。

### 调用参数
|参数名称 |参数类型 | 是否必须 |描述 | 示例值                                      |
|--------|--------|---|----|------------------------------------------|
|msg |Message  | 是 |输入消息，包含用户提出的问题。| Message("你好")                            |
|context_list|Message| 是 |用户输入的问题对应的段落文本列表。| Message(["""context1""","""context2"""]) |
|reject|bool| 否 |拒绝开关，如果为 True，则启用该能力。默认为 False。当输入的问题在context_list中没有找到答案时，开关开启时，模型会用特定话术("当前文档库找不到对应的答案，我可以尝试用我的常识来回答你。")做回复的开头，并后接自有知识做回复内容。| eg.示例值                                   |
|clarify|bool| 否 |澄清开关，如果为 True，则启用该能力。默认为 False。 当输入的问题比较模糊、或者主体指代不清晰，且context_list中包含有可以回答该模糊问题的多种潜在备选答案时，开启该开关，大模型会以特定的话术做澄清反问，引导用户继续补充问题发问。举例子，query:发电机的续航时间？ Answer: 根据搜索结果得到了xx和xx两种型号的发电机，您的问题具体涉及到哪一个？请补充关键信息，作为完整的问题重新发问。| eg.示例值                                   |
|highlight|bool| 否 |重点强调开关，如果为 True，则启用该能力。默认为 False。开启该功能时，回复结果中会高亮显示关键部分的内容。| 加粗的部分是**重点内容**                           |
|friendly|bool| 否 |友好性提升开关，如果为 True，则启用该能力。默认为 False。开关开启时，部分回复的开头会加礼貌用语。且如果回答涉及到大段的信息，会倾向于以<总-分>或者<总-分-总>的形式做分点论述，使得答案的格式更规整，可读性更强。| eg.示例值                                   |
|cite|bool| 否 |溯源开关，如果为 True，则启用该能力。默认为 False。开关开启时，回复内容后会接形如(^[1]^)的标记来表示回答内容在原文(context_list)中的来源索引。例如：按照当地公安机关出入境管理部门规定的其他材料办理^[2]^。| eg.示例值                                   |
|temperature|float| 否 |模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。| 0.0001                                   |


### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|result  |Message  |返回结果|对象，包含模型运行后的输出消息。|
### 响应示例
```json
{"result": "极氪007的售价区间为20.99~29.99万元。"}
```

### 错误码
无



## 高级用法
该组件的高级用法包括定制化的输入处理、输出处理，以及更复杂的调用场景。用户可以根据具体需求扩展组件功能，实现个性化的问答系统。
包括如下功能：
1、拒答
2、澄清反问
3、重点强调
4、友好度提升
5、溯源


### 代码样例
```python
import appbuilder
import os

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建MRC对象
mrc_component = appbuilder.MRC(model="Qianfan-Agent-Speed-8K")

# 初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)
context_list = appbuilder.Message(["""如何办理残疾人通行证一、残疾人通行证办理条件：
1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）""",
                    """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
北京市无障碍环境建设促进中心"""])

# 模拟运行MRC组件，开启拒答、澄清追问、重点强调、友好性提升和溯源能力五个功能
result = mrc_component.run(msg, context_list, reject=True,
                           clarify=True, highlight=True, friendly=True, cite=True)

# 输出运行结果
print(result)
```

## 更新记录和贡献
* 阅读理解问答 (2023-12)


