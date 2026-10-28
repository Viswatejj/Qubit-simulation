import numpy as np

#Initializing teh the QUBIT in base states
ket0 = np.array([[1],[0]], dtype=complex)  #|0>
ket1 = np.array([[0],[1]], dtype=complex)  #|1>
state = ket0  #Original state of the qubit

#setting up the QuantumGate matrices

Gate_identity = np.array([[1,0],[0,1]], dtype=complex)
Gate_PauliX = np.array([[0,1], [1,0]], dtype=complex)
Gate_Hadamard = np.sqrt(1/2)*np.array([[1,1],[1,-1]], dtype=complex)
Gate_pauliY = np.array([[0, -1j], [1j, 0]], dtype=complex)
Gate_pauliZ = np.array([[1, 0], [0, -1]], dtype=complex)

gates = {
    "1": ("Identity",  Gate_identity),
    "2": ("Pauli X",   Gate_PauliX),
    "3": ("Pauli Y",  Gate_pauliY),
    "4": ("Pauli Z",  Gate_pauliZ),
    "5": ("Hadamard",  Gate_Hadamard),
}

#gate that applies a given function
def applyGate(gate, stateParameter):
    return gate@stateParameter

#gate that returns the probabilities each qubit ket
def probability(stateParameter):
    return np.abs(stateParameter) ** 2

initializationChoice = int(input('''1. |0>
2. |1>
3. Custom
Initialize the qubit: '''))

match initializationChoice:
    case 1:
        state = ket0
    case 2:
        state = ket1
    case 3:
        alpha = float(input("Enter the coeffecients of |0> : "))
        beta = float(input("Enter the coeffecients of |1> : "))
        state = np.array([[alpha*ket0], [beta*ket1]])
        if (np.square(np.abs(alpha)) + np.square(np.abs(beta)) != 1):
            print("Invalid")
            exit()


while True:
    print("\nGates:")
    for key, (name, _) in gates.items():
        print(f"  {key}. {name}")
    choice = input("Choose a gate (or q to quit): ")

    if choice == "q":
        break
    if choice not in gates:
        print("Invalid entry")
        continue

    name, gate = gates[choice]
    state = applyGate(gate, state)
    print(f"After {name}:")
    print(f"  State:        {np.round(state.flatten(), 3)}")
    print(f"  Probabilities:    {np.round(probability(state), 3)}")