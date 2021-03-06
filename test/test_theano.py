'''
Created on 7 juil. 2016

@author: lvanni
'''
from numpy import array
import numpy
import theano
from theano.compile import function
from theano.compile.io import In

import theano.tensor as T


def tuto():
    
    print "A Real Example: Logistic Regression"
    print "-----------------------------------"
    rng = numpy.random
    N = 400                                   # training sample size
    feats = 784                               # number of input variables => exemple Image 28x28 pixels = 784 variables
    
    # generate a dataset: D = (input_values, target_class)
    # D = [X, Y]
    D = (rng.randn(N, feats), rng.randint(size=N, low=0, high=2))
    training_steps = 10000 # nombre de retropropagation / backpropagation
    
    print D
    
    # Declare Theano symbolic variables
    x = T.dmatrix("x")
    y = T.dvector("y")
    
    # initialize the weight vector w randomly
    #
    # this and the following bias variable b
    # are shared so they keep their values
    # between training iterations (updates)
    w = theano.shared(rng.randn(feats), name="w")
    
    # initialize the bias term
    b = theano.shared(0., name="b")
    
    print("Initial model:")
    print "W:"
    print(w.get_value())
    print "B:"
    print(b.get_value())
    
    # Construct Theano expression graph
    p_1 = 1 / (1 + T.exp(-T.dot(x, w) - b))   # Probability that target = 1 => fonction resultat entre 0 et 1
    prediction = p_1 > 0.5                    # The prediction thresholded
    xent = -y * T.log(p_1) - (1-y) * T.log(1-p_1) # Cross-entropy loss function ===> calcul d'erreur => vecteur d'erreur
    cost = xent.mean() + 0.01 * (w ** 2).sum()# The cost to minimize => contrainte sur les poids pour eviter des valeurs trop grandes
    gw, gb = T.grad(cost, [w, b])             # Compute the gradient of the cost => gw correction poids ; bg correction biais
                                              # w.r.t weight vector w and
                                              # bias term b
                                              # (we shall return to this in a
                                              # following section of this tutorial)
    
    # Compile
    train = theano.function(
              inputs=[x,y],
              outputs=[prediction, xent],
              updates=((w, w - 0.1 * gw), (b, b - 0.1 * gb))) # 0.1 => learning rate
    predict = theano.function(inputs=[x], outputs=prediction)
    
    # Train
    for i in range(training_steps):
        pred, err = train(D[0], D[1])
    
    print("Final model:")
    print "B:"
    print(w.get_value())
    print "B:"
    print(b.get_value())
    print("target values for D:")
    print(D[1])
    print("prediction on D:")
    test = rng.randn(1, feats)
    print(predict(test)) # On test sur les valeurs de depart

if __name__ == '__main__':
    tuto()