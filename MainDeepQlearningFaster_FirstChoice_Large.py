
from Environnement import *
from GridSearch import *
import matplotlib.pyplot as plt
from torch import nn

print(">>>>>>>>>>> TESTING THE AGENT : IN CASE THE CUSTOMER ALWAYS CHOOSES THE FIRST RECOMMENDATION <<<<<<<<<<<<<<<<<<")

# ------------ Defining several parameters - others will be chosen by grid search --------------
N_items = 10000
N_recommended = 3
memory = 2
choiceMethod =  'DeepQlearningFaster'
rewardType = 'Trust'
behaviour = 'choiceFirst'
rewardParameters = [1,1]
steps = 10
epochs = 3
train_list = [True for u in range(3) ]+[ False, False ]
more_params = {'debug' : False, 'subset_size':10}

#------------- Defining the environnement  -----------
environnement = Environnement(N_items, N_recommended, behaviour,  rewardType , rewardParameters )


#environnement.items.display(True)


#Create model
model = nn.Sequential(
    nn.Linear(memory+2*N_recommended, 20),
    nn.SELU(),
    nn.Linear(20, 5),
    nn.SELU(),
    nn.Linear(5, 1),
    nn.Sigmoid()

)
trainable_layers = [0,2,4]

deepQModel = {'model': model, 'trainable_layers': trainable_layers}

# >>> Grid search over the parameters to get the best parameters
gridSearch = GridSearch()
num_avg = 3
_ , params = gridSearch(num_avg, environnement, memory, choiceMethod, epochs, train_list, steps=steps, more_params = more_params, deepQModel=deepQModel)

print("Testing the Grid Search parameters: ")

#------------ launching the episode series : Average the learning processes results   ---------------
#(less randomness in the plots), for statistical study, than the Series class
num_avg = 3
epochs = 10
avgSeries = AverageSeries(num_avg, environnement, memory, choiceMethod, params, epochs, train_list, steps, deepQModel)
Rewards = avgSeries.avgRewards


plt.figure()
plt.plot(Rewards, 'r-')
plt.title("Average reward per serie")
plt.show()
#
#
#As it is an approximate function : it does not work as well as it should...