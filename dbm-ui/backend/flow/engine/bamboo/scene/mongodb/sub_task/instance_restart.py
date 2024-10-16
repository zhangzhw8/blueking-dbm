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

from copy import deepcopy
from typing import Dict, Optional

from django.utils.translation import ugettext as _

from backend.flow.engine.bamboo.scene.common.builder import SubBuilder
from backend.flow.plugins.components.collections.mongodb.exec_actuator_job import ExecuteDBActuatorJobComponent
from backend.flow.plugins.components.collections.mongodb.send_media import ExecSendMediaOperationComponent
from backend.flow.utils.mongodb.mongodb_dataclass import ActKwargs


def instance_restart(
    root_id: str, ticket_data: Optional[Dict], sub_kwargs: ActKwargs, instances_info: dict, only_change_param: bool
) -> SubBuilder:
    """
    单个instance 重启流程
    """

    # 获取变量
    sub_get_kwargs = deepcopy(sub_kwargs)

    # 创建子流程
    sub_pipeline = SubBuilder(root_id=root_id, data=ticket_data)

    # 介质下发
    sub_get_kwargs.get_file_path()
    sub_get_kwargs.payload["hosts"] = instances_info["hosts"]
    kwargs = sub_get_kwargs.get_send_media_kwargs(media_type="actuator")
    sub_pipeline.add_act(
        act_name=_("MongoDB-介质下发"), act_component_code=ExecSendMediaOperationComponent.code, kwargs=kwargs
    )

    # 创建原子任务执行目录
    kwargs = sub_get_kwargs.get_create_dir_kwargs()
    sub_pipeline.add_act(
        act_name=_("MongoDB-创建原子任务执行目录"), act_component_code=ExecuteDBActuatorJobComponent.code, kwargs=kwargs
    )

    # 重启实例
    for instance in instances_info["instances"]:
        kwargs = sub_get_kwargs.get_instance_restart_kwargs(
            host=instances_info["hosts"][0],
            instance=instance,
            cache_size_gb=0,
            mongos_conf_db_old="",
            mongos_conf_db_new="",
            cluster_id=0,
            only_change_param=only_change_param,
        )
        sub_pipeline.add_act(
            act_name=_(
                "MongoDB-cluster_id:{}-ip:{}-port:{}--重启实例".format(
                    instance["cluster_id"], instances_info["hosts"][0]["ip"], str(instance["port"])
                )
            ),
            act_component_code=ExecuteDBActuatorJobComponent.code,
            kwargs=kwargs,
        )

    return sub_pipeline.build_sub_process(sub_name=_("MongoDB--重启实例--ip:{}".format(instances_info["hosts"][0]["ip"])))
