from xuance.tensorflow.policies import *
from xuance.tensorflow.utils import *


class ActorNet(tk.Model):
    def __init__(self,
                 state_dim: int,
                 action_dim: int,
                 hidden_sizes: Sequence[int],
                 normalize: Optional[tk.layers.Layer] = None,
                 initializer: Optional[tk.initializers.Initializer] = None,
                 activation: Optional[tk.layers.Layer] = None,
                 device: str = "cpu:0"):
        super(ActorNet, self).__init__()
        layers = []
        input_shapes = (state_dim,)
        for h in hidden_sizes:
            mlp, input_shapes = mlp_block(input_shapes[0], h, normalize, activation, initializer, device)
            layers.extend(mlp)
        layers.extend(mlp_block(input_shapes[0], action_dim, device=device)[0])
        self.model = tk.Sequential(layers)
        self.dist = CategoricalDistribution(action_dim)

    def call(self, x: tf.Tensor, training=None, masks=None):
        self.dist.set_param(self.model(x))
        return self.model(x)


class CriticNet(tk.Model):
    def __init__(self,
                 state_dim: int,
                 hidden_sizes: Sequence[int],
                 normalize: Optional[tk.layers.Layer] = None,
                 initializer: Optional[tk.initializers.Initializer] = None,
                 activation: Optional[tk.layers.Layer] = None,
                 device: str = "cpu:0"):
        super(CriticNet, self).__init__()
        layers = []
        input_shapes = (state_dim,)
        for h in hidden_sizes:
            mlp, input_shapes = mlp_block(input_shapes[0], h, normalize, activation, initializer, device)
            layers.extend(mlp)
        layers.extend(mlp_block(input_shapes[0], 1, device=device)[0])
        self.model = tk.Sequential(layers)

    def call(self, x: tf.Tensor, training=None, masks=None):
        return self.model(x)[:, 0]


class ActorCriticPolicy(tk.Model):
    def __init__(self,
                 action_space: Space,
                 representation: tk.Model,
                 actor_hidden_size: Sequence[int] = None,
                 critic_hidden_size: Sequence[int] = None,
                 normalize: Optional[tk.layers.Layer] = None,
                 initializer: Optional[tk.initializers.Initializer] = None,
                 activation: Optional[tk.layers.Layer] = None,
                 device: str = "cpu:0"):
        super(ActorCriticPolicy, self).__init__()
        self.action_dim = action_space.n
        self.representation = representation
        self.representation_info_shape = self.representation.output_shapes
        self.actor = ActorNet(representation.output_shapes['state'][0], self.action_dim, actor_hidden_size,
                              normalize, initializer, activation, device)
        self.critic = CriticNet(representation.output_shapes['state'][0], critic_hidden_size,
                                normalize, initializer, activation, device)

    def call(self, observations: Union[np.ndarray, dict], training=None, masks=None):
        outputs = self.representation(observations)
        a = self.actor(outputs['state'])
        v = self.critic(outputs['state'])
        return outputs, a, v


class ActorPolicy(tk.Model):
    def __init__(self,
                 action_space: Space,
                 representation: tk.Model,
                 actor_hidden_size: Sequence[int] = None,
                 normalize: Optional[tk.layers.Layer] = None,
                 initializer: Optional[tk.initializers.Initializer] = None,
                 activation: Optional[tk.layers.Layer] = None,
                 device: str = "cpu:0"):
        assert isinstance(action_space, Discrete)
        super(ActorPolicy, self).__init__()
        self.action_dim = action_space.n
        self.representation = representation
        self.representation_info_shape = self.representation.output_shapes
        self.actor = ActorNet(representation.output_shapes['state'][0], self.action_dim, actor_hidden_size,
                              normalize, initializer, activation, device)

    def call(self, observation: Union[np.ndarray, dict], training=None, masks=None):
        outputs = self.representation(observation)
        a = self.actor(outputs['state'])
        return outputs, a


class PPGActorCritic(tk.Model):
    def __init__(self,
                 action_space: Space,
                 representation: tk.Model,
                 actor_hidden_size: Sequence[int] = None,
                 critic_hidden_size: Sequence[int] = None,
                 normalize: Optional[tk.layers.Layer] = None,
                 initializer: Optional[tk.initializers.Initializer] = None,
                 activation: Optional[tk.layers.Layer] = None,
                 device: str = "cpu:0"):
        assert isinstance(action_space, Discrete)
        super(PPGActorCritic, self).__init__()
        self.action_dim = action_space.n
        self.representation = representation
        self.policy_representation = representation
        self.critic_representation = copy.deepcopy(representation)
        self.representation_info_shape = self.policy_representation.output_shapes

        self.actor = ActorNet(representation.output_shapes['state'][0], self.action_dim, actor_hidden_size,
                              normalize, initializer, activation, device)
        self.critic = CriticNet(representation.output_shapes['state'][0], critic_hidden_size,
                                normalize, initializer, activation, device)
        self.aux_critic = CriticNet(representation.output_shapes['state'][0], critic_hidden_size,
                                    normalize, initializer, activation, device)

    def call(self, observation: Union[np.ndarray, dict], training=None, masks=None):
        policy_outputs = self.policy_representation(observation)
        critic_outputs = self.critic_representation(observation)
        a = self.actor(policy_outputs['state'])
        v = self.critic(critic_outputs['state'])
        aux_v = self.aux_critic(policy_outputs['state'])
        return policy_outputs, a, v, aux_v


class CriticNet_SACDIS(tk.Model):
    def __init__(self,
                 state_dim: int,
                 action_dim: int,
                 hidden_sizes: Sequence[int],
                 initializer: Optional[tk.initializers.Initializer] = None,
                 activation: Optional[tk.layers.Layer] = None,
                 device: str = "cpu:0"):
        super(CriticNet_SACDIS, self).__init__()
        layers = []
        input_shape = (state_dim,)
        for h in hidden_sizes:
            mlp, input_shape = mlp_block(input_shape[0], h, None, activation, initializer, device)
            layers.extend(mlp)
        layers.extend(mlp_block(input_shape[0], action_dim, None, None, initializer, device)[0])
        self.model = tk.Sequential(layers)

    def call(self, x: tf.Tensor, training=None, masks=None):
        return self.model(x)


class ActorNet_SACDIS(tk.Model):
    def __init__(self,
                 state_dim: int,
                 action_dim: int,
                 hidden_sizes: Sequence[int],
                 normalize: Optional[tk.layers.Layer] = None,
                 initializer: Optional[tk.initializers.Initializer] = None,
                 activation: Optional[tk.layers.Layer] = None,
                 device: str = "cpu:0"):
        super(ActorNet_SACDIS, self).__init__()
        layers = []
        input_shape = (state_dim,)
        for h in hidden_sizes:
            mlp, input_shape = mlp_block(input_shape[0], h, normalize, activation, initializer, device)
            layers.extend(mlp)
        layers.extend(mlp_block(input_shape[0], action_dim, None, None, None, device)[0])
        self.outputs = tk.Sequential(layers)
        self.model = tk.layers.Softmax(axis=-1)

    def call(self, x: tf.Tensor, training=None, masks=None):
        action_prob = self.model(self.outputs(x))
        dist = tfd.Categorical(probs=action_prob)
        return action_prob, dist


class SACDISPolicy(tk.Model):
    def __init__(self,
                 action_space: Space,
                 representation: tk.Model,
                 actor_hidden_size: Sequence[int],
                 critic_hidden_size: Sequence[int],
                 normalize: Optional[tk.layers.Layer] = None,
                 initializer: Optional[tk.initializers.Initializer] = None,
                 activation: Optional[tk.layers.Layer] = None,
                 device: str = "cpu:0"):
        # assert isinstance(action_space, Box)
        super(SACDISPolicy, self).__init__()
        self.action_dim = action_space.n
        self.representation = representation
        self.representation_info_shape = self.representation.output_shapes

        self.actor = ActorNet_SACDIS(representation.output_shapes['state'][0], self.action_dim, actor_hidden_size,
                                     normalize, initializer, activation, device)
        self.critic = CriticNet_SACDIS(representation.output_shapes['state'][0], self.action_dim, critic_hidden_size,
                                       initializer, activation, device)
        self.target_critic = CriticNet_SACDIS(representation.output_shapes['state'][0], self.action_dim,
                                              critic_hidden_size, initializer, activation, device)
        self.soft_update(tau=1.0)

    def action(self, observation: Union[np.ndarray, dict]):
        outputs = self.representation(observation)
        act_prob, act_distribution = self.actor(outputs['state'])
        return outputs, act_prob, act_distribution

    def Qtarget(self, observation: Union[np.ndarray, dict]):
        outputs = self.representation(observation)
        act_prob, act_distribution = self.actor(outputs['state'])
        log_action_prob = tf.math.log(act_prob + 1e-5)
        return outputs, act_prob, log_action_prob, self.target_critic(outputs['state'])

    def Qaction(self, observation: Union[np.ndarray, dict]):
        outputs = self.representation(observation)
        return outputs, self.critic(outputs['state'])

    def Qpolicy(self, observation: Union[np.ndarray, dict]):
        outputs = self.representation(observation)
        act_prob, act_distribution = self.actor(outputs['state'])
        # z = act_prob == 0.0
        # z = z.float() * 1e-8
        log_action_prob = tf.math.log(act_prob + 1e-5)
        return outputs, act_prob, log_action_prob, self.critic(outputs['state'])

    def soft_update(self, tau=0.005):
        for ep, tp in zip(self.critic.variables, self.target_critic.variables):
            tp.assign((1 - tau) * tp + tau * ep)
