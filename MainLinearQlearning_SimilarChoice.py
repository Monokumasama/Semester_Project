
from Environnement import *
from GridSearch import *
import matplotlib.pyplot as plt

print(">>>>>>>>>>> TESTING THE AGENT : IN CASE THE CUSTOMER MAKES SIMILAR CHOICES <<<<<<<<<<<<<<<<<<")
print("In this setting, the number of recommended items is 2. And only 2 items have a cost of 0. But the customer makes similar choices. Will the agent adapt?")

# ------------ Defining several parameters - others will be chosen by grid search --------------
N_items = 4
N_recommended = 1
memory = 1
choiceMethod =   'LinearQlearning'
rewardType = 'Trust'
behaviour = 'similar'
rewardParameters = [1,1]
steps = 20
epochs = 3
train_list = [True for u in range(3) ]+[ False, False ]
p = 0.7


#------------- Defining the environnement  -----------
environnement = Environnement(N_items, N_recommended, behaviour,  rewardType , rewardParameters, proba_p=p )

#>>> let's test the efficiency of our algorithm by testing with this simplified set:
for item in environnement.items.items :
    item.cost = 1
environnement.items.items[1].cost =0
environnement.items.items[3].cost =0
#environnement.items.items[1].cost =0.5

environnement.items.similarities = np.array([[  -np.inf,  0.1 , 0.1, 0.8],
[0.1, -np.inf, 0.1, 0.8],
 [ 0.1,  0.1,  -np.inf,  0.8],
 [0.8, 0.8, 0.8 , -np.inf]
   ])

#<<<

environnement.items.display(True,True)


# >>> Grid search over the parameters to get the best parameters
gridSearch = GridSearch()
num_avg = 3
_ , params = gridSearch(num_avg, environnement, memory, choiceMethod, epochs, train_list, steps=steps)
#params = {'gamma': 0.1, 'hidden_size': 10, 'epsilon': 0.2, 'learning_rate': 0.01, 'QLchoiceMethod': 'eGreedy'}


#------------ launching the episode series : Average the learning processes results   ---------------
#(less randomness in the plots), for statistical study, than the Series class
num_avg = 3
avgSeries = AverageSeries(num_avg, environnement, memory, choiceMethod, params, epochs, train_list, steps)
Rewards = avgSeries.avgRewards


plt.figure()
plt.plot(Rewards, 'r-')
plt.title("Average reward per serie")
plt.show()
#
#
#Success ! Reward often of 20, the max available reward...