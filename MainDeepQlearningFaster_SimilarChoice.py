
from Environnement import *
from GridSearch import *
import matplotlib.pyplot as plt
from torch import nn

print(">>>>>>>>>>> TESTING THE AGENT : Similar choice <<<<<<<<<<<<<<<<<<")

# ------------ Defining several parameters - others will be chosen by grid search --------------
N_items = 4
N_recommended = 1
memory = 1
choiceMethod =  'DeepQlearningFaster'
rewardType = 'Trust'
behaviour = 'similar'
rewardParameters = [1,1]
steps = 10
epochs = 3
train_list = [True for u in range(3) ]+[ False, False ]
more_params = {'debug' : True, 'subset_size':4} #Here, the subset will exactly be the number of available actions

#------------- Defining the environnement  -----------
environnement = Environnement(N_items, N_recommended, behaviour,  rewardType , rewardParameters )

#>>> let's test the efficiency of our algorithm by testing with this simplified set:
for item in environnement.items.items :
    item.cost = 1
environnement.items.items[1].cost =0


environnement.items.similarities = np.array([[  -np.inf,  0.1 , 0.1, 0.8],
[0.1, -np.inf, 0.1, 0.8],
 [ 0.1,  0.1,  -np.inf,  0.8],
 [0.8, 0.8, 0.8 , -np.inf]
   ])
#<<<

environnement.items.display(True)


#Create model
model = nn.Sequential(
    nn.Linear(memory+2*N_recommended, 10),
    nn.SELU(),
    nn.Linear(10, 1)
    #nn.SELU(),
    #nn.Linear(5, 1),
 #   nn.Sigmoid()

)
trainable_layers = [0,2]

deepQModel = {'model': model, 'trainable_layers': trainable_layers}

# >>> Grid search over the parameters to get the best parameters
gridSearch = GridSearch()
num_avg = 3
_ , params = gridSearch(num_avg, environnement, memory, choiceMethod, epochs, train_list, steps=steps, more_params = more_params, deepQModel=deepQModel)

print("Testing the Grid Search parameters: ")

#------------ launching the episode series : Average the learning processes results   ---------------
#(less randomness in the plots), for statistical study, than the Series class
num_avg = 3
avgSeries = AverageSeries(num_avg, environnement, memory, choiceMethod, params, epochs, train_list, steps, deepQModel)
Rewards = avgSeries.avgRewards


plt.figure()
plt.plot(Rewards, 'r-')
plt.title("Average reward per serie")
plt.show()
#
#
