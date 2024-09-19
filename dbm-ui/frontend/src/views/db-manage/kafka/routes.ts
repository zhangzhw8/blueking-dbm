/*
 * TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
 *
 * Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
 *
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at https://opensource.org/licenses/MIT
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
 * the specific language governing permissions and limitations under the License.
 */

import type { RouteRecordRaw } from 'vue-router';

import type { BigdataFunctions } from '@services/model/function-controller/functionController';
import FunctionControllModel from '@services/model/function-controller/functionController';

import { t } from '@locales/index';

const routes: RouteRecordRaw[] = [
  {
    name: 'KafkaManage',
    path: 'kafka',
    meta: {
      navName: t('Kafka_集群管理'),
    },
    redirect: {
      name: 'KafkaList',
    },
    component: () => import('@views/db-manage/kafka/Index.vue'),
    children: [
      // {
      //   name: 'KafkaApply',
      //   path: 'apply',
      //   meta: {
      //     navName: t('申请Kafka集群部署'),
      //   },
      //   component: () => import('@views/db-manage/kafka/apply/Index.vue'),
      // },
      {
        name: 'KafkaList',
        path: 'list',
        meta: {
          navName: t('Kafka_集群管理'),
          fullscreen: true,
        },
        component: () => import('@views/db-manage/kafka/list/Index.vue'),
      },
    ],
  },
];

export default function getRoutes(funControllerData: FunctionControllModel) {
  const controller = funControllerData.getFlatData<BigdataFunctions, 'bigdata'>('bigdata');
  return controller.kafka ? routes : [];
}