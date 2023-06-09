from Collaborative_Filtering.RP3betaRecommender import RP3betaRecommender
from FeatureWeighting.Cython.Feature_Weighting import Feature_Weighting, EvaluatorCFW_D_wrapper

from Base.Evaluation.Evaluator import EvaluatorHoldout

# from Data_manager.Movielens_20m.Movielens20MReader import Movielens20MReader
from Data_manager.Movielens_1m.Movielens1MReader import Movielens1MReader
from Data_manager.DataSplitter_k_fold import DataSplitter_Warm_k_fold
import scipy.sparse as sps


dataReader = Movielens1MReader()

# Splitting the dataset. This split will produce a warm item split
# To replicate the original experimens use the dataset accessible here with a cold item split:
# https://mmprj.github.io/mtrm_dataset/index
dataSplitter = DataSplitter_Warm_k_fold(dataReader)
dataSplitter.load_data()

# Each URM is a scipy.sparse matrix of shape |users|x|items|
URM_train, URM_validation, URM_test = dataSplitter.get_holdout_split()

# The ICM is a scipy.sparse matrix of shape |items|x|features|
ICM = dataSplitter.get_ICM_from_name("ICM_genre")
print("ICM:\n");
print(ICM.toarray());
print("URM:\n")
print(URM_train.toarray());

URM_train[1,5]=3
URM_train[3,0]=4
URM_train[4,3]=3
URM_train[3,6]=4
URM_train[1,7]=3
URM_train[3,8]=4
URM_train[3,9]=4
URM_train[1,89]=3
URM_train[3,800]=4
URM_train[3,600]=4
URM_train[1,711]=3
URM_train[3,811]=4

print(URM_train.toarray());

# This contains the items to be ignored during the evaluation step
# In a cold items setting this should contain the indices of the warm items
ignore_items = []

evaluator_validation = EvaluatorHoldout(URM_validation, cutoff_list=[5], ignore_items=ignore_items)
evaluator_test = EvaluatorHoldout(URM_test, cutoff_list=[5], ignore_items=ignore_items)

# This is used by the ML model of CFeCBF to perform early stopping and may be omitted.
# ICM_target allows to set a different ICM for this validation step, providing flexibility in including
# features present in either validation or test but not in train
evaluator_validation_earlystopping = EvaluatorCFW_D_wrapper(evaluator_validation, ICM_target=ICM, model_to_use="last")
firstTime=True;
# We compute the similarity matrix resulting from a RP3beta recommender
# Note that we have not included the code for parameter tuning, which should be done
cf_parameters = {'topK': 500,
                 'alpha': 0.9,
                 'beta': 0.7,
                 'normalize_similarity': True,
                 'firstTime':firstTime}

recommender_collaborative = RP3betaRecommender(URM_train)
recommender_collaborative.fit(**cf_parameters)

result_dict, result_string = evaluator_test.evaluateRecommender(recommender_collaborative)
print("CF recommendation quality is: {}".format(result_string))


# We get the similarity matrix
# The similarity is a scipy.sparse matrix of shape |items|x|items|
similarity_collaborative = recommender_collaborative.W_sparse.copy()

# We instance and fit the feature weighting algorithm, it takes as input:
# - The train URM
# - The ICM
# - The collaborative similarity matrix
# Note that we have not included the code for parameter tuning, which should be done as those are just default parameters

fw_parameters =  {'epochs': 5,
                  'learning_rate': 0.0001,
                  'sgd_mode': 'adam',
                  'add_zeros_quota': 1.0,
                  'l1_reg': 0.01,
                  'l2_reg': 0.001,
                  'topK': 100,
                  'use_dropout': True,
                  'dropout_perc': 0.7,
                  'initialization_mode_D': 'one',
                  'positive_only_D': False,
                  'normalize_similarity': False,
                  'firstTime':firstTime}

recommender_fw = Feature_Weighting(URM_train, ICM, similarity_collaborative)
recommender_fw.fit(**fw_parameters,
                   evaluator_object=evaluator_validation_earlystopping,
                   stop_on_validation=True,
                   validation_every_n = 5,
                   lower_validations_allowed=10,
                   validation_metric="MAP")


result_dict, result_string = evaluator_test.evaluateRecommender(recommender_fw)
print("CFeCBF recommendation quality is: {}".format(result_string))
