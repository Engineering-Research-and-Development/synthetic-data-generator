import numpy as np
import pandas as pd
import scipy.stats as ss


class TabularComparisonEvaluator:
    def __init__(self, real_data:pd.DataFrame,
                 synthetic_data:pd.DataFrame,
                 numerical_columns:list[str],
                 categorical_columns:list[str]
                 ):
        self._real_data = real_data
        self._synthetic_data = synthetic_data
        self._numerical_columns = numerical_columns
        self._categorical_columns = categorical_columns


    def compute(self):
        if len(self._numerical_columns) <= 1 and len(self._categorical_columns) <= 1:
            return {"available": False}

        report = {
            "statistical_metrics": self._evaluate_statistical_properties(),
            "adherence_metrics": self._evaluate_adherence(),
            "novelty_metrics": self._evaluate_novelty()
        }
        return report


    @staticmethod
    def _compute_cramer_v(data1:np.array, data2:np.array):
        """
        Computes Cramer's V on a pair of categorical columns
        :param data1: first column
        :param data2: second column
        :return: Cramer's V
        """
        confusion_matrix = pd.crosstab(data1, data2)
        chi2 = ss.chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum()
        phi2 = chi2 / n
        r, k = confusion_matrix.shape
        phi2_corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        r_corr = r - ((r - 1) ** 2) / (n - 1)
        k_corr = k - ((k - 1) ** 2) / (n - 1)
        V = np.sqrt(phi2_corr / min((k_corr - 1), (r_corr - 1)))
        return V


    def _evaluate_cramer_v_distance(self) -> float:
        """
        Evaluates Cramer's v with Bias Correction https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V on categorical data,
        evaluating pairwise columns. Each pair of columns is evaluated on both datasets, appending scores in a list
        and returning the aggregate.

        :return: A score ranging from 0 to 1. A score of 0 is the worst possible score, while 1 is the best possible score,
        meaning that category pairs are perfectly balanced
        """
        if len(self._categorical_columns) < 2:
            return 0

        contingency_scores_distances = []
        for idx, col in enumerate(self._categorical_columns[:-1]):
            for col2 in self._categorical_columns[idx + 1:]:
                V_real = self._compute_cramer_v(self._real_data[col].to_numpy(), self._real_data[col2].to_numpy())
                V_synth = self._compute_cramer_v(self._synthetic_data[col].to_numpy(), self._synthetic_data[col2].to_numpy())
                contingency_scores_distances.append(np.abs(V_real - V_synth))

        final_score = 1 - np.mean(contingency_scores_distances)
        return np.clip(final_score, 0, 1)


    def _evaluate_wasserstein_distance(self) -> float:
        """
        Computing the Wasserstein distance for each numerical column. The score is computed using a different approach,
        trying to clip the values between 0 and 1. With 1 it means that the distribution of data is aligned, while with
        0 means that the distribution of data are largely unaligned.
        In particular, the Wasserstein distance score will be clipped between 0 and |max - min|, where max and min
        are related to the real dataset distribution. In the end, the score is scaled between 0 and 1
        :return: A single score, computed as 1 - mean(scores)
        """
        if len(self._numerical_columns) < 1:
            return 0

        wass_distance_scores = []
        for col in self._numerical_columns:
            real_data = self._real_data[col].to_numpy()
            synth_data = self._synthetic_data[col].to_numpy()
            distance = np.abs(np.max(real_data) - np.min(real_data))
            wass_dist = ss.wasserstein_distance(real_data, synth_data)
            wass_dist = np.clip(wass_dist, 0, distance) / distance
            wass_distance_scores.append(wass_dist)

        return 1 - np.mean(wass_distance_scores)


    def _evaluate_statistical_properties(self) -> dict:
        """
        This function evaluates both Wasserstein distance for numerical features and Cramer's V for categorical ones,
        providing a weighted mean of the scores based on the number of features
        :return: a dictionary report containing a brief statistical report
        """
        cramer_v = self._evaluate_cramer_v_distance()
        wass_distance = self._evaluate_wasserstein_distance()
        n_features = len(self._real_data.columns)
        stat_compliance = (len(self._categorical_columns) * cramer_v +
                           len(self._numerical_columns) * wass_distance) / n_features

        report = {
            "Total Statistical Compliance [%]": np.round(stat_compliance*100, 2).item(),
            "Categorical Features Cramer's V [%]": np.round(cramer_v*100, 2).item(),
            "Numerical Features Wasserstein Distance [%]": np.round(wass_distance*100, 2).item()
        }

        return report


    def _evaluate_novelty(self):
        """
        This function evaluates in two steps the following metrics
        1) The number of unique samples generated in the synthetic dataset with respect to the real data
        2) The number of duplicated samples in the synthetic dataset
        :return: a dictionary report with percentage of duplicated data
        """
        synth_len = self._synthetic_data.shape[0]

        synth_unique = self._synthetic_data.drop_duplicates()
        synth_unique_len = synth_unique.shape[0]

        real_unique = self._real_data.drop_duplicates()
        real_unique_len = real_unique.shape[0]

        concat_df = pd.concat([real_unique, synth_unique], axis=0)
        concat_unique = concat_df.drop_duplicates()
        conc_unique_len = concat_unique.shape[0]

        new_synt_data = synth_len - ((real_unique_len + synth_unique_len) - conc_unique_len)

        report = {
            "Unique Synthetic Data [%]": np.round(synth_unique_len/synth_len*100, 2).item(),
            "New Synthetic Data [%]:": np.round(new_synt_data/synth_len*100, 2).item()
        }
        return report


    def _evaluate_adherence(self):
        """
        Computes adherence metrics such as:
        - Synthetic Categories Adherence to Real Categories
        - Numerical min-max boundaries
        - Primary / Foreign Keys integrity and uniqueness
        :return:
        """
        category_adherence_score = {}
        real_categorical = self._real_data[self._categorical_columns]
        synth_categorical = self._synthetic_data[self._categorical_columns]
        for col in self._categorical_columns:
            item_diff = set(synth_categorical[col].unique()) - set(real_categorical[col].unique())
            n_items = synth_categorical[col].isin(item_diff)
            category_adherence_score[col] = np.round(n_items / self._synthetic_data.shape[0] * 100, 2).item()

        boundary_adherence_score = {}
        real_numerical = self._real_data[self._numerical_columns]
        synth_numerical = self._synthetic_data[self._numerical_columns]
        for col in self._numerical_columns:
            report = real_numerical[col].describe()
            max_boundary = report["max"]
            min_boundary = report["min"]
            df_filtered = synth_numerical[(synth_numerical[col] <= max_boundary) & (synth_numerical[col] >= min_boundary)]
            n_items_in = df_filtered.shape[0]
            boundary_adherence_score[col] = np.round(n_items_in / self._synthetic_data.shape[0] * 100, 2).item()

        report = {
            "category_adherence_score [%]": category_adherence_score,
            "boundary_adherence_score [%]": boundary_adherence_score
        }
        return report



