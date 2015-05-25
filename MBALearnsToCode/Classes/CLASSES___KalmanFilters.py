from numpy import diag, sqrt
from numpy.linalg import pinv
from MBALearnsToCode.Classes.CLASSES___ProbabilityDensityFunctions import gaussian_density_function as gauss_pdf


class ExtendedKalmanFilter:
    def __init__(self, state_means, state_covariances,
                 transition_means_lambda, transition_means_jacobi_lambda, transition_covariances_lambda,
                 observation_means_lambda, observation_means_jacobi_lambda, observation_covariances_lambda):
        self.means = state_means
        self.covariances = state_covariances
        self.transition_means_lambda = transition_means_lambda
        self.transition_means_jacobi_lambda = transition_means_jacobi_lambda
        self.transition_covariances_lambda = transition_covariances_lambda
        self.observation_means_lambda = observation_means_lambda
        self.observation_means_jacobi_lambda = observation_means_jacobi_lambda
        self.observation_covariances_lambda = observation_covariances_lambda

    def standard_deviations(self):
        return sqrt(diag(self.covariances))

    def predict(self, control_data):
        self.means = self.transition_means_lambda(self.means, control_data)
        F = self.transition_means_jacobi_lambda(self.means, control_data)
        self.covariances = F.dot(self.covariances).dot(F.T) + self.transition_covariances_lambda(control_data)

    def update(self, observation_data):
        H = self.observation_means_jacobi_lambda(self.means)
        K = self.covariances.dot(H.T).dot(pinv(H.dot(self.covariances).dot(H.T) +
                                               self.observation_covariances_lambda(observation_data)))
        self.means += K.dot(observation_data - self.observation_means_lambda(self.means))
        self.covariances -= K.dot(H).dot(self.covariances)