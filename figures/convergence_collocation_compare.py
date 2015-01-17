import chaospy as cp
import pylab as pl
import numpy as np

cp.seed(1124)
#cp.seed(9125593)
pl.rc("figure", figsize=[6,4])

Nt = 10**2
N = 10

def E_analytical(x):
    return 90*(1-np.exp(-0.1*x))/(x)

    
def V_analytical(x):
    return 1220*(1-np.exp(-0.2*x))/(3*x) - (90*(1-np.exp(-0.1*x))/(x))**2


def u(x,a, I):
    return I*np.exp(-a*x)

a = cp.Uniform(0, 0.1)
I = cp.Uniform(8, 10)
dist = cp.J(a,I)

T = np.linspace(0, 10, Nt+1)[1:]
dt = 10./Nt


error = []
var = []
K = []
for n in range(1,N):
     
    P = cp.orth_ttr(n, dist)
    nodes = dist.sample(2*len(P))
    K.append(2*len(P))
    solves = [u(T, s[0], s[1]) for s in nodes.T]
    U_hat = cp.fit_regression(P, nodes, solves,rule="LS")

    error.append(dt*np.sum(np.abs(E_analytical(T) - cp.E(U_hat,dist))))
    var.append(dt*np.sum(np.abs(V_analytical(T) - cp.Var(U_hat,dist))))

pl.figure()
pl.plot(K,error,linewidth=2)
pl.plot(K, var,linewidth=2)


error = []
var = []
K = []
for n in range(1,N):
     
    P = cp.orth_ttr(n, dist)
    nodes = dist.sample(2*len(P), "M")
    K.append(2*len(P))
    solves = [u(T, s[0], s[1]) for s in nodes.T]
    U_hat = cp.fit_regression(P, nodes, solves,rule="LS")

    error.append(dt*np.sum(np.abs(E_analytical(T) - cp.E(U_hat,dist))))
    var.append(dt*np.sum(np.abs(V_analytical(T) - cp.Var(U_hat,dist))))

 
pl.plot(K,error,linewidth=2)
pl.plot(K, var,linewidth=2)


pl.xlabel("Samples, k")
pl.ylabel("Error")
pl.yscale('log')
pl.title("Error in expectation value and variance ")
pl.legend(["Expectation value","Variance", "Expectation value, Hammersley","Variance, Hammersley"])
#pl.savefig("convergence_collocation_compare.png")



pl.figure()
nodes = dist.sample(100)
pl.scatter(nodes[0],nodes[1])
pl.xlabel("a")
pl.ylabel("I")
pl.savefig("samples_S.png")

pl.figure()
nodes = dist.sample(100, "M")
pl.scatter(nodes[0],nodes[1])
pl.xlabel("a")
pl.ylabel("I")
pl.savefig("samples_M.png")

pl.figure()
nodes = dist.sample(100, "H")
pl.scatter(nodes[0],nodes[1])
pl.xlabel("a")
pl.ylabel("I")
pl.savefig("samples_H.png")

pl.figure()
nodes = dist.sample(100, "LH")
pl.scatter(nodes[0],nodes[1])
pl.xlabel("a")
pl.ylabel("I")
pl.savefig("samples_LH.png")


pl.show()



