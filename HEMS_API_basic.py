# Optimization Course - 24h Market Clearing with network Primal - IEEE 6 Bus network
# Author: Íngrid Munné-Collado
# Date: 09/01/2021

# Requirements: Install pyomo, glpk and gurobi. You should apply for an academic license in gurobi
from pyomo.environ import *
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import pandas as pd
import numpy as np

# Creating the model
model = AbstractModel()

# sets


# Defining Parameters
model.U_pv = Param()
model.C_grid = Param()
model.C_EV = Param()
model.P_demanda_total = Param()
model.P_max_PV = Param()
model.P_max_EV = Param()
model.P_max_grid = Param()

# Defining Variables
model.p_pv = Var(within=NonNegativeReals) #pv generada
# model.p_pv_aut = Var(within=NonNegativeReals) #pv autoconsum
model.p_pv_ex = Var(within=NonNegativeReals) #excedent que bolco a xarxa
model.p_ev = Var(within=NonNegativeReals)
model.p_grid = Var(within=NonNegativeReals) #consum de xarxa

# Defining Objective Function
def benefits(model):
    return ((model.U_pv * model.p_pv_ex) - (model.C_grid * model.p_grid + model.C_EV * model.p_ev))
model.benefits_of = Objective(rule=benefits, sense=maximize)

# constraints
# C1 PV max production
def pv_MAX(model):
    return model.p_pv <= model.P_max_PV
model.pv_max_limit = Constraint(rule=pv_MAX)

# C2 Max grid consumption
def pgrid_MAX(model):
    return model.p_grid <= model.P_max_grid
model.pgrid_max_limit = Constraint(rule=pgrid_MAX)

# C3 Max EV consumption
def pev_MAX(model):
    return model.p_ev <= model.P_max_EV
model.pgrid_max_limit = Constraint(rule=pev_MAX)

# C4 grid balance
def power_balance(model):
    return model.P_demanda_total == model.p_grid + model.p_ev - (model.p_pv - model.p_pv_ex)
model.powerbalance = Constraint(rule=power_balance)

# C5 PV balance
def PV_balance(model):
    return model.p_pv_ex == model.p_pv - model.P_demanda_total
model.PVbalance = Constraint(rule=PV_balance)

# choose the solver
opt = pyo.SolverFactory('glpk')

# Create a model instance and optimize
instance = model.create_instance('HEMS_API.dat')

# Solve the optimization problem
results = opt.solve(instance)
# Display results of the code.
instance.display()



