# HR Service Workflow

id: HR-WF-01
version: 1.0
effective: 2026-09-01
status: active
owner: Fictional HR department
classification: Synthetic educational data

## fields | 工单必填字段
工单需要五个字段：employee_id、request_type、requested_date、reason、contact_channel。缺少信息时字段值为null并询问员工。缺少任一字段的草稿不算完整工单。

## intent | 咨询与办理
询问怎么申请、需要什么材料或是否可以属于咨询，不自动生成工单。明确要求帮我申请或创建草稿才属于办理；含糊请求先澄清。

## review | 审批与提交
所有生成工单都只是草稿。员工核实五个字段后，仍需自行进入正式人事系统提交。审批权属于主管或HR，助手没有提交和审批接口。

## version | 制度版本
本资料版本为1.0，2026-09-01生效，状态为active。仅载入已经生效的active版本；同一制度优先使用最新生效日期，同日期冲突停止载入并要求人工处理。

