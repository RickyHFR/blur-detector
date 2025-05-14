import torch
import torch.nn as nn

class GaussianNB(nn.Module):
    def __init__(self, n_features, n_classes):
        super().__init__()
        self.n_features = n_features
        self.n_classes = n_classes
        # Log‐priors, shape (n_classes,)
        self.log_prior = nn.Parameter(torch.zeros(n_classes), requires_grad=False)
        # Means and log-variances, shape (n_classes, n_features)
        self.class_mean = nn.Parameter(torch.zeros(n_classes, n_features), requires_grad=False)
        self.class_log_var = nn.Parameter(torch.zeros(n_classes, n_features), requires_grad=False)

    def fit(self, X: torch.Tensor, y: torch.Tensor):
        """
        Estimate class priors, means, and variances from data.
        X: (N, D) features
        y: (N,) integer class labels in [0..n_classes-1]
        """
        N, D = X.shape
        for c in range(self.n_classes):
            mask = (y == c)
            Nc = mask.sum().item()
            # avoid zero-count
            if Nc == 0:
                continue
            Xc = X[mask]
            # prior = Nc/N
            self.log_prior.data[c] = torch.log(torch.tensor(Nc / N))
            # mean and var
            mu = Xc.mean(dim=0)
            var = Xc.var(dim=0, unbiased=False) + 1e-6  # add small epsilon
            self.class_mean.data[c] = mu
            self.class_log_var.data[c] = torch.log(var)

    def forward(self, X: torch.Tensor):
        """
        Compute log-probabilities for each class.
        Returns: (N, n_classes) log P(y=c | X)
        """
        # Expand: X → (N, 1, D), means/vars → (1, C, D)
        X_exp = X.unsqueeze(1)  # (N,1,D)
        mu = self.class_mean.unsqueeze(0)      # (1,C,D)
        log_var = self.class_log_var.unsqueeze(0)  # (1,C,D)

        # Gaussian log-likelihood:
        #   −0.5 * [ log(2πσ^2) + (x−μ)^2/σ^2 ]
        ll = -0.5 * (log_var + ((X_exp - mu)**2 / log_var.exp()))  
        ll = ll.sum(dim=2)  # sum over features → (N,C)

        # Add log-priors
        log_prior = self.log_prior.unsqueeze(0)  # (1,C)
        return ll + log_prior  # (N,C)

    def predict(self, X: torch.Tensor):
        """Return predicted class indices."""
        log_probs = self.forward(X)
        return log_probs.argmax(dim=1)

    def predict_proba(self, X: torch.Tensor):
        """Return normalized probabilities P(y|X)."""
        log_probs = self.forward(X)
        return torch.exp(log_probs - log_probs.logsumexp(dim=1, keepdim=True))
