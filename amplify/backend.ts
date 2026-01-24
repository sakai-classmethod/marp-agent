import { defineBackend } from '@aws-amplify/backend';
import { auth } from './auth/resource';
import { createMarpAgent } from './agent/resource';

const backend = defineBackend({
  auth,
});

// AgentCoreスタックを作成
const agentCoreStack = backend.createStack('AgentCoreStack');

// Marp Agentを作成（Cognito認証統合）
const { endpoint } = createMarpAgent({
  stack: agentCoreStack,
  userPool: backend.auth.resources.userPool,
  userPoolClient: backend.auth.resources.userPoolClient,
});

// フロントエンドにエンドポイント情報を渡す
backend.addOutput({
  custom: {
    agentEndpointArn: endpoint.agentRuntimeEndpointArn,
    agentRuntimeArn: endpoint.agentRuntimeArn,
  },
});
