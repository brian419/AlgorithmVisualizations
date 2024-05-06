import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from matplotlib.animation import FuncAnimation

# Generating synthetic dataset
X, y = make_classification(n_samples=100, n_features=2, n_informative=2, n_redundant=0, random_state=42)

# Create a meshgrid for plotting decision boundaries
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

# Initialize the GBM classifier
gbm_model = GradientBoostingClassifier(n_estimators=10, learning_rate=0.1, random_state=42)

# Initialize the figure and axes
fig, ax = plt.subplots()
ax.set_xlim(xx.min(), xx.max())
ax.set_ylim(yy.min(), yy.max())

# Scatter plot of the data points
scat = ax.scatter(X[:, 0], X[:, 1], c=y, s=20, edgecolor='k')

# Function to update the plot for each frame in the animation
def update(frame):
    global scat  # Declare scat as a global variable
    if frame == 0:
        return scat,
    
    # Train the GBM model using a subset of the data
    gbm_model.fit(X[:frame, :], y[:frame])
    
    # Predictions for the meshgrid points
    Z = gbm_model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Plot decision boundaries and update scatter plot
    ax.clear()
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.contourf(xx, yy, Z, alpha=0.4)
    scat = ax.scatter(X[:, 0], X[:, 1], c=y, s=20, edgecolor='k')
    
    return scat,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(X)+1, interval=500, blit=True)

plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Gradient Boosting Machines (GBM) Learning Process')

plt.show()
