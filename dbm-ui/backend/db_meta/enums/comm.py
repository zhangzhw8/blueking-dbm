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

from django.utils.translation import gettext_lazy as _

from blue_krill.data_types.enum import EnumField, StructuredEnum


class SyncType(str, StructuredEnum):
    MS = EnumField("ms", _("ms"))
    SMS = EnumField("sms", _("sms"))
    MMS = EnumField("mms", _("mms"))


class DBCCModule(str, StructuredEnum):
    REDIS = EnumField("redis", _("redis"))
    MONGODB = EnumField("mongodb", _("mongodb"))


class TagType(str, StructuredEnum):
    CUSTOM = EnumField("custom", _("自定义标签"))
    SYSTEM = EnumField("system", _("系统标签"))
    BUILTIN = EnumField("builtin", _("内置标签"))


class SystemTagEnum(str, StructuredEnum):
    """系统内置的tag名称"""

    TEMPORARY = EnumField("temporary", _("temporary"))


class TagResourceEnum(int, StructuredEnum):
    """资源类型"""

    CLUSTER = EnumField(0, _("集群"))
    STORAGE_INSTANCE = EnumField(1, _("存储实例"))
    PROXY_INSTANCE = EnumField(2, _("代理实例"))
    MACHINE = EnumField(3, _("实例机器"))
    RESOURCE_MACHINE = EnumField(4, _("资源池机器"))


class RedisVerUpdateNodeType(str, StructuredEnum):
    """redis版本升级节点类型"""

    Proxy = EnumField("Proxy", _("Proxy"))
    Backend = EnumField("Backend", _("Backend"))
