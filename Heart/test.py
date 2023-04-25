import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5] # remplacez les valeurs par les coordonnées x de vos points
y = [1, 2, 3, 4, 5] # remplacez les valeurs par les coordonnées y de vos points

fig, ax = plt.subplots()
ax.plot(x, y, 'ro')
ax.set_title('Points du cœur')
plt.show()