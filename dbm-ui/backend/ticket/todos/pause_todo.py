# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from dataclasses import dataclass

from django.utils.translation import gettext as _

from backend.ticket import todos
from backend.ticket.constants import TicketFlowStatus, TodoType
from backend.ticket.exceptions import TodoWrongOperatorException
from backend.ticket.flow_manager import manager
from backend.ticket.flow_manager.manager import TicketFlowManager
from backend.ticket.todos import ActionType, BaseTodoContext


@dataclass
class PauseTodoContext(BaseTodoContext):
    pass


@dataclass
class ResourceReplenishTodoContext(BaseTodoContext):
    user: str
    administrators: list


@todos.TodoActorFactory.register(TodoType.APPROVE)
class PauseTodo(todos.TodoActor):
    """来自主流程的待办"""

    def process(self, username, action, params):
        """确认/终止"""
        if username not in self.todo.operators:
            raise TodoWrongOperatorException(_("{}不在处理人: {}中，无法处理").format(username, self.todo.operators))

        if action == ActionType.TERMINATE:
            self.todo.set_terminated(username, action)
            return

        self.todo.set_success(username, action)

        # 所有待办完成后，执行后面的flow
        if not self.todo.ticket.todo_of_ticket.exist_unfinished():
            manager.TicketFlowManager(ticket=self.todo.ticket).run_next_flow()


@todos.TodoActorFactory.register(TodoType.RESOURCE_REPLENISH)
class ResourceReplenishTodo(todos.TodoActor):
    """资源补货的代办"""

    def process(self, username, action, params):
        """确认/终止"""
        if username not in self.todo.operators:
            raise TodoWrongOperatorException(_("{}不在处理人: {}中，无法处理").format(username, self.todo.operators))

        # 终止单据
        if action == ActionType.TERMINATE:
            self.todo.set_terminated(username, action)
            return

        # 尝试重新申请资源，申请成功则关闭todo单
        resource_apply_flow = TicketFlowManager(ticket=self.todo.ticket).get_ticket_flow_cls(self.todo.flow.flow_type)(
            self.todo.flow
        )
        resource_apply_flow.retry()

        # 注意这里需要刷新flow字段
        self.todo.refresh_from_db(fields=["flow"])
        if self.todo.flow.status == TicketFlowStatus.SUCCEEDED:
            self.todo.set_success(username, action)
