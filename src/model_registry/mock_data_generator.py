import random



from model_registry.database_schema import MLModel,Algorithm,Metadata
algorithm_names = [
'Linear Regression',
'Polynomial Regression',
'Ridge Regression',
'Lasso Regression',
'Elastic Net Regression',
'Support Vector Regression',
'Decision Tree Regression',
'Random Forest Regression',
'XGBoost',
'LightGBM',
'CatBoost',
'Bayesian Regression',
'K-NN Regression',
'Logistic Regression',
'Support Vector Machines (SVM)',
'K-Nearest Neighbors (KNN) Classification',
'Decision Trees',
'Random Forest Classification',
'Gradient Boosting Machines (GBM)',
'AdaBoost',
'XGBoost',
'LightGBM',
'CatBoost',
'Naive Bayes',
'Neural Networks',
'Quadratic Discriminant Analysis (QDA)',
'Linear Discriminant Analysis (LDA)',
'K-Means',
'Hierarchical Clustering',
'DBSCAN (Density-Based Spatial Clustering of Applications with Noise)',
'Mean Shift',
'Gaussian Mixture Models (GMM)',
'BIRCH (Balanced Iterative Reducing and Clustering using Hierarchies)',
'Affinity Propagation',
'Principal Component Analysis (PCA)',
'Independent Component Analysis (ICA)',
't-Distributed Stochastic Neighbor Embedding (t-SNE)',
'Linear Discriminant Analysis (LDA)',
'Factor Analysis',
'Non-Negative Matrix Factorization (NMF)',
'UMAP (Uniform Manifold Approximation and Projection)',
'Self-training',
'Co-training',
'Generative Adversarial Networks (GANs) for Semi-Supervised Learning',
'Graph-based Semi-Supervised Learning',
'Q-Learning',
'SARSA (State-Action-Reward-State-Action)',
'Deep Q-Networks (DQN)',
'Policy Gradient Methods',
'Actor-Critic Methods',
'Deep Deterministic Policy Gradient (DDPG)',
'Proximal Policy Optimization (PPO)',
'Trust Region Policy Optimization (TRPO)',
'Bagging (Bootstrap Aggregating)',
'Random Forest',
'Boosting',
'Stacking',
'Voting Classifier',
'Blending',
'Convolutional Neural Networks (CNN)',
'Recurrent Neural Networks (RNN)',
'Long Short-Term Memory Networks (LSTM)',
'Gated Recurrent Unit (GRU)',
'Autoencoders',
'Generative Adversarial Networks (GANs)',
'Transformer Networks',
'BERT (Bidirectional Encoder Representations from Transformers)',
'GPT (Generative Pre-trained Transformer)',
'Bayesian Networks',
'Hidden Markov Models (HMM)',
'Markov Chain Monte Carlo (MCMC)',
'Gaussian Processes',
'Locally Weighted Learning',
'Case-Based Reasoning',
'Genetic Algorithms (GA)',
'Genetic Programming (GP)',
'Evolutionary Strategies (ES)',
'Differential Evolution (DE)',
'Neural Evolution',
'Neuro-Fuzzy Systems'
]
from random import shuffle

def create_mock_algorithms(size: int = 50) -> list[Algorithm]:
    mock_algorithms = []
    for i in range(size):
        mock_algorithms.append(Algorithm(name=algorithm_names[i]))
    return mock_algorithms


def create_mock_models(batch_size) -> list[MLModel]:
    mock_models = []
    # Random ids
    ids = [i for i in range(1,batch_size)]
    random.shuffle(ids)
    for elem in ids:
        mock_models.append(MLModel(name='name' + str(elem),file_path='C:\\foo',metadata=elem))
    return mock_models

def create_mock_model_metadata(batch_size):
    metadata = []
    for i in range(batch_size):
        random_shape = '(' + str(random.randint(1,10)) + "x" + str(random.randint(1,10)) + "x" + str(random.randint(1,10)) \
                       + "x" + str(random.randint(1, 10)) + ")"
        metadata.append(Metadata(dtype='string',input_shape=random_shape,params={'foo':'bar'},metrics={'mse':'pippo'}))

    return metadata